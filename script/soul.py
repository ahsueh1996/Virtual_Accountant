from cortex import Cortex
import time
import utils

class Soul(Cortex):
    def __init__(self,logging_groups=['Default','Cortex']):
        Cortex.__init__(self,'SOUL',logging_groups)
        
        # The following is parsing the defines.txt to get the app specific data
        defines = utils.parse_defines(utils.read_txt("../database/cortex/soul.txt"))
        self.delay = eval(defines['delay'])
        
    def fire(self,data):
        self.loggings.log('Fired; sleeping 5s')
        time.sleep(self.delay)
        self.loggings.log('Publish')
        self.skull.publish(self.name,None)
    
        
    