from loggings import *
''' set up logging:'''
lgs = get_logging_groups()
lgs['Default'] = (ECHO,"../log/",None)
lgs['CV'] = (ECHO,"../log/",None)
set_logging_groups(lgs)
''''''

from vision import *
''' set up i/o '''
screen = Screen('Primary')
''''''

from cortex import Skull
from soul import *
from collector import *
''' set up cortex and skull'''
collector = Collector(screen)
skull = Skull([Soul(),collector])
collector.subscribe(['SOUL'])
''''''



''' RUN '''
skull.operate()
'''''''