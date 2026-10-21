"""Bounded, allowlisted inspectors. No cloud/resource write operations are implemented.
A GET-only adapter is not a security boundary against a compromised process with a raw engine socket.
"""
from __future__ import annotations
import http.client, json, socket, time
from datetime import datetime, timezone
from uuid import uuid4
from pathlib import Path
from .store import now

MAX_PAGES = 5
MAX_ITEMS = 1000
MAX_RESPONSE_BYTES = 8 * 1024 * 1024
AWS_SERVICES = ['ec2', 'autoscaling', 'eks', 'ecs', 'lambda', 'rds', 'elbv2', 'cloudwatch', 'fis']

class InspectionError(ValueError):
    pass

class Collector:
    def __init__(self, config):
        self.config = config
        self.start = now()
        self.deadline = time.monotonic() + 120
        self.resources = []
        self.coverage = []
        self.truncated = False
        self.identity = {}

    def check_deadline(self):
        if time.monotonic() > self.deadline:
            raise InspectionError('InspectionDeadlineExceeded')

    def add(self, identifier, name, model, kind, location='', state='unknown', **facts):
        if len(self.resources) >= 20000:
            self.truncated = True
            return
        self.resources.append({'id': str(identifier), 'name': str(name), 'provider': self.config['kind'], 'model': model, 'kind': kind, 'location': location, 'state': str(state), 'facts': facts})

    def group(self, scope, action):
        before = len(self.resources)
        self.truncated = False
        try:
            self.check_deadline()
            action()
            status = 'truncated' if self.truncated else 'complete'
            detail = 'Collection limit reached. This is not a complete inventory.' if self.truncated else 'All requested pages were read within this collector’s documented scope.'
            self.coverage.append({'scope': scope, 'status': status, 'resource_count': len(self.resources) - before, 'error_code': '', 'detail': detail})
        except Exception as exc:
            # Do not persist SDK exception text, response bodies, environment values, or credentials.
            code = exc.__class__.__name__
            if hasattr(exc, 'response') and isinstance(exc.response, dict):
                code = exc.response.get('Error', {}).get('Code', code)
            if isinstance(exc, InspectionError):
                code = str(exc)
            if hasattr(exc, 'status') and isinstance(exc.status, int):
                code = 'HTTP' + str(exc.status)
            denied = any(t in code.lower() for t in ['denied', 'unauthor', 'forbidden', '403'])
            self.coverage.append({'scope': scope, 'status': 'denied' if denied else 'error', 'resource_count': len(self.resources) - before, 'error_code': code[:200], 'detail': 'This scope was not completely inspected. Previously collected resources may be present.'})

    def finish(self, requested, limitations):
        c = self.config
        scope = f"{c['kind']}:{c['id']}"
        if c['kind'] == 'aws':
            scope += ':' + self.identity['account_id'] + ':' + ','.join(c['regions'])
        return {'kind': 'snapshot', 'id': 'snap-' + uuid4().hex[:16], 'revision': 1, 'title': c.get('name', c['id']) + ' · inspection', 'simulated': False, 'data': {'connection_id': c['id'], 'connector': c['kind'], 'scope_id': scope, 'identity': self.identity, 'started_at': self.start, 'ended_at': now(), 'requested_scope': requested, 'coverage': self.coverage, 'resources': self.resources, 'limitations': limitations}}

    def pages(self, client, method, key, **kwargs):
        """Return a bounded collection. Preserve incomplete status instead of treating it as absence."""
        out = []
        if client.can_paginate(method):
            iterator = iter(client.get_paginator(method).paginate(**kwargs))
            for i in range(MAX_PAGES):
                self.check_deadline()
                try:
                    page = next(iterator)
                except StopIteration:
                    break
                values = page.get(key, []) or []
                remaining = MAX_ITEMS - len(out)
                out.extend(values[:remaining])
                more = any(page.get(t) for t in ['NextToken', 'nextToken', 'Marker', 'NextMarker', 'NextContinuationToken', 'NextRecordName'])
                if len(values) > remaining or (len(out) >= MAX_ITEMS and more):
                    self.truncated = True
                    break
                if i == MAX_PAGES - 1 and more:
                    self.truncated = True
            return out
        self.check_deadline()
        page = getattr(client, method)(**kwargs)
        values = page.get(key, []) or []
        if len(values) > MAX_ITEMS or any(page.get(t) for t in ['NextToken', 'nextToken', 'Marker', 'NextMarker']):
            self.truncated = True
        return values[:MAX_ITEMS]


