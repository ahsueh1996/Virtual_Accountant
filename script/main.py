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
img = screen.read_img("../database/programs/groupme_web/test.PNG")
screen.show_img(img)