"""Deterministic checks of collected business and collateral metric windows.

These checks evaluate the configured measurement, not the truth of an arbitrary
metric name. A reconciliation metric's producer and denominator need independent
acceptance. No observations are synthesized or carried forward.
"""
from __future__ import annotations
import math
from .util import dt


def evaluate(requirements,observation,*,closed,source_id=None):
    available={m['id']:m for m in observation.get('metrics',[])}
    checks=[]
    for r in requirements:
        metric=available.get(r.metric_id);observed=None
        outcome='inconclusive';reason='The required metric or complete closed-window evidence is missing.'
        values=[]
        if metric:
            values=[p.get('value') for p in metric.get('points',[])]
        valid=(closed and observation.get('complete') is True and metric and metric.get('complete') is True
               and metric.get('missing')==0 and len(values)>=r.minimum_samples
               and all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in values))
        if valid:
            observed={'maximum':max,'minimum':min,'sum':sum,'last':lambda xs:xs[-1]}[r.aggregation](values)
            passed=observed<=r.threshold if r.operator=='lte' else observed>=r.threshold if r.operator=='gte' else observed==r.threshold
            outcome='pass' if passed else 'fail'
            reason='Collected '+r.aggregation+' '+str(observed)+' '+r.operator+' '+str(r.threshold)+'.'
        checks.append({'id':r.id,'metric_id':r.metric_id,'category':r.category,'outcome':outcome,
            'observed':observed,'threshold':r.threshold,'operator':r.operator,'aggregation':r.aggregation,
            'sample_count':len(values),'reason':reason,'interpretation':r.interpretation,'source_record_id':source_id})
    dimensions={}
    for category in ('data_correctness','collateral_regression','application'):
        selected=[c for c in checks if c['category']==category]
        outcomes={c['outcome'] for c in selected}
        outcome='fail' if 'fail' in outcomes else 'inconclusive' if 'inconclusive' in outcomes else 'pass' if selected else 'not_assessed'
        dimensions[category]={'outcome':outcome,'reason':'Configured business checks only; absence is not proof of correctness.',
                             'source_record_ids':[source_id] if source_id and selected else []}
    return checks,dimensions
