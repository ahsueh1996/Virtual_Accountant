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
    