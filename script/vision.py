import pyautogui as ui
import time
import copy
import numpy as np
import cv2 as cv

import utils
from loggings import *

''' ******************************************************
Super class
*********************************************************'''

class Vision(Loggable):
    def __init__(self, name, savefile, filepath, ext, region, log_groups):
        Loggable.__init__(self,log_groups)
        self.class_name = "Vision"
        self.loggings.set_obj_id("Vision."+name)
        self.sample_count = 0
        self.savefile = savefile
        self.name = name
        self.ext = ext
        self.region = region
        self.savepath = filepath + "/"
        utils.mkdir(self.savepath)
    
    def sample(self, savefile = 0, description = ""):
        pass
    
    def read_img(self,file):
        return cv.imread(file)
    
    def show_img(self,img,wait=0):
        cv.imshow('Window',img)
        cv.waitKey(wait)

    def cvtPIL2np(self,im):
        ''' adds 0.01097sec '''
        return np.array(im)[:,:,::-1].copy()    # The PIL image is in RGB mode
                                                # you can tell if you print the PIL obj

    def reset_sample_count(self):
        self.sample_count = 0
        
    def filter_bgr(self,im,lb,ub):
        '''
        Call this on a nom cat screen capture and it returns a mask of all the obj
        using color segmentation.
        '''
        return cv.inRange(im, lb, ub)

    def filter_hsv(self,im,lb,ub):
        '''
        Call this on a nom cat screen capture and it returns a mask of all the obj
        using hsv color segmentation.
        '''
        hsv = cv.cvtColor(im,cv.COLOR_BGR2HSV)
        return cv.inRange(hsv, lb, ub)
    
    def define_contours(self,mask):
        '''
        Call this on a mask and we use centroid finding algorithm to localize all
        objects and return a vector of xy coordinates.
        '''
        __, contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        return contours
    
    def filter_contours_by_size(self,contours,lb=0,ub=9999999999999):
        ret = []
        for each in contours:
            if each.shape[0] >= lb and each.shape[0] <= ub:
                ret.append(each)
        return ret
    
    def eval_centroids(self,contours):
        ret = []
        for each in contours:
            M = cv.moments(each)
            ret.append( (int(M['m10']/M['m00']),int(M['m01']/M['m00'])) )
        return ret
    
    def match_template(self,img,template):
        res = cv.matchTemplate(img,template,cv.TM_CCOEFF)
        _,_,_,loc = cv.minMaxLoc(res)
        return loc
        
''' ******************************************************
Children Class: Screen related vision
*********************************************************'''        
    
class Screen(Vision):
    def __init__(self, name, savefile = 0, filepath = "../vision", ext = ".png", region = (-1,-1,-1,-1), log_groups = ["Default"]):
        Vision.__init__(self, name, savefile, filepath, ext, region, log_groups)
        self.class_name += ".Screen"
        self.loggings.set_obj_id(self.class_name+"."+name)
    
    def sample(self, get_filename = None, savefile = 0, description = ""):
        '''
        Sampling is done by taking a screenshot of the primary display using the 
        py auto gui library and the screenshot is returned as an PIL object.
        Using the cvtPIL2np, we automatically convert image to numpy array.
        Sampling by default will not save the screen shot, but for demonstration
        we can choose to save it. Give it a file path and a prefix and each time
        sample is called, the file will be saved. 
        Saving to disk costs time: avg 0.1045 sec
        Compared to not saving: avg 0.034 sec
        '''
        if get_filename == None:
            filename = str(self.sample_count)
        else:
            filename = get_filename()
        if self.savefile == 1 or savefile == 1:
            im =  ui.screenshot(self.savepath + filename + description + self.ext)
            self.sample_count += 1
        else:
            if self.region == (-1,-1,-1,-1):
                im = ui.screenshot()
            else:
                im = ui.screenshot(region=self.region)
        
        return im


        