''' ******************************************************
Datetime
*********************************************************'''       
import datetime

def datetime2str(dt_obj):
    dt = str(dt_obj)
    dt = dt.replace(" ","-")
    dt = dt.replace(":","-")
    dt = dt.replace(".","-")
    return dt

def get_time():
    return datetime.datetime.now()

def get_str_time():
    return datetime2str(get_time())

''' ******************************************************
OS
*********************************************************'''       
import os

def cmd_prompt(command):
    os.system(command)

def mkdir(savepath):
    try:
        os.makedirs(savepath)
    except FileExistsError:
        pass

def mktxt(savepath,filename,log=1):
    t = get_str_time()
    mkdir(savepath)
    f = open(savepath+filename,"a+")
    if log==1:
        f.write(">>>>>NEW LOG BEGINS "+t+">>>>>>\n")
    return f

def mktxt_notepad(filepath):
    ''' Focus changes to the notepad'''
    cmd_prompt("start notepad " + "'" + filepath + "'")

def write_2_file(f,msg):
    t = get_str_time()
    f.write(t+":\t"+msg+"\n")
    
def print_with_time(msg):
    t = get_str_time()
    print(t+":  "+msg)

def read_txt(filepath):
    ''' Return an array of file content deliminated by new lines'''
    f = open(filepath,"r")
    ret = []
    for line in f:
        line = line.replace('\n','')
        ret.append(line)
    return ret

def parse_defines(file_array):
    dict = {}
    for line in file_array:
        if not '::' in line:
            continue
        info = line.split('::')
        dict[info[0]] = info[1]
    return dict

def parse_numbers(str):
    ret = []
    for each in str.split(','):
        ret.append(int(each))
    return ret

def parse_pp(str_pp):
    a = parse_numbers(str_pp)
    return ((a[0],a[1]),(a[2],a[3]))

def parse_str(str):
    ret = []
    for each in str.split(','):
        ret.append(each)
    return ret

''' ******************************************************
Clipboard
*********************************************************'''
import win32clipboard

def paste_clipboard():
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return data       
    
''' ******************************************************
Operations
*********************************************************

A point is a tuple is (x,y)
A quad is (x,y,w,h) where (x,y) define top left corner and (w,h) are width and height 
pp is a rect defined by two points
'''       
def pp2quad(p1,p2):
    minX = min(p1[0],p2[0])
    maxX = max(p1[0],p2[0])
    minY = min(p1[1],p2[1])
    maxY = max(p1[1],p2[1])    
    return (minX,minY,maxX-minX,maxY-minY)

def quad2pp(q):
    p1 = (q[0],q[1])
    p2 = (q[0]+q[2],q[1]+q[3])
    return (p1,p2)

def rect_cent_q(q):
    half_x = int(q[2]/2)
    half_y = int(q[3]/2)
    return (q[0]+half_x, q[1]+half_y)

def rect_cent_pp(p1,p2):
    return (int((p1[0]+p2[0])/2), int((p1[1]+p2[1])/2))

import itertools

def reverse_enumerate(iterable):
    """
    Enumerate over an iterable in reverse order while retaining proper indexes
    """
    return itertools.zip_longest(reversed(range(len(iterable))), reversed(iterable))