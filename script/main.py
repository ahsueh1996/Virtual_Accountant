from loggings import *
''' set up logging:'''
lgs = get_logging_groups()
lgs['Default'] = (OFF,"../log/",None)
lgs['Vision'] = (OFF,"../log/",None)
lgs['Cortex'] = (ECHO,"../log/",None)
set_logging_groups(lgs)
''''''

from vision import *
''' set up i/o '''
screen = Screen('Primary', ['Default','Vision'])
''''''

from cortex import Skull
from soul import *
from collector import *
''' set up cortex and skull'''
collector = Collector(screen)
cortex_list = [Soul(),collector]
skull = Skull(cortex_list)
for each in cortex_list:
    each.set_skull(skull)
collector.subscribe(['SOUL'])
''''''

''' RUN '''
skull.operate()
''''''