/* AWS Health demo selectors. No function mutates provider records or workflow state.
 * Public API:
 * - eventRows: array; contexts are account-filtered, with summaryContexts separate.
 *   A status filter qualifies an event when any selected context matches; it does
 *   not replace the other selected account states. `mixed` is a local rollup.
 * - lifecycleRows: array of exposure rows AND unmatched inventory rows; riskStatus
 *   is overdue | due_soon | planned | unknown, using only meta.asOf.
 * - serviceMatrix: array { service, cells: [{ region, state, events, coverage }] }.
 * - coverageSummary: issues/records are coverage records, complete/total numbers.
 * - validateData: array of human-readable errors; [] means valid.
 */
(function (root) {
  'use strict';

  const DAY = 86400000;
  const DEFAULT_FILTERS = Object.freeze({ q: '', account: 'all', region: 'all', category: 'all', scope: 'all', status: 'all', actionability: 'all' });
  const list = value => Array.isArray(value) ? value : [];
  const index = values => new Map(list(values).map(value => [value.id, value]));
  const present = value => value !== null && value !== undefined && value !== '';
  const text = value => value === null || value === undefined ? '' : String(value);
  const lower = value => text(value).toLowerCase();
  const unique = values => [...new Set(values.filter(present))];
  const byIdentity = (values, key) => [...new Map(values.map(value => [key(value), value])).values()];
  const filtersOf = filters => Object.assign({}, DEFAULT_FILTERS, filters || {});
  const isAll = value => !present(value) || lower(value) === 'all';
  const eq = (left, right) => lower(left) === lower(right);
  const actionClass = value => ({ action_required: 'required', action_may_be_required: 'may_required', informational: 'informational' }[lower(value)] || lower(value));
  const latest = values => values.filter(value => present(value) && Number.isFinite(Date.parse(value))).sort((a, b) => Date.parse(b) - Date.parse(a))[0] || null;
  const searchable = values => values.flat(Infinity).filter(present).map(value => typeof value === 'object' ? JSON.stringify(value) : text(value)).join(' ').toLowerCase();
  const includesQuery = (query, values) => !text(query).trim() || text(query).trim().toLowerCase().split(/\s+/).every(term => searchable(values).includes(term));

  function lookups(data) {
    return {
      accounts: index(data.accounts), events: index(data.events), contexts: index(data.contexts),
      resources: index(data.resources), entities: index(data.entities),
      entries: index(data.catalogEntries), milestones: index(data.milestones),
      deployments: index(data.deployments), exposures: index(data.exposures)
    };
  }

  function matchesValue(filter, value) {
    if (isAll(filter)) return true;
    if (['unsupplied', 'not_supplied', 'missing'].includes(lower(filter))) return !present(value);
    return eq(filter, value);
  }

  function coverageRecords(data, filters, options) {
    const f = filtersOf(filters);
    const opt = options || {};
    return list(data.coverage).filter(record => {
      if (!isAll(f.account) && present(record.accountId) && record.accountId !== f.account) return false;
      if (!isAll(f.region) && present(record.region) && !['all', 'global', '*'].includes(lower(record.region)) && !eq(record.region, f.region)) return false;
      if (opt.accountIds && present(record.accountId) && !opt.accountIds.includes(record.accountId)) return false;
      if (opt.eventIds && present(record.eventId) && !opt.eventIds.includes(record.eventId)) return false;
      if (opt.publicOnly && present(record.accountId)) return false;
      return true;
    });
  }

  function summarizeCoverage(records, accounts) {
    const complete = records.filter(record => record.status === 'complete').length;
    let state = 'unknown';
    if (records.length) {
      if (records.every(record => record.status === 'unavailable')) state = 'unavailable';
      else if (records.some(record => ['partial', 'unavailable'].includes(record.status))) state = 'partial';
      else if (records.some(record => record.status === 'stale')) state = 'stale';
      else if (complete === records.length) state = 'complete';
    }
    const selectedAccounts = unique(accounts);
    const accountsComplete = selectedAccounts.filter(accountId => {
      const own = records.filter(record => record.accountId === accountId || (!present(record.accountId) && !present(record.eventId)));
      return own.length && own.every(record => record.status === 'complete');
    }).length;
    return {
      state,
      records: records.slice(),
      issues: records.filter(record => record.status !== 'complete'),
      complete,
      total: records.length,
      accountsComplete,
      accountsTotal: selectedAccounts.length,
      lastCollectedAt: latest(records.map(record => record.lastSuccessAt)),
      missingAccountIds: selectedAccounts.filter(accountId => !records.some(record => record.accountId === accountId || (!present(record.accountId) && !present(record.eventId))))
    };
  }

  function eventRows(data, filters) {
    const f = filtersOf(filters);
    const maps = lookups(data);
    const rows = [];
    for (const event of byIdentity(list(data.events), event => event.eventArn || event.id)) {
      if (!matchesValue(f.region, event.region) || !matchesValue(f.category, event.category) || !matchesValue(f.scope, event.scope)) continue;
      const allContexts = list(data.contexts).filter(context => context.eventId === event.id);
      const summaryContexts = allContexts.filter(context => context.kind === 'ORG_SUMMARY');
      const leafContexts = allContexts.filter(context => context.kind !== 'ORG_SUMMARY' && (isAll(f.account) || context.kind === 'PUBLIC' || context.accountId === f.account));
      // Summaries can explain an organization-level observation. They never add
      // account entities or replace more precise account/public observations.
      const contexts = leafContexts.length ? leafContexts : (isAll(f.account) ? summaryContexts : []);
      if (!contexts.length) continue;
      if (!isAll(f.status) && !contexts.some(context => matchesValue(f.status, context.statusCode))) continue;
      if (!isAll(f.actionability) && !contexts.some(context => matchesValue(f.actionability, context.actionability) || (present(context.actionability) && actionClass(f.actionability) === actionClass(context.actionability)))) continue;
      const contextIds = new Set(contexts.filter(context => context.kind !== 'ORG_SUMMARY').map(context => context.id));
      const entities = byIdentity(list(data.entities).filter(entity => contextIds.has(entity.contextId)), entity => entity.id).map(entity => {
        const context = maps.contexts.get(entity.contextId);
        return Object.assign({}, entity, {
          context,
          account: context && context.kind === 'ACCOUNT' ? maps.accounts.get(context.accountId) || null : null,
          resource: entity.resourceId ? maps.resources.get(entity.resourceId) || null : null
        });
      });
      const accounts = unique(contexts.filter(context => context.kind === 'ACCOUNT').map(context => context.accountId)).map(id => maps.accounts.get(id) || { id, name: id });
      if (!includesQuery(f.q, [event.title, event.summary, event.eventArn, event.service, event.typeCode, event.category, event.region,
        accounts.map(account => [account.id, account.name, account.owner]),
        entities.map(entity => [entity.entityValue, entity.healthEntityArn, entity.resource && [entity.resource.name, entity.resource.workload, entity.resource.owner]]),
        contexts.map(context => context.description)])) continue;
      const statusCounts = { open: 0, upcoming: 0, closed: 0, unsupplied: 0 };
      for (const context of contexts) {
        const status = present(context.statusCode) ? context.statusCode : 'unsupplied';
        statusCounts[status] = (statusCounts[status] || 0) + 1;
      }
      const statuses = unique(contexts.map(context => present(context.statusCode) ? context.statusCode : 'unsupplied'));
      const actions = unique(contexts.map(context => context.actionability));
      const actionability = actions.find(action => actionClass(action) === 'required') || actions.find(action => actionClass(action) === 'may_required') || (actions.length === 1 ? actions[0] : actions.length ? 'mixed' : null);
      const countStatus = status => entities.filter(entity => entity.statusCode === status).length;
      const coverage = summarizeCoverage(coverageRecords(data, { account: f.account, region: event.region }, {
        accountIds: accounts.map(account => account.id), eventIds: [event.id], publicOnly: contexts.every(context => context.kind === 'PUBLIC')
      }), accounts.map(account => account.id));
      rows.push(Object.assign({}, event, {
        contexts,
        summaryContexts: isAll(f.account) ? summaryContexts : [],
        accounts,
        entities,
        status: statuses.length > 1 ? 'mixed' : statuses[0] === 'unsupplied' ? null : statuses[0],
        statusIsDerived: statuses.length > 1,
        statusCounts,
        actionability,
        actionabilityValues: actions,
        personas: unique(contexts.flatMap(context => list(context.personas))),
        updatedAt: latest(contexts.map(context => context.lastUpdatedTime)),
        impairedCount: countStatus('IMPAIRED'),
        pendingCount: countStatus('PENDING'),
        unknownCount: countStatus('UNKNOWN'),
        unsuppliedCount: entities.filter(entity => !present(entity.statusCode)).length,
        entityCount: entities.length,
        mappedResourceCount: unique(entities.filter(entity => entity.resource).map(entity => entity.resourceId)).length,
        coverage
      }));
    }
    return rows;
  }

  function metrics(data, filters) {
    const rows = eventRows(data, filters);
    const entities = byIdentity(rows.flatMap(row => row.entities), entity => entity.id);
    return {
      events: unique(rows.map(row => row.eventArn || row.id)).length,
      openIssues: rows.filter(row => row.category === 'issue' && row.contexts.some(context => context.statusCode === 'open')).length,
      affectedAccounts: unique(rows.flatMap(row => row.accounts.map(account => account.id))).length,
      impairedEntities: entities.filter(entity => entity.statusCode === 'IMPAIRED').length,
      pendingEntities: entities.filter(entity => entity.statusCode === 'PENDING').length,
      reportedEntities: entities.length,
      mappedResources: unique(entities.filter(entity => entity.resource).map(entity => entity.resourceId)).length,
      unknownEntities: entities.filter(entity => entity.statusCode === 'UNKNOWN').length,
      unsuppliedEntities: entities.filter(entity => !present(entity.statusCode)).length,
      actionRequiredEvents: rows.filter(row => row.contexts.some(context => actionClass(context.actionability) === 'required')).length
    };
  }

  function coverageSummary(data, filters) {
    const f = filtersOf(filters);
    const eventIds = eventRows(data, f).map(event => event.id);
    const accounts = list(data.accounts).filter(account => isAll(f.account) || account.id === f.account).map(account => account.id);
    return summarizeCoverage(coverageRecords(data, f, { eventIds }), accounts);
  }

  function lifecycleRows(data, filters) {
    const f = filtersOf(filters);
    const maps = lookups(data);
    const asOf = Date.parse(data.meta && data.meta.asOf);
    const rows = [];
    const representedDeployments = new Set();
    function append(exposure, deployment) {
      if (!deployment) return;
      const resource = maps.resources.get(deployment.resourceId) || null;
      const account = resource ? maps.accounts.get(resource.accountId) || null : null;
      const milestone = exposure ? maps.milestones.get(exposure.milestoneId) || null : null;
      const entry = milestone ? maps.entries.get(milestone.entryId) || null : null;
      if (!isAll(f.account) && (!resource || resource.accountId !== f.account)) return;
      if (!isAll(f.region) && (!resource || !eq(resource.region, f.region))) return;
      if (!includesQuery(f.q, [resource && [resource.name, resource.service, resource.workload, resource.owner], account && [account.id, account.name],
        deployment.component, deployment.version, entry && [entry.title, entry.service, entry.version, entry.recommendedVersion], milestone && [milestone.type, milestone.description], exposure && exposure.reason])) return;
      const deadline = milestone && milestone.date || null;
      const time = deadline ? Date.parse(deadline) : NaN;
      const daysUntil = Number.isFinite(time) && Number.isFinite(asOf) ? Math.ceil((time - asOf) / DAY) : null;
      const unmatched = !exposure;
      const confirmed = exposure && exposure.applicability === 'confirmed' && deployment.matchStatus !== 'unmatched';
      const riskStatus = !confirmed || daysUntil === null ? 'unknown' : daysUntil < 0 ? 'overdue' : daysUntil <= 30 ? 'due_soon' : 'planned';
      rows.push(Object.assign({}, exposure || {}, {
        id: exposure ? exposure.id : 'unmatched:' + deployment.id,
        exposureId: exposure ? exposure.id : null,
        deploymentId: deployment.id,
        resourceId: resource && resource.id,
        milestoneId: milestone && milestone.id,
        entryId: entry && entry.id,
        deployment, resource, account, milestone, entry, catalogEntry: entry,
        service: resource && resource.service || entry && entry.service || null,
        region: resource && resource.region || null,
        component: deployment.component,
        version: deployment.version,
        recommendedVersion: entry && entry.recommendedVersion || null,
        milestoneType: milestone && milestone.type || null,
        deadline, daysUntil, riskStatus, unmatched,
        applicability: exposure ? exposure.applicability : 'unknown',
        reason: exposure ? exposure.reason : 'No verified lifecycle catalog match for this inventory observation.',
        confidence: exposure ? exposure.confidence : null,
        observedAt: deployment.observedAt
      }));
    }
    for (const exposure of list(data.exposures)) {
      representedDeployments.add(exposure.deploymentId);
      append(exposure, maps.deployments.get(exposure.deploymentId));
    }
    // Unmatched inventory is visible as unknown; absence of a catalog match is
    // not evidence of support, non-support, or a healthy asset. Matched versions
    // without an applicable modeled milestone remain in inventory, not this risk list.
    for (const deployment of list(data.deployments)) if (!representedDeployments.has(deployment.id) && deployment.matchStatus !== 'matched') append(null, deployment);
    const order = { overdue: 0, due_soon: 1, unknown: 2, planned: 3 };
    return rows.sort((a, b) => order[a.riskStatus] - order[b.riskStatus] || (a.daysUntil === null ? Infinity : a.daysUntil) - (b.daysUntil === null ? Infinity : b.daysUntil) || a.id.localeCompare(b.id));
  }

  function workRows(data, workItems, filters) {
    const f = filtersOf(filters);
    const maps = lookups(data);
    const visibleEvents = new Map(eventRows(data, Object.assign({}, f, { q: '' })).map(event => [event.id, event]));
    const eventFilters = ['category', 'scope', 'status', 'actionability'].some(key => !isAll(f[key]));
    const result = [];
    for (const item of list(workItems === undefined ? data.workItems : workItems)) {
      const allTargets = list(data.workItemTargets).filter(target => target.workItemId === item.id).map(target => {
        const impact = target.impactId ? maps.entities.get(target.impactId) || null : null;
        const context = maps.contexts.get(target.contextId || impact && impact.contextId) || null;
        const exposure = target.exposureId ? maps.exposures.get(target.exposureId) || null : null;
        const deployment = exposure ? maps.deployments.get(exposure.deploymentId) || null : null;
        const milestone = exposure ? maps.milestones.get(exposure.milestoneId) || null : null;
        const entry = milestone ? maps.entries.get(milestone.entryId) || null : null;
        const event = context ? maps.events.get(context.eventId) || null : null;
        const impacts = impact ? [impact] : context ? list(data.entities).filter(entity => entity.contextId === context.id) : [];
        const resources = byIdentity([
          ...impacts.map(entity => maps.resources.get(entity.resourceId)),
          deployment && maps.resources.get(deployment.resourceId)
        ].filter(Boolean), resource => resource.id);
        return Object.assign({}, target, { impact, impacts, context, event, exposure, deployment, milestone, entry, resources,
          resource: resources.length === 1 ? resources[0] : null });
      });
      const targets = allTargets.filter(target => {
        if (target.event && !visibleEvents.has(target.event.id)) return false;
        if (!target.event && eventFilters) return false;
        if (!isAll(f.account) && target.context && target.context.kind !== 'PUBLIC' && target.context.accountId !== f.account) return false;
        if (!isAll(f.account) && !target.context && !target.resources.some(resource => resource.accountId === f.account)) return false;
        if (!isAll(f.region) && !target.event && !target.resources.some(resource => eq(resource.region, f.region))) return false;
        return true;
      });
      if (!targets.length) continue;
      const resources = byIdentity(targets.flatMap(target => target.resources), resource => resource.id);
      const events = byIdentity(targets.map(target => target.event).filter(Boolean), event => event.eventArn || event.id);
      if (!includesQuery(f.q, [item.title, item.owner, item.state, item.priority, item.notes, events.map(event => [event.title, event.service, event.typeCode]), resources.map(resource => [resource.name, resource.workload, resource.owner])])) continue;
      const impacts = byIdentity(targets.flatMap(target => target.impacts), impact => impact.id);
      result.push(Object.assign({}, item, {
        targets, allTargets, events,
        eventIds: events.map(event => event.id),
        eventArns: events.map(event => event.eventArn),
        resources,
        accounts: unique(targets.flatMap(target => [target.context && target.context.kind === 'ACCOUNT' ? target.context.accountId : null, ...target.resources.map(resource => resource.accountId)])).map(id => maps.accounts.get(id) || { id, name: id }),
        pendingProviderCount: impacts.filter(impact => impact.statusCode === 'PENDING').length,
        impairedProviderCount: impacts.filter(impact => impact.statusCode === 'IMPAIRED').length,
        providerStatuses: unique(impacts.map(impact => impact.statusCode))
      }));
    }
    return result;
  }

  function serviceMatrix(data, filters) {
    const f = filtersOf(filters);
    const rows = eventRows(data, f);
    const resources = list(data.resources).filter(resource => isAll(f.account) || resource.accountId === f.account);
    const declaredRegions = list(data.meta && data.meta.regions).map(region => typeof region === 'string' ? region : region.id || region.name);
    const regions = isAll(f.region) ? unique([...declaredRegions, ...list(data.events).map(event => event.region), ...resources.map(resource => resource.region)]).sort() : [f.region];
    const services = unique([...rows.map(row => row.service), ...resources.map(resource => resource.service)]).sort();
    const selectedAccounts = list(data.accounts).filter(account => isAll(f.account) || account.id === f.account).map(account => account.id);
    return services.map(service => ({
      service,
      cells: regions.map(region => {
        const events = rows.filter(event => event.service === service && eq(event.region, region));
        const active = events.filter(event => event.contexts.some(context => ['open', 'upcoming'].includes(context.statusCode)));
        const coverage = summarizeCoverage(coverageRecords(data, { account: f.account, region }, { eventIds: events.map(event => event.id) }), selectedAccounts);
        const issue = active.some(event => event.category === 'issue' && event.contexts.some(context => context.statusCode === 'open'));
        const change = active.some(event => event.category !== 'issue');
        const state = issue ? 'issue' : change ? 'change' : coverage.state === 'complete' ? 'clear' : 'unknown';
        return {
          service, region, state, events, count: events.length, activeCount: active.length, coverage,
          label: state === 'issue' ? 'Open issue observed' : state === 'change' ? 'Change or notification observed' : state === 'clear' ? 'No open events observed' : 'Collection coverage incomplete'
        };
      })
    }));
  }

  function validateData(data) {
    const errors = [];
    if (!data || typeof data !== 'object') return ['Data must be an object.'];
    const tables = ['accounts', 'events', 'contexts', 'entities', 'resources', 'workItems', 'workItemTargets', 'catalogEntries', 'milestones', 'deployments', 'exposures', 'coverage', 'updates'];
    for (const table of tables) {
      if (!Array.isArray(data[table])) { errors.push(table + ' must be an array.'); continue; }
      const seen = new Set();
      for (const row of data[table]) {
        if (!row || !present(row.id)) { errors.push(table + ': every row requires an id.'); continue; }
        if (seen.has(row.id)) errors.push(table + ': duplicate id ' + row.id + '.');
        seen.add(row.id);
      }
    }
    if (!Number.isFinite(Date.parse(data.meta && data.meta.asOf))) errors.push('meta.asOf must provide the fixed scenario timestamp.');
    const maps = lookups(data);
    const workItems = index(data.workItems);
    function ref(map, id, path) { if (!map.has(id)) errors.push(path + ' references missing id ' + text(id) + '.'); }
    const arns = new Set();
    for (const event of list(data.events)) {
      if (!present(event.eventArn)) errors.push('Event ' + event.id + ' requires its full eventArn identity.');
      else if (arns.has(event.eventArn)) errors.push('Duplicate eventArn ' + event.eventArn + '.');
      arns.add(event.eventArn);
    }
    const keys = new Set();
    for (const context of list(data.contexts)) {
      ref(maps.events, context.eventId, 'Context ' + context.id);
      if (!present(context.contextKey)) errors.push('Context ' + context.id + ' requires a non-null contextKey.');
      const key = [context.eventId, context.kind, context.contextKey].join('|');
      if (keys.has(key)) errors.push('Duplicate event/context identity for ' + context.id + '.');
      keys.add(key);
      if (context.kind === 'ACCOUNT') {
        ref(maps.accounts, context.accountId, 'ACCOUNT context ' + context.id);
        if (present(context.organizationId)) errors.push('ACCOUNT context ' + context.id + ' must not own an organizationId.');
        if (context.contextKey !== context.accountId) errors.push('ACCOUNT context ' + context.id + ' contextKey must equal accountId.');
      } else if (context.kind === 'PUBLIC') {
        if (present(context.accountId) || present(context.organizationId)) errors.push('PUBLIC context ' + context.id + ' must not identify an affected account or organization.');
        if (!eq(context.contextKey, 'PUBLIC')) errors.push('PUBLIC context ' + context.id + ' requires the PUBLIC contextKey.');
      } else if (context.kind === 'ORG_SUMMARY') {
        if (present(context.accountId) || !present(context.organizationId)) errors.push('ORG_SUMMARY context ' + context.id + ' requires only organizationId.');
        if (data.meta && data.meta.organization && context.organizationId !== data.meta.organization.id) errors.push('ORG_SUMMARY context ' + context.id + ' references an unknown organization.');
      } else errors.push('Context ' + context.id + ' has an invalid local kind.');
    }
    const resourceArns = new Set();
    for (const resource of list(data.resources)) {
      ref(maps.accounts, resource.accountId, 'Resource ' + resource.id);
      if (present(resource.arn) && resourceArns.has(resource.arn)) errors.push('Duplicate resource ARN ' + resource.arn + '.');
      resourceArns.add(resource.arn);
    }
    const impacts = new Set();
    for (const entity of list(data.entities)) {
      ref(maps.contexts, entity.contextId, 'Entity ' + entity.id);
      const context = maps.contexts.get(entity.contextId);
      if (context && context.kind === 'ORG_SUMMARY') errors.push('ORG_SUMMARY must not own entity ' + entity.id + '.');
      if (context && present(entity.awsAccountId) && (context.kind !== 'ACCOUNT' || entity.awsAccountId !== context.accountId)) errors.push('Entity ' + entity.id + ' awsAccountId contradicts its context.');
      if (present(entity.resourceId)) {
        ref(maps.resources, entity.resourceId, 'Entity ' + entity.id);
        const resource = maps.resources.get(entity.resourceId);
        if (resource && context && (context.kind !== 'ACCOUNT' || resource.accountId !== context.accountId)) errors.push('Entity ' + entity.id + ' maps to a resource outside its ACCOUNT context.');
      }
      if (present(entity.healthEntityArn)) {
        const key = entity.contextId + '|' + entity.healthEntityArn;
        if (impacts.has(key)) errors.push('Duplicate context/entity identity for ' + entity.id + '.');
        impacts.add(key);
      }
    }
    for (const item of list(data.workItems)) if (!['new', 'acknowledged', 'in_progress', 'completed', 'verified'].includes(item.state)) errors.push('Work item ' + item.id + ' has an invalid local workflow state.');
    for (const target of list(data.workItemTargets)) {
      ref(workItems, target.workItemId, 'Work target ' + target.id);
      const foreignKeys = ['contextId', 'impactId', 'exposureId'].filter(key => present(target[key]));
      if (foreignKeys.length !== 1) errors.push('Work target ' + target.id + ' must reference exactly one context, impact, or exposure.');
      if (present(target.contextId)) ref(maps.contexts, target.contextId, 'Work target ' + target.id);
      if (present(target.impactId)) ref(maps.entities, target.impactId, 'Work target ' + target.id);
      if (present(target.exposureId)) ref(maps.exposures, target.exposureId, 'Work target ' + target.id);
    }
    for (const milestone of list(data.milestones)) ref(maps.entries, milestone.entryId, 'Milestone ' + milestone.id);
    for (const deployment of list(data.deployments)) ref(maps.resources, deployment.resourceId, 'Deployment ' + deployment.id);
    for (const exposure of list(data.exposures)) {
      ref(maps.milestones, exposure.milestoneId, 'Exposure ' + exposure.id);
      ref(maps.deployments, exposure.deploymentId, 'Exposure ' + exposure.id);
    }
    for (const coverage of list(data.coverage)) {
      if (present(coverage.accountId)) ref(maps.accounts, coverage.accountId, 'Coverage ' + coverage.id);
      if (present(coverage.eventId)) ref(maps.events, coverage.eventId, 'Coverage ' + coverage.id);
      if (!['complete', 'partial', 'stale', 'unavailable'].includes(coverage.status)) errors.push('Coverage ' + coverage.id + ' has an invalid local collection status.');
    }
    for (const update of list(data.updates)) {
      if (present(update.eventId)) ref(maps.events, update.eventId, 'Update ' + update.id);
      if (present(update.contextId)) {
        ref(maps.contexts, update.contextId, 'Update ' + update.id);
        const context = maps.contexts.get(update.contextId);
        if (context && present(update.eventId) && context.eventId !== update.eventId) errors.push('Update ' + update.id + ' context belongs to another event.');
      }
    }
    return errors;
  }

  const api = Object.freeze({ DEFAULT_FILTERS, eventRows, metrics, lifecycleRows, coverageSummary, workRows, serviceMatrix, validateData });
  root.HealthDemoModel = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : this);
