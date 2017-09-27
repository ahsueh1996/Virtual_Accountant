from loggings import *
from programs import *

class Messenger(Loggable):
    def __init__(self, logging_groups,screen):
        Loggable.__init__(self, logging_groups)
        self.class_name = "Messenger"
        self.loggings.set_obj_id(self.class_name)
        self.program = None
        self.screen = screen
        self.textbox_cent = (0,0)
    
    def open(self):
        pass
    
    def open_convo(self, name):
        pass
    
    def get_new_msgs(self):
        pass
    
    def send_msg(self,msg):
        ui.click(self.textbox_cent[0],self.textbox_cent[1],clicks=1,button='left')
        ui.typewrite(msg)
        time.sleep(1)
        ui.hotkey('enter')
    
    def close(self):
        pass

class GroupMe_Web(Messenger):
    def __init__(self,logging_groups = ['Default'],screen=None):
        Messenger.__init__(self, logging_groups,screen)
        self.class_name += ".GroupMe_Web"
        self.loggings.set_obj_id(self.class_name)
        self.program = Chrome()
        defines = utils.parse_defines(utils.read_txt("../database/programs/groupme_web/defines.txt"))
        self.convos_pp = utils.parse_pp(defines['convos_pp'])
        self.messages_pp = utils.parse_pp(defines['messages_pp'])
        self.messages_cent = utils.rect_cent_pp(self.messages_pp[0],self.messages_pp[1])
        self.textbox_pp = utils.parse_pp(defines['textbox_pp'])
        self.textbox_cent = utils.rect_cent_pp(self.textbox_pp[0],self.textbox_pp[1])
        self.delay = utils.parse_numbers(defines['delay'])[0]
        self.convo_template = None #screen.cvtPIL2np(screen.read_img('../database/programs/groupme_web/'+defines['convo_template']))
        self.usernames = utils.parse_str(defines['usernames'])
        self.my_username = utils.parse_str(defines['me'])[0]
        self.flag_msg = "Collection"
        
    def open(self):
        self.program.open("groupme.com")
        time.sleep(self.delay)
    
    def close(self):
        self.program.close()
        time.sleep(self.delay)
    
    def open_convo(self, name='Virtual Accountant'):
        loc = self.screen.match_template(self.screen.sample(),self.convo_template)
        ui.click(loc[0]+20, loc[1]+20, clicks=1, button='left')
        time.sleep(self.delay)
    
    def get_new_msgs(self):
        # collection
        # focus on message box
        ui.click(self.messages_cent[0],self.messages_cent[1],clicks=1,button='left')
        # scroll up at least far enough 2 refreshes (5 pg up keys)
        for i in range(2*5):
            ui.hotkey('pgup')
        # select all and copy
        ui.hotkey('ctrl','a')
        ui.hotkey('ctrl','c')
        # send acknowledgement
        self.send_msg(self.flag_msg)
        # destroy window
        time.sleep(10)
        self.close()
        # batch record
        # make raw txt file with notepad to convert it to ASCII encoding while
        # maintaining the original new line characters
        utils.mktxt_notepad('../database/files/$temp.txt')
        # we made sure that this file was not existent before so we expect a create new file prompt from notepad
        ui.hotkey('enter')
        # just in case it exists, paste over everything
        ui.hotkey('ctrl','a')
        ui.hotkey('ctrl','v')
        # read txt and return only the new_msgs as an array of strings
        data = utils.read_txt('../database/files/$temp.txt')
        for i,line in utils.reversed_enumerate(data):
            if line == self.flag_msg and data[i-1] == self.my_username:
                break
        new_msgs = data[i+1:]
        # delete the $temp.txt file for good practice
        utils.cmd_prompt("cd ../database/files & del $temp.txt")
        return new_msgs

gm = GroupMe_Web()
print(gm.get_new_msgs())
