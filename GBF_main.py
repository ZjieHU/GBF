#-*- coding:utf8 -*- 

import requests
import threading
import Queue
import sys
import multiprocessing 
import os
import time

reload(sys)
sys.setdefaultencoding('utf8')

work = Queue.Queue()
muxlock = threading.Lock()


class GBF(object): 

    def __init__(self): 
        self.process_count=0
        self.thread_count=0
        self.target=None


    def run_process(self): 
        process = []
        for i in range(self.process_count): 
            p = multiprocessing.Process(target=self.run_thread, args=())
            process.append(p)
        print 'create process count is %s' % self.process_count
        for p in process:
            p.start()
        for p in process: 
            p.join()
        

    def run_thread(self): 
        threads = []
        for i in range(0, self.thread_count): 
            t = threading.Thread(target=self.target, args=())
            threads.append(t)
        print 'create thread count is %s' % self.thread_count
        for t in threads: 
            t.start()
        for t in threads: 
            t.join()
        

def ach_work():
    global muxlock
    try:
        muxlock.acquire()
        if work.qsize() > 0: 
            return work.get()
        else:
            return '0'
    except Exception as e:
        pass
    finally: 
        muxlock.release()


def run(): 
    while 1: 
        i = ach_work()
        time.sleep(1)
        if i == '0': 
            break
    print 'pid is %s , %s' % (os.getpid(), 'end')

if __name__ == '__main__': 
    for i in range(0,100): 
        work.put(str(i))
    pro = GBF()
    pro.process_count = 10
    pro.thread_count = 10
    pro.target = run
    pro.run_process()