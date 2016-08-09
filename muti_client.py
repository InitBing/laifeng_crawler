#! /usr/bin/env python
# coding:utf-8
# author:wenhui

import client22
import grnumber
import threading
import multiprocessing
import time
import signal


global running_room

rinning_room=[]

def multi_run ():
   num_list=grnumber.get_room_num()
   fp = open('output','w')
   global worker_list
   worker_list = []
   for roomid in num_list:
	    p = multiprocessing.Process(target=client22.run,args=(int(roomid[0]),fp))
	    p.name = "%  room charting info" % roomid[0]
	    worker_list.append(p)

   for worker in worker_list:
      worker.start()

   for worker in worker_list:
      worker.join()
   global running_room

   for worker in worker_list:
      if (worker.is_alive()==True):
        running_room.append(worker.name)


def get_processing_room_num():
    global running_room
    for item in running_room:
      print "item.name\n"
    

















