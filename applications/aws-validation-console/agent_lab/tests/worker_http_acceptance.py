#!/usr/bin/env python3
"""Real worker + real loopback workload; provider is explicitly test-only.
No AWS credentials, account, Agent Space or fault target is accessed.
"""
import json,socket,sys,tempfile,threading,time
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]));sys.path.insert(0,str(Path(__file__).resolve().parent))
from conftest import config_dict,World,FakeAWS,approve,TARGET
from lab.models import Configuration,Experiment,TrialRequest
from lab.store import Store
from lab.service import Service
from lab.engine import Engine
from lab.worker import Worker
from lab.util import utcnow,iso,dt


def main():
 checks=[]
 def check(name,condition):
  assert condition,name
  checks.append(name);print('PASS',name,flush=True)
 world=World(utcnow)
 class Instrument(FakeAWS):
  def experiment(self,identifier):
   v=dict(world.experiments[identifier]);elapsed=(utcnow()-dt(v['startTime'])).total_seconds()
   status='stopped' if v.get('forced_stop') else 'completed' if elapsed>=10 else 'running'
   v['state']={'status':status};v['actions']={'fault':{'state':{'status':'running' if status=='running' else 'completed'}}}
   if status!='running':
    from datetime import timedelta
    v['endTime']=iso(dt(v['startTime'])+timedelta(seconds=10))
   ref=self.store.put_record('aws',self.owner,{'explicit_test_provider':True,'experiment':v})
   return {'experiment':v,'source_record_id':ref['id'],'resolved_targets':[{'targetInformation':{'arn':TARGET}}]}
  def checks(self,ids):
   rows=[];active=any((utcnow()-dt(v['startTime'])).total_seconds()<10 and not v.get('forced_stop') for v in world.experiments.values())
   for identifier in ids:
    actual='stopped' if active else 'running';expected=next(c.expected for c in self.b.checks if c.id==identifier)
    r=self.store.put_record('aws',self.owner,{'explicit_test_provider':True,'actual':actual,'resource':TARGET})
    rows.append({'id':identifier,'passed':actual==expected,'actual':actual,'expected':expected,'source_record_id':r['id']})
   return rows
 factory=lambda b,s,o:Instrument(b,s,o,world)
 class Handler(BaseHTTPRequestHandler):
  def do_GET(self):
   active=any((utcnow()-dt(v['startTime'])).total_seconds()<10 and not v.get('forced_stop') for v in world.experiments.values())
   self.send_response(503 if active else 200);self.end_headers();self.wfile.write(b'{"test_only":true}')
  def log_message(self,*a):pass
 server=ThreadingHTTPServer(('127.0.0.1',0),Handler);threading.Thread(target=server.serve_forever,daemon=True).start()
 with tempfile.TemporaryDirectory() as directory:
  raw=config_dict.__wrapped__();raw['bindings'][0]['probes'][0]['url']=f'http://127.0.0.1:{server.server_port}/business';raw['bindings'][0]['faults'][0]['max_fault_seconds']=10
  config=Configuration.model_validate(raw);store=Store(directory);service=Service(config,store,aws_factory=factory)
  spec=Experiment(id='worker-real-http',title='Test-only worker and loopback acceptance',binding_id='test-binding',fault_id='bounded-stop',probe_id='get-health',baseline_seconds=30,observation_seconds=60,ingestion_wait_seconds=2,response_deadline_seconds=30,max_error_ratio=.01,max_latency_ms=500,stable_seconds=10,bucket_seconds=5,hypotheses='Exercise the actual scheduler, HTTP measurements and durable phases with a test-only provider.',oracle={'mechanism_code':'capacity_loss','mechanism_description':'A test fixture makes the loopback business path unavailable.','affected_resource_arns':[TARGET],'required_checks':['fault-present'],'rubric':'Test-only expected mechanism; no AWS or agent behavior established.'})
  ref=service.register(spec)['id'];trial=service.trial(TrialRequest(experiment_ref=ref));tid=trial['id']
  worker=Worker(config,store,engine=Engine(config,store,aws_factory=factory));wt=threading.Thread(target=worker.run,daemon=True);wt.start()
  def wait(pred,seconds=140):
   until=time.monotonic()+seconds
   while time.monotonic()<until:
    if pred():return
    time.sleep(.15)
   raise AssertionError('Timed out: '+json.dumps(store.entity(tid)))
  try:
   service.qualify(tid);wait(lambda:store.entity(tid)['state']=='READY',15);approve(service,tid);service.start(tid)
   wait(lambda:store.entity(tid)['state']=='OBSERVING',50)
   check('real worker established a healthy baseline before provider exposure',bool(store.entity(tid)['data'].get('baseline_record_id')))
   wait(lambda:any(not p['success'] for p in store.probes(tid)),15)
   check('HTTP requests actually observed an induced loopback failure',any(p.get('status')==503 for p in store.probes(tid)))
   first_id=store.entity(tid)['data']['fis_id']
   worker.stop();wt.join(15)
   check('first worker released its local ownership lock',not wt.is_alive())
   worker=Worker(config,Store(directory),engine=Engine(config,Store(directory),aws_factory=factory));wt=threading.Thread(target=worker.run,daemon=True);wt.start()
   wait(lambda:store.entity(tid)['state'] in {'CLOSED','CLOSED_ABORTED','RESTORE_REQUIRED'},100)
   t=store.entity(tid)
   check('replacement worker resumed the persisted experiment identity',t['data']['fis_id']==first_id)
   check('provider start was dispatched once',sum(w[2]=='start_experiment' for w in world.writes)==1)
   check('actual loopback requests recovered',any(p.get('status')==200 and dt(p['scheduled_at'])>dt(t['data']['exposure_at']) for p in store.probes(tid)))
   check('independent fixture cleanup completed',t['data']['cleanup_verified'] and t['state']=='CLOSED')
   check('trial produced a pinned assessment and immutable probe capture',bool(store.record(t['data']['assessment_id'])['data']['probe_capture_id']))
   check('requests were measured rather than preloaded',len(store.probes(tid))>=70 and all(p.get('response_sha256') for p in store.probes(tid) if p.get('status')))
  finally:worker.stop();wt.join(15);server.shutdown();server.server_close()
 report={'passed':len(checks),'checks':checks,'workload':'Actual bounded HTTP requests against an ephemeral local test server','provider':'test-only in-memory AWS/agent double','worker_restart':'Worker owner replacement with reopened SQLite; not an AWS or container restart test','live_aws_tested':False}
 dest=Path(__file__).resolve().parents[1]/'validation/worker-http-review.json';dest.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2),flush=True)
if __name__=='__main__':main()
