import utils
''' 
OFF - nothing is logged
QUIET - things are logged to file
ECHO - console output during runtime
FILING - ECHO and saves to file during runtime
'''
OFF, QUIET, ECO, ECHO, FILING = (0,1,2,3,4)

''' This dict contains triplets of mode and filepath and history keyed by
strings (aka group). The purpose is so that multiple loggers can log to the 
same file or echo the the console.
= {'Default': (ECHO,"../log",fileobj), ...}
'''
logging_groups = {"Default": (ECHO,"../log/",None)}

def set_logging_groups(lgs):
    ''' file objs are inferred based on the logging group name and the path'''
    global logging_groups
    for key in lgs:
        if lgs[key][0] == ECHO:
            continue
        lgs[key] = (lgs[key][0],lgs[key][1],utils.mktxt(lgs[key][1],key+".txt"))
    logging_groups = lgs

def get_logging_groups():
    global logging_groups
    return logging_groups

class Logger():
    def __init__(self,names):
        global logging_groups
        self.names = names
        self.obj_id = "unknown"
        self.files = []
        self.modes = []
        # we assume that the logging group is predefined by someone else!!
        for name in names:
            mode, _, file = logging_groups[name]
            self.files.append(file)
            self.modes.append(mode)
    
    def set_obj_id(self,id):
        self.obj_id = id
    
    def log(self,msg):
        for i,name in enumerate(self.names):
            mode = self.modes[i]
            if mode == OFF:
                continue
            new_msg = name + " log in " + self.obj_id + ":\t" + msg
            if mode == ECHO or mode == FILING:
                self.echo(new_msg)
            if mode == QUIET or mode == FILING:
                self.quiet(i,new_msg)
            
    def echo(self,msg):
        utils.print_with_time(msg)
        
    def quiet(self,i,msg):
        utils.write_2_file(self.files[i],msg)

class Loggable():
    def __init__(self, logging_groups):
        self.loggings = Logger(logging_groups)
