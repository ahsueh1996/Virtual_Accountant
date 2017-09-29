import utils

class Cortex():
    def __init__(self,name):
        self.subscriptions = []
        self.skull = None
        self.name = name
    
    def fire(self,data):
        ''' Cortex specific function '''
        pass
    
    def set_skull(self, skull):
        self.skull = skull
    
    def publish(self,data = None):
        ''' When cortex fired and has results, publish through the server or
        the "skull". '''
        self.skull.publish(self.name,data)
    
    def subscribe(self,array):
        ''' Subcribe to other cortexes and get their results automatically.
        The skull will fire the subscriber's cortex when their subscriptions
        receive updates'''
        self.subscriptions += array
        self.skull.subscribe(self.name,array)

import numpy as np
import queue

class Skull():
    ''' The skull is the pub/sub server for the cortexes. Build the cortex first
    then inject them into the skull. When this happens, the skull will also update
    the cortex's skull pointer.
    The pubsub_matrix is a 2d matrix that reads publisher to subscribers (row/col).
    When a cortex publishes info, its subscribers (as recored in the row) will get
    their own threads to fire. We assume that the subscribers can fire in parallel
    to one another for now. The publishments are FIFO queued.
    
    The one necessary cortex is the "SOUL". It's function can be defined by the user
    but it is the cortext that functions when all other cortexes are idle. It is
    something like the root node, the daydreamer, the associator/simulatior, the
    hardware interrupter.'''
    def __init__(self,cortexes):
        self.cortexes = cortexes
        self.namemap = {} # maps cortex names to indicies
        for i,each in enumerate(cortexes):
            self.namemap[each.name] = i
            each.set_skull = self
        self.soul = cortexes[self.namemap['SOUL']]
        self.pubsub_matrix = np.zeros((i+1,i+1)) # row (pub): col (sub)
        self.publish_queue = queue.Queue()
        self.alive = True
    
    def operate(self):
        ''' operation loop. As long as people are publishing, we will continue to allow
        subscribers to fire. If the skull dies though, the process is over'''
        while self.alive:
            if self.publish_queue.empty():
                self.soul.fire(None)
            else:
                pub,data = self.publish_queue.get()
                pub = self.namemap[pub]
                subs = self.pubsub_matrix[pub]  # array of subscribers
                for i,each in enumerate(subs):
                    if each == 1:
                        self.cortexes[i].fire(data)
    
    def kill(self):
        utils.T_LOCK.acquire()
        self.alive = False
        utils.T_LOCK.release()
    
    def publish(self,name,data):
        self.publish_queue.put((name,data))
    
