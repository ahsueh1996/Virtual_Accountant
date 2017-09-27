import pyautogui as ui
import os
import time
import utils

class Program():
    def __init__(self):
        self.bondary = [(0,0),(0,0)]
        self.anchor = (0,0)
    
    def set_boundary(self,boundary):
        self.bondary = boundary
        # for now we assume all boundary is rectangle
        self.set_anchor(utils.rect_cent_pp(boundary[0],boundary[1]))
    
    def set_anchor(self,anchor):
        self.anchor = anchor

    def open(self):
        pass
    
    def full_screen(self):
        ui.hotkey('win','up')
        self.set_boundary([(0,0),ui.size()])
    
    def close(self):
        ui.hotkey('alt','f4')
        self.set_bondary = [(0,0),(0,0)]

''' ******************************************************
Common fields of a program
*********************************************************'''               
class Program_Field():
    def __init__(self):
        self.zone = ((0,0),(0,0))
        self.zone_cent = (0,0)
    
    def set_zone(self, p1, p2):
        self.zone = (p1,p2)
        self.zone_cent = utils.rect_cent(utils.pp2quad(p1,p2))
    
    def get_zone_quad(self):
        return utils.pp2quad(self.zone)
    
    def set_zone_cent(self,cent):
        self.zone_cent = cent

class Scrollable(Program_Field):
    def __init__(self):
        Program_Field.__init__(self)
    
    def scroll(self,clicks):
        x,y = self.zone_cent
        ui.scroll(clicks, x, y)
        
class Clickable(Program_Field):
    def __init__(self):
        Program_Field.__init__(self)
    
    def click(self,button,clicks):
        x,y = self.zone_cent
        ui.click(x, y, clicks, interval=0.2, button=button)
        
''' ******************************************************
Types of Programs: Explorers
*********************************************************'''       
    
class Explorer(Program):
    def __init__(self):
        Program.__init__(self)
        
    def _search(self,query):
        ''' right after a open command the cursor is focused on
        the search bar. For now, this function should be used with open'''
        ui.typewrite(query)
        ui.hotkey('enter')
    
class Chrome(Explorer):
    def __init__(self):
        Explorer.__init__(self)
    
    def open(self, query):
        ''' opens a new tab in a new chrome window
        The profile can be selected: Default, Guest, Profile #'''
        utils.cmd_prompt('start chrome --profile-directory="Default"')
        # alt: 'start chrome --profile-directory="Default" "<query URL>"'
        time.sleep(2)
        self._search(query)
        self.full_screen()
        
    def close(self):
        ''' requires that the opened tab is in focus, choose to
        do ctrl w because if another app was in focus.. we'd have
        closed it, besides the open function will open 1 tab in a
        new app window'''
        ui.hotkey('ctrl','w')
        