def inspect_aws(config):
    import boto3
    from botocore.config import Config
    c = Collector(config)
    session = boto3.Session(profile_name=config.get('profile') or None)
    sdk_config = Config(connect_timeout=3, read_timeout=8, retries={'total_max_attempts': 2, 'mode': 'standard'}, ignore_configured_endpoint_urls=True)
    # Identity check precedes inventory. Do not infer the account from a profile label.
    identity = session.client('sts', region_name=config['regions'][0], config=sdk_config).get_caller_identity()
    if identity['Account'] != config['expected_account_id']:
        raise InspectionError('AccountMismatch: the authenticated account differs from expected_account_id; no inventory was collected')
    if identity['Arn'].endswith(':root'):
        raise InspectionError('RootIdentityRejected: configure a restricted role or profile instead')
    c.identity = {'account_id': identity['Account'], 'principal_arn': identity['Arn']}
    for region in config['regions']:
        clients = {}
        def client(name):
            if name not in clients:
                clients[name] = session.client(name, region_name=region, config=sdk_config)
            return clients[name]
        def ec2():
            for reservation in c.pages(client('ec2'), 'describe_instances', 'Reservations'):
                for r in reservation.get('Instances', []):
                    c.add(r['InstanceId'], r['InstanceId'], 'ec2', 'EC2 instance', region, r.get('State', {}).get('Name', 'unknown'), instance_type=r.get('InstanceType', ''), zone=r.get('Placement', {}).get('AvailabilityZone', ''), lifecycle=r.get('InstanceLifecycle', 'on-demand'))
        def autoscaling():
            for r in c.pages(client('autoscaling'), 'describe_auto_scaling_groups', 'AutoScalingGroups'):
                c.add(r['AutoScalingGroupARN'], r['AutoScalingGroupName'], 'ec2', 'Auto Scaling group', region, 'configured', desired=r['DesiredCapacity'], minimum=r['MinSize'], maximum=r['MaxSize'], instances=len(r.get('Instances', [])), zones=r.get('AvailabilityZones', []))
        def eks():
            e = client('eks')
            for name in c.pages(e, 'list_clusters', 'clusters'):
                c.check_deadline()
                r = e.describe_cluster(name=name)['cluster']
                c.add(r['arn'], name, 'shared', 'EKS control plane', region, r['status'], version=r.get('version', ''))
                for ng in c.pages(e, 'list_nodegroups', 'nodegroups', clusterName=name):
                    c.check_deadline()
                    n = e.describe_nodegroup(clusterName=name, nodegroupName=ng)['nodegroup']
                    c.add(n['nodegroupArn'], name + '/' + ng, 'eks-ec2', 'EKS managed node group', region, n['status'], capacity_type=n.get('capacityType', ''), desired=n.get('scalingConfig', {}).get('desiredSize', 0))
                for fp in c.pages(e, 'list_fargate_profiles', 'fargateProfileNames', clusterName=name):
                    c.check_deadline()
                    f = e.describe_fargate_profile(clusterName=name, fargateProfileName=fp)['fargateProfile']
                    c.add(f['fargateProfileArn'], name + '/' + fp, 'eks-fargate', 'EKS Fargate profile', region, f['status'], namespaces=[x['namespace'] for x in f.get('selectors', [])])
        def ecs():
            e = client('ecs')
            for cluster_arn in c.pages(e, 'list_clusters', 'clusterArns'):
                c.add(cluster_arn, cluster_arn.split('/')[-1], 'shared', 'ECS cluster', region, 'discovered')
                services = c.pages(e, 'list_services', 'serviceArns', cluster=cluster_arn)
                for i in range(0, len(services), 10):
                    c.check_deadline()
                    result = e.describe_services(cluster=cluster_arn, services=services[i:i+10])
                    if result.get('failures'):
                        raise InspectionError('ECSDescribeServicesPartialFailure')
                    for s in result.get('services', []):
                        lt = s.get('launchType', '')
                        providers = [p['capacityProvider'] for p in s.get('capacityProviderStrategy', [])]
                        model = 'ecs-fargate' if lt == 'FARGATE' or (providers and all(p in ['FARGATE', 'FARGATE_SPOT'] for p in providers)) else ('ecs-ec2' if lt == 'EC2' else 'shared')
                        c.add(s['serviceArn'], s['serviceName'], model, 'ECS service', region, s['status'], desired=s.get('desiredCount', 0), running=s.get('runningCount', 0), pending=s.get('pendingCount', 0), capacity_providers=providers, launch_type=lt or 'not explicit')
                tasks = c.pages(e, 'list_tasks', 'taskArns', cluster=cluster_arn, desiredStatus='RUNNING')
                for i in range(0, len(tasks), 100):
                    c.check_deadline()
                    result = e.describe_tasks(cluster=cluster_arn, tasks=tasks[i:i+100])
                    if result.get('failures'):
                        raise InspectionError('ECSDescribeTasksPartialFailure')
                    for t in result.get('tasks', []):
                        lt = t.get('launchType', 'unknown')
                        model = {'FARGATE': 'ecs-fargate', 'EC2': 'ecs-ec2'}.get(lt, 'shared')
                        c.add(t['taskArn'], t['taskArn'].split('/')[-1], model, 'ECS running task', region, t.get('lastStatus', 'unknown'), launch_type=lt, zone=t.get('availabilityZone', ''))
        def lambdas():
            for r in c.pages(client('lambda'), 'list_functions', 'Functions'):
                c.add(r['FunctionArn'], r['FunctionName'], 'lambda', 'Lambda function', region, 'listed', runtime=r.get('Runtime', r.get('PackageType', 'unknown')), timeout_seconds=r.get('Timeout', 0), memory_mb=r.get('MemorySize', 0), version=r.get('Version', ''))
        def rds():
            r = client('rds')
            for x in c.pages(r, 'describe_db_instances', 'DBInstances'):
                c.add(x['DBInstanceArn'], x['DBInstanceIdentifier'], 'shared', 'RDS instance', region, x['DBInstanceStatus'], engine=x.get('Engine', ''), multi_az=x.get('MultiAZ', False), zone=x.get('AvailabilityZone', ''))
            for x in c.pages(r, 'describe_db_clusters', 'DBClusters'):
                c.add(x['DBClusterArn'], x['DBClusterIdentifier'], 'shared', 'RDS cluster', region, x['Status'], engine=x.get('Engine', ''), zones=x.get('AvailabilityZones', []))
        def elb():
            for r in c.pages(client('elbv2'), 'describe_load_balancers', 'LoadBalancers'):
                c.add(r['LoadBalancerArn'], r['LoadBalancerName'], 'shared', 'Load balancer', region, r.get('State', {}).get('Code', 'unknown'), type=r.get('Type', ''), zones=[x['ZoneName'] for x in r.get('AvailabilityZones', [])])
        def alarms():
            # Metric alarms only: composite alarms and delivery-path testing are separate work.
            for r in c.pages(client('cloudwatch'), 'describe_alarms', 'MetricAlarms', AlarmTypes=['MetricAlarm']):
                c.add(r['AlarmArn'], r['AlarmName'], 'shared', 'CloudWatch metric alarm', region, r['StateValue'], actions_enabled=r.get('ActionsEnabled', False), metric=r.get('MetricName', 'metric math'))
        def fis():
            f = client('fis')
            for r in c.pages(f, 'list_actions', 'actions'):
                c.add(r['id'], r['id'], 'shared', 'FIS action definition', region, 'available')
            for r in c.pages(f, 'list_experiment_templates', 'experimentTemplates'):
                c.add(r['id'], r['id'], 'shared', 'FIS experiment template', region, 'listed')
        handlers = {'ec2': ec2, 'autoscaling': autoscaling, 'eks': eks, 'ecs': ecs, 'lambda': lambdas, 'rds': rds, 'elbv2': elb, 'cloudwatch': alarms, 'fis': fis}
        for service in config.get('services', AWS_SERVICES):
            c.group(region + '/' + service, handlers[service])
    return c.finish([r + '/' + s for r in config['regions'] for s in config.get('services', AWS_SERVICES)], ['This is a bounded configuration inventory, not a workload, dependency, traffic or resilience test.', 'An EKS Fargate profile proves configuration, not that a pod is currently running on Fargate. Self-managed and other EKS compute require Kubernetes-side inspection.', 'ECS service capacity-provider classification may remain unknown; running task launch types are recorded separately.', 'Lambda layer prerequisites, alarm delivery, target health, secrets, function code and container environments are not collected.', 'Collections are limited to five pages or 1,000 items per list operation and a 120-second cooperative deadline; an in-flight SDK call may finish after that deadline.'])

