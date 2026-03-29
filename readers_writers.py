#!/usr/bin/env python3
"""Readers-writers problem — multiple concurrent readers, exclusive writer."""
import threading, time, random, sys

class ReadWriteLock:
    def __init__(self):
        self.readers = 0
        self.lock = threading.Lock()
        self.write_lock = threading.Lock()
    def read_acquire(self):
        with self.lock:
            self.readers += 1
            if self.readers == 1: self.write_lock.acquire()
    def read_release(self):
        with self.lock:
            self.readers -= 1
            if self.readers == 0: self.write_lock.release()
    def write_acquire(self):
        self.write_lock.acquire()
    def write_release(self):
        self.write_lock.release()

if __name__ == "__main__":
    rwl = ReadWriteLock()
    data = [0]
    log = []
    def reader(rid, n):
        for _ in range(n):
            rwl.read_acquire()
            val = data[0]
            log.append(f"R{rid} read {val}")
            time.sleep(random.uniform(0.01, 0.03))
            rwl.read_release()
    def writer(wid, n):
        for i in range(n):
            rwl.write_acquire()
            data[0] += 1
            log.append(f"W{wid} wrote {data[0]}")
            time.sleep(random.uniform(0.02, 0.05))
            rwl.write_release()
    threads = []
    for i in range(4): threads.append(threading.Thread(target=reader, args=(i, 5)))
    for i in range(2): threads.append(threading.Thread(target=writer, args=(i, 3)))
    for t in threads: t.start()
    for t in threads: t.join()
    print(f"Operations: {len(log)}")
    print(f"Final value: {data[0]}")
    for entry in log[-10:]: print(f"  {entry}")
