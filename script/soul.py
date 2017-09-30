from cortex import Cortex
import time

class Soul(Cortex):
    def __init__(self,logging_groups=['Default','Cortex']):
        Cortex.__init__(self,'SOUL',logging_groups)
        
    def fire(self,data):
        self.loggings.log('Fired; sleeping 10s')
        time.sleep(10)
        self.loggings.log('Publish')
        self.skull.publish(self.name,None)
    
        
    