#!/usr/bin/env python3
"""readers_writers - Readers-writers synchronization."""
import sys, threading, time, random
class ReadWriteLock:
    def __init__(self):
        self.readers=0; self.lock=threading.Lock(); self.write_lock=threading.Lock()
    def read_acquire(self):
        with self.lock:
            self.readers+=1
            if self.readers==1: self.write_lock.acquire()
    def read_release(self):
        with self.lock:
            self.readers-=1
            if self.readers==0: self.write_lock.release()
    def write_acquire(self): self.write_lock.acquire()
    def write_release(self): self.write_lock.release()
def simulate(n_readers=3, n_writers=2):
    rw=ReadWriteLock(); data=[0]; log_lock=threading.Lock()
    def reader(rid):
        for _ in range(3):
            rw.read_acquire()
            with log_lock: print(f"  Reader {rid} reads: {data[0]}")
            time.sleep(random.uniform(0.01,0.03)); rw.read_release()
            time.sleep(random.uniform(0.01,0.02))
    def writer(wid):
        for _ in range(2):
            rw.write_acquire()
            data[0]+=1
            with log_lock: print(f"  Writer {wid} writes: {data[0]}")
            time.sleep(random.uniform(0.01,0.03)); rw.write_release()
            time.sleep(random.uniform(0.01,0.02))
    threads=[]
    for i in range(n_readers): threads.append(threading.Thread(target=reader,args=(i,)))
    for i in range(n_writers): threads.append(threading.Thread(target=writer,args=(i,)))
    for t in threads: t.start()
    for t in threads: t.join(timeout=10)
    print(f"Final value: {data[0]}")
if __name__=="__main__": simulate()
