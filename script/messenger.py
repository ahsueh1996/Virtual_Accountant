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
        time.sleep(self.delay)
        ui.typewrite(msg)
        time.sleep(self.delay)
        ui.hotkey('enter')
    
    def close(self):
        pass

class GroupMe_Web(Messenger):
    def __init__(self,screen,logging_groups):
        Messenger.__init__(self, logging_groups,screen)
        self.class_name += ".GroupMe_Web"
        self.loggings.set_obj_id(self.class_name)
        self.program = Chrome()
        
        # The following is parsing the defines.txt to get the app specific data
        defines = utils.parse_defines(utils.read_txt("../database/programs/groupme_web/defines.txt"))
        
        self.messages_pp = utils.parse_pp(defines['messages_pp'])
        self.messages_cent = utils.rect_cent_pp(self.messages_pp[0],self.messages_pp[1])
        
        self.textbox_pp = utils.parse_pp(defines['textbox_pp'])
        self.textbox_cent = utils.rect_cent_pp(self.textbox_pp[0],self.textbox_pp[1])
        
        self.delay = utils.parse_numbers(defines['delay'])[0]
        
        self.convos_pp = utils.parse_pp(defines['convos_pp'])
        self.convo_templates = []
        array = utils.parse_str(defines['convo_templates'])
        for each in array:
            self.convo_templates.append(screen.read_img('../database/programs/groupme_web/'+each))
        self.convo_names = utils.parse_str(defines['convo_names'])
        
        self.usernames = utils.parse_str(defines['usernames'])
        self.my_username = utils.parse_str(defines['me'])[0]
        
        self.flag_msg = "Collection"
        
    def open(self):
        self.program.open("groupme.com") # we remember the login for our script
        time.sleep(self.delay)
    
    def close(self):
        self.program.close()
        time.sleep(self.delay)
    
    def open_convo(self, index):
        loc = self.screen.match_template(self.screen.cvtPIL2np(self.screen.sample()),self.convo_templates[index])
        ui.click(loc[0]+20, loc[1]+20, clicks=1, button='left')
        time.sleep(self.delay)
    
    def get_new_msgs(self):
        self.loggings.log('Fetching new messages')
        new_msgs = {}
        for index,convo_name in enumerate(self.convo_names):
            # open the conversation
            self.open()
            self.open_convo(index)
            # collection
            # focus on message box
            ui.click(self.messages_cent[0],self.messages_cent[1],clicks=1,button='left')
            time.sleep(self.delay)
            # scroll up at least far enough: 2 load older message actions (4 pg up keys each)
            for i in range(2*4):
                ui.hotkey('pgup')
                time.sleep(self.delay)
            # select all and copy
            ui.hotkey('ctrl','a')
            time.sleep(self.delay)
            ui.hotkey('ctrl','c')
            # send acknowledgement
#             self.send_msg(self.flag_msg)
            # destroy window
            self.close()
            # record the batch
            # make raw txt file with notepad to convert it to ASCII encoding while
            # maintaining the original new line characters. If we do it through
            # pasting the clipboard to python and converting the encoding in the shell
            # it gives strange extra new line characters.
            utils.mktxt_notepad('../database/files/$temp.txt')
            time.sleep(self.delay)
            # we made sure that this file was not existent before so we expect a 'create
            # new file prompt' from notepad
            ui.hotkey('enter')
            time.sleep(self.delay)
            # just in case the file existed and had things, paste over everything
            ui.hotkey('ctrl','a')
            ui.hotkey('ctrl','v')
            ui.hotkey('ctrl','s')
            time.sleep(self.delay)
            # here a warning apears about losing some characters when converting to
            # ASCII/ANSI. enter to confirm
            ui.hotkey('enter')
            ui.hotkey('alt','f4')
            time.sleep(self.delay)
            ui.hotkey('s')
            # read txt and return only the new_msgs as an array of strings
            data = utils.read_txt('../database/files/$temp.txt')
            temp_msgs = data
            for i,line in utils.reverse_enumerate(data):
                # identify 'me' putting an acknowledgement as the end of new messages
                if line == self.flag_msg and data[i-1] == self.my_username:
                    # Search one down for time stamp if not, search up for closest time
                    temp_msgs = data[i+1:]
                    if not self.is_timestamp(data[i+1]):
                        j = i-2
                        while (not self.is_timestamp(data[j]) or j<0):
                            j-=1
                        if j>=0:
                            temp_msgs = [data[j]] + temp_msgs
            # delete the $temp.txt file for good practice
            utils.cmd_prompt("cd ../database/files & del $temp.txt")
            new_msgs[convo_name] = temp_msgs
        self.loggings.log('Returning new messages')
        # new messages get returned as a dictionary keyed by the conversation name
        return new_msgs
    
    def is_username(self,s):
        return s in self.usernames
        
    def is_timestamp(self,s):
        return ('AM' in s[-3:] or 'PM' in s[-3:]) and len(s)<17 and (':' in s)
    
    def parse_timestamp(self,s):
        ''' return it in yyyy MM dd hh mm ss'''
        yyyy, MM, dd, hh, mm, ss = (None, None, None, None, None, None)
        if ',' in s:
            date_info, time_info = s.split(',')
        else:
            date_info = None
            time_info = s
        # time info
        time_info = time_info.replace(' ','')
        ampm = time_info[-2:]
        time_info = time_info[:-2]
        hh,mm = (lambda x: (utils.pad('left','0',2,x[0]),utils.pad('left','0',2,x[1])) )(time_info.split(':'))
        ss = '00'
        # convert to 24 hour clock
        if ampm == 'AM' and hh == '12':
            hh = '00'
        if ampm == 'PM' and hh != '12':
            hh = utils.pad('left','0',2,str(int(hh)+12))
        # date info
        now = utils.get_time()
        day = utils.get_weekday(now)
        if date_info != None:
            # Then the time stamp refers to some other day other then today
            if utils.has_digit(date_info):
                # some date was specified
                JAN,FEB,MAR,APR,MAY,JUN,JUL,AUG,SEP,OCT,NOV,DEC = (1,2,3,4,5,6,7,8,9,10,11,12)
                # grab the month and date
                MM = utils.pad('left','0',2,str(eval(date_info[:3])))
                dd = utils.pad('left','0',2,str(date_info[3:])) 
            else:
                # some weekday was specified, it means the previous x day
                MON, TUE, WED, THU, FRI, SAT, SUN = (0,1,2,3,4,5,6)
                # grab the specified weekday
                timestamp_day = eval(date_info)
                # calculate how many days ago that must be
                days_prior = (day - timestamp_day)%7
                # roll back time using datetime objects
                td = utils.timedelta(days=days_prior)
                now = utils.rollback_time(now,td)
        # if any of the fields were specified, update the array to be returned.
        # else the default information is as specified by "today"
        a = utils.datetime2str(now).split('-')[:-1] # [yyyy MM dd hh mm ss |splice| decimals]
        f = lambda x: x[0] if x[1] == None else x[1]
        return [f((a[0],yyyy)),f((a[1],MM)),f((a[2],dd)),f((a[3],hh)),f((a[4],mm)),f((a[5],ss))]