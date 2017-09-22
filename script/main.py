import utils
from vision import *
from loggings import *

''' set up logging:'''
lgs = get_logging_groups()
lgs['Default'] = (ECHO,"../log/",None)
lgs['CV'] = (ECHO,"../log/",None)
set_logging_groups(lgs)
''''''

screen = Screen("test",savefile=1,log_groups=['Default','CV'])
screen.loggings.log('hello world')
screen.sample(utils.get_str_time)
screen.loggings.log('complete picture sampling')
