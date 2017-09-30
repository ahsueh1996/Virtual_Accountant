from cortex import Cortex
from messenger import GroupMe_Web
import utils

class Collector(Cortex):
    ''' The collector's job is to make a metadata file and raw data files on disk
    for the next cortex to process. Array recording which files were added will be
    published using the skull (see cortex super class) to the subscribers.'''
    def __init__(self,screen,logging_groups = ['Default','Cortex']):
        Cortex.__init__(self,'Collector',logging_groups)
        
        # Current collection platform
        self.platform = GroupMe_Web(screen,logging_groups)
        
        # The following is parsing the defines.txt to get the app specific data
        defines = utils.parse_defines(utils.read_txt("../database/cortex/collector.txt"))
        self.alias_dict = eval(defines['member_alias'])
    
    def default_meta(self):
        return {'rec_time': None, 'sent_time': None, 'sender': None,
                 'platform': None, 'convo_name': None, 'medium': None}
        
    def fire(self,data):
        self.loggings.log('Fire')
        rec_array = []
        new_msgs_dict = self.platform.get_new_msgs()
        meta = self.default_meta()
        meta['platform'] = self.platform.class_name    
        for convo_name in new_msgs_dict:
            ''' expect these types of data (aka medium) to record:
            -text
            -img
            -meta
            
            For GroupMe_web:
            -images are expected when there is an empty line with perhaps just a space character.
            -emoticons don't appear at all.. just the username and its avatar proceeds it.
            -message sent times are grouped and always say AM or PM. It assumes the closest
                specified day of the week or it uses actual date. ALL caps.
            -A line is a message if it is proceeded by a username.
            
            TUE, 4:15 PM
            Avatar
            User 1 Name
            testing
            message 2, blah
            '''
            # iterate the array of new messages from oldest to newest
            meta['convo_name'] = convo_name
            for line in new_msgs_dict[convo_name]:
                if self.platform.is_timestamp(line):
                    meta['sent_time'] = self.platform.parse_timestamp(line)
                    continue
                if self.platform.is_username(line):
                    meta['sender'] = self.alias_dict[line]
                    continue
                if line == 'Avatar':
                    continue
                rec_time = utils.get_str_time()
                rec_time_str = utils.datetime2str(rec_time)
                meta['rec_time'] = rec_time_str.split('-') 
                if line == ' ':
                    meta['medium'] = 'img'
                    '''TODO'''
                else:
                    meta['medium'] = 'txt'
                    utils.mktxt('../database/files/',rec_time_str+'-raw_text.txt',log=0)
                    utils.write_2_file(line,no_time=True)
                utils.pickle_sto('../database/files/',rec_time_str+'-meta.pkl',meta)
                rec_array.append(rec_time)
        self.skull.publish(self.name,rec_array)
            