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

def mkdir(savepath):
    try:
        os.makedirs(savepath)
    except FileExistsError:
        pass

def mktxt(savepath,filename):
    t = get_str_time()
    mkdir(savepath)
    f = open(savepath+filename,"a+")
    f.write(">>>>>NEW LOG BEGINS "+t+">>>>>>\n")
    return f

def write_2_file(f,msg):
    t = get_str_time()
    f.write(t+":\t"+msg+"\n")
    
def print_with_time(msg):
    t = get_str_time()
    print(t+":  "+msg)
    
''' ******************************************************
Operations
*********************************************************'''       
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

def rect_cent(q):
    half_x = int(q[2]/2)
    half_y = int(q[3]/2)
    return (q[0]+half_x, q[1]+half_y)