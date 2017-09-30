from cortex import Cortex
import time

class Soul(Cortex):
    def __init__(self):
        Cortex.__init__(self,'SOUL')
        
    def fire(self,data):
        print('fire soul')
        time.sleep(10)
        self.skull.publish(self.name,None)
    
        
    