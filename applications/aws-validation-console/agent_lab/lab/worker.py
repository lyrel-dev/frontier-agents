"""Single local owner, durable phase processing, independent bounded probe thread."""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import fcntl
import os
import threading
import time
from .engine import Engine, PROBING
from .fis_campaigns import Fleet
from .models import Configuration
from .probe import request
from .util import iso, dt, error_code


class Worker:
    def __init__(self,config:Configuration,store,*,engine=None):
        from .setup import refresh
        refresh(config,store)
        self.config=config; self.store=store; self.engine=engine or Engine(config,store)
        self.fleet=Fleet(config,store)
        self.stop_event=threading.Event(); self.owner=None; self.thread=None
        self.background_thread=None; self.failure=None; self.probe_failure=None
        self.started=threading.Event(); self.finished=threading.Event()

    def acquire(self):
        self.owner=open(self.store.directory/'worker.lock','a+')
        os.chmod(self.store.directory/'worker.lock',0o600)
        try: fcntl.flock(self.owner,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:
            self.owner.close(); self.owner=None
            raise RuntimeError('A worker already owns this local workspace') from None

    def release(self):
        if self.owner:
            fcntl.flock(self.owner,fcntl.LOCK_UN); self.owner.close(); self.owner=None

    def _probes(self):
        pending=set(); schedules={}
        with ThreadPoolExecutor(max_workers=4,thread_name_prefix='real-probe') as pool:
            while not self.stop_event.is_set():
                for future in list(pending):
                    if future.done():
                        tid,result=future.result(); self.store.probe(tid,result); pending.remove(future)
                active=[t for t in self.store.entities('trial') if t['state'] in PROBING and t['data'].get('started_at')]
                for trial in active:
                    tid=trial['id']; spec,binding,fault,probe=self.engine.instruments(trial)
                    # Do not continue local traffic beyond a finite wall deadline
                    # even while a remote operation is unresolved.
                    maximum=spec.baseline_seconds+spec.observation_seconds+fault.max_fault_seconds+spec.ingestion_wait_seconds+900
                    if time.time()>dt(trial['data']['started_at']).timestamp()+maximum: continue
                    interval=1/probe.requests_per_second
                    if tid not in schedules:
                        previous=self.store.probes(tid)
                        schedules[tid]=dt(previous[-1]['scheduled_at']).timestamp()+interval if previous else dt(trial['data']['started_at']).timestamp()
                    current=time.time(); scheduled=schedules[tid]
                    if scheduled>current: continue
                    # One bounded discontinuity record, not millions of invented
                    # failed requests after a restart. The evaluator sees the gap.
                    if current-scheduled>self.config.probe_gap_seconds:
                        self.store.put_record('worker_gap',tid,{'from':iso(datetime.fromtimestamp(scheduled,timezone.utc)),
                                        'to':iso(),'instrument':'probe-scheduler'})
                        scheduled=current; schedules[tid]=current
                    stamp=iso(datetime.fromtimestamp(scheduled,timezone.utc))
                    lag=current-scheduled
                    if len(pending)>=4:
                        self.store.probe(tid,{'scheduled_at':stamp,'at':iso(),'probe_id':probe.id,'attempted':False,'missed':True,'success':False,'latency_ms':None,'scheduling_lag_seconds':lag})
                    else:
                        def run(identifier=tid,specification=probe,at=stamp,delay=lag):
                            result=request(specification,at); result['scheduling_lag_seconds']=round(delay,4)
                            return identifier,result
                        pending.add(pool.submit(run))
                    schedules[tid]=scheduled+interval
                self.stop_event.wait(.05)
            for future in pending:
                tid,result=future.result(); self.store.probe(tid,result)

    def _probe_loop(self):
        try:
            self._probes()
        except Exception as exc:
            self.probe_failure=error_code(exc)
            self.stop_event.set()

    def _run_owned(self):
        """Keep the workspace lock until the engine and all probe work drain."""
        try:
            self.thread=threading.Thread(target=self._probe_loop,daemon=True,name='probe-scheduler')
            self.thread.start()
            self.store.meta('worker',{'pid':os.getpid(),'heartbeat_at':iso(),'state':'running'})
            self.started.set()
            while not self.stop_event.is_set():
                if not self.thread.is_alive():
                    raise RuntimeError('Probe scheduler stopped unexpectedly')
                self.store.meta('worker',{'pid':os.getpid(),'heartbeat_at':iso(),'state':'running'})
                from .setup import refresh
                refresh(self.config,self.store)
                self.engine.step()
                self.fleet.step()
                self.store.meta('worker',{'pid':os.getpid(),'heartbeat_at':iso(),'state':'running'})
                self.stop_event.wait(self.fleet.poll_delay())
            if self.probe_failure:
                raise RuntimeError('Probe scheduler failed')
        except Exception as exc:
            self.failure=error_code(exc)
            raise
        finally:
            self.stop_event.set()
            # A timeout here would release ownership while requests could still
            # write evidence. The process supervisor applies the shutdown budget.
            try:
                if self.thread and self.thread.ident is not None:
                    self.thread.join()
                if self.probe_failure and not self.failure:
                    self.failure=self.probe_failure
                self.store.meta('worker',{'pid':os.getpid(),'heartbeat_at':iso(),
                    'state':'failed' if self.failure else 'stopped',
                    **({'error_code':self.failure} if self.failure else {})})
            finally:
                self.release()
                self.finished.set()

    def run(self):
        self.acquire()
        self._run_owned()

    def start_background(self, timeout=5):
        """Acquire synchronously: a duplicate owner must fail before HTTP starts."""
        if self.background_thread is not None or self.owner is not None or self.stop_event.is_set():
            raise RuntimeError('Worker instance cannot be started twice')
        self.acquire()
        def background():
            try:
                self._run_owned()
            except Exception:
                # Failure is retained in worker metadata and observed by run.py.
                pass
        self.background_thread=threading.Thread(target=background,name='experiment-worker',daemon=True)
        try:
            self.background_thread.start()
        except Exception:
            self.release()
            raise
        deadline=time.monotonic()+timeout
        while not self.started.is_set() and not self.finished.is_set() and time.monotonic()<deadline:
            self.started.wait(.01)
        if not self.started.is_set() or self.failure or not self.background_thread.is_alive():
            self.stop()
            self.background_thread.join(timeout=timeout)
            raise RuntimeError('Experiment worker did not start successfully')
        return self.background_thread

    def stop(self):
        self.stop_event.set()