class UnixHTTP(http.client.HTTPConnection):
    def __init__(self, socket_path):
        super().__init__('localhost', timeout=8)
        self.socket_path = socket_path
    def connect(self):
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.socket_path)

def engine_get(socket_path, route):
    if route not in ['/version', '/containers/json?all=true', '/volumes', '/networks']:
        raise InspectionError('EndpointNotAllowlisted')
    conn = UnixHTTP(socket_path)
    try:
        conn.request('GET', route, headers={'Accept': 'application/json'})
        response = conn.getresponse()
        if response.status != 200:
            raise InspectionError('EngineHTTP' + str(response.status))
        body = response.read(MAX_RESPONSE_BYTES + 1)
        if len(body) > MAX_RESPONSE_BYTES:
            raise InspectionError('EngineResponseTooLarge')
        return json.loads(body)
    finally:
        conn.close()

def inspect_engine(config):
    c = Collector(config)
    path = config['socket']
    def version():
        r = engine_get(path, '/version')
        c.identity = {'engine': config['kind'], 'version': str(r.get('Version', 'unknown')), 'api_version': str(r.get('ApiVersion', 'unknown'))}
    def containers():
        values = engine_get(path, '/containers/json?all=true')
        if len(values) > MAX_ITEMS:
            c.truncated = True
        for r in values[:MAX_ITEMS]:
            name = (r.get('Names') or [r['Id'][:12]])[0].lstrip('/')
            c.add(r['Id'], name, config['kind'], 'Container', 'local engine', r.get('State', 'unknown'), image=r.get('Image', ''), status=r.get('Status', ''))
    def volumes():
        values = engine_get(path, '/volumes').get('Volumes') or []
        if len(values) > MAX_ITEMS:
            c.truncated = True
        for r in values[:MAX_ITEMS]:
            c.add(r['Name'], r['Name'], config['kind'], 'Volume', 'local engine', 'listed', driver=r.get('Driver', ''), scope=r.get('Scope', ''))
    def networks():
        values = engine_get(path, '/networks')
        if len(values) > MAX_ITEMS:
            c.truncated = True
        for r in values[:MAX_ITEMS]:
            c.add(r['Id'], r['Name'], config['kind'], 'Network', 'local engine', 'listed', driver=r.get('Driver', ''), scope=r.get('Scope', ''))
    for scope, fn in [('version', version), ('containers', containers), ('volumes', volumes), ('networks', networks)]:
        c.group(scope, fn)
    return c.finish(['version', 'containers', 'volumes', 'networks'], ['Only the configured local Unix socket is used; remote TCP/SSH engine contexts are not supported by this adapter.', 'Container logs, environments, exec, volume contents and host paths are not read.', 'The adapter issues GET requests only. Raw socket access still grants the process engine-level privileges; use an administrator-enforced read-only proxy for stronger isolation.'])

