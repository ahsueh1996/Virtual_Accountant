from loggings import *
from programs import *

class Messenger(Loggable):
    def __init__(self, logging_groups):
        Loggable.__init__(self, logging_groups)
        self.class_name = "Messenger"
        self.loggings.set_obj_id(self.class_name)
        self.program = None
    
    def open(self):
        pass
        
    def identify_conversations(self):
        pass
    
    def identify_messages(self):
        pass
    
    def close(self):
        pass

class GroupMe_Web(Messenger):
    def __init__(self,logging_groups = ['Default']):
        Messenger.__init__(self, logging_groups)
        self.class_name += ".GroupMe_Web"
        self.loggings.set_obj_id(self.class_name)
        self.program = Chrome()
        
    def open(self):
        self.program.open("groupme.com")
        time.sleep(3)
    
    def close(self):
        self.program.close()