def inspect_kubernetes(config):
    from kubernetes import client, config as kube_config
    c = Collector(config)
    configuration = client.Configuration()
    if config.get('in_cluster'):
        kube_config.load_incluster_config(client_configuration=configuration)
    else:
        kube_config.load_kube_config(config_file=config.get('kubeconfig'), context=config['context'], client_configuration=configuration, persist_config=False)
    if not configuration.verify_ssl:
        raise InspectionError('KubernetesTLSVerificationRequired')
    api = client.ApiClient(configuration)
    core, apps = client.CoreV1Api(api), client.AppsV1Api(api)
    c.identity = {'context': 'in-cluster' if config.get('in_cluster') else config['context'], 'api_server': configuration.host}
    def listing(fn, namespace):
        values = []
        token = None
        for i in range(MAX_PAGES):
            c.check_deadline()
            result = fn(namespace=namespace, limit=200, _continue=token, _request_timeout=(3, 8))
            values.extend(result.items[:max(0, MAX_ITEMS - len(values))])
            token = result.metadata._continue
            if not token:
                break
            if i == MAX_PAGES - 1 or len(values) >= MAX_ITEMS:
                c.truncated = True
                break
        return values
    requested = []
    try:
        for ns in config['namespaces']:
            def pods():
                for r in listing(core.list_namespaced_pod, ns):
                    statuses = r.status.container_statuses or []
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'Pod', ns, r.status.phase or 'unknown', ready_containers=sum(bool(x.ready) for x in statuses), containers=len(statuses), restarts=sum(x.restart_count for x in statuses))
            def deployments():
                for r in listing(apps.list_namespaced_deployment, ns):
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'Deployment', ns, 'observed', desired=r.spec.replicas or 0, ready=r.status.ready_replicas or 0, available=r.status.available_replicas or 0)
            def statefulsets():
                for r in listing(apps.list_namespaced_stateful_set, ns):
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'StatefulSet', ns, 'observed', desired=r.spec.replicas or 0, ready=r.status.ready_replicas or 0)
            def daemonsets():
                for r in listing(apps.list_namespaced_daemon_set, ns):
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'DaemonSet', ns, 'observed', desired=r.status.desired_number_scheduled or 0, ready=r.status.number_ready or 0)
            def services():
                for r in listing(core.list_namespaced_service, ns):
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'Service', ns, 'configured', type=r.spec.type or '')
            def pvcs():
                for r in listing(core.list_namespaced_persistent_volume_claim, ns):
                    c.add(r.metadata.uid, r.metadata.name, 'kubernetes', 'PersistentVolumeClaim', ns, r.status.phase or 'unknown', storage_class=r.spec.storage_class_name or '', access_modes=r.spec.access_modes or [])
            for label, fn in [('pods', pods), ('deployments', deployments), ('statefulsets', statefulsets), ('daemonsets', daemonsets), ('services', services), ('persistentvolumeclaims', pvcs)]:
                requested.append(ns + '/' + label)
                c.group(ns + '/' + label, fn)
    finally:
        api.close()
    return c.finish(requested, ['Only configured namespaces and six allowlisted resource types are read.', 'Kubeconfig is a trusted administrator-provided file; its authentication plugins may execute code. Browser uploads cannot change it.', 'No Secrets, ConfigMaps, container environments, pod logs, exec or cluster-scoped node reads are collected.', 'A Kubernetes context can point to a remote cluster. The administrator must verify the configured context; local hosting does not make its target local.'])


def inspect(config):
    kind = config['kind']
    if kind == 'aws':
        return inspect_aws(config)
    if kind in ('docker', 'podman'):
        return inspect_engine(config)
    if kind == 'kubernetes':
        return inspect_kubernetes(config)
    raise InspectionError('UnsupportedConnector')
