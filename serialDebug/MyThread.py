'''
@ author: hogen
@ tools: pycharm
@ content: 实现线程类
@ date: 2021.01.29
'''
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ctypes
import threading
import time
import tkinter

import MisDll

# threadLock = threading.Lock()
# threads = []
from serialDebug.MainSerial import MainSerial


class myThread(threading.Thread):
    def __init__(self, indata,outdata):
        threading.Thread.__init__(self)
        self.indata = indata
        self.outdata = outdata

    def run(self):
        MainSerial.showLog(self,"Starting....")
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        # threadLock.acquire()
        self.trans()
        # 释放锁
        # threadLock.release()

    def trans(self):
        string1 = "0200637B22616D6F756E74223A22302E3031222C22636F6465223A302C22636F6E73756D6554797065223A342C226D7367223A22B3C9B9A6B7A2C6F0BDBBD2D7227D0338"
        string2 = "no"
        string3 = "no"

        # create byte objects from the strings
        b_string1 = string1.encode('utf-8')
        b_string2 = ctypes.c_char_p(string2.encode('utf-8'))
        b_string3 = string3.encode('utf-8')

        result = MisDll.POS_Trans( b_string1,
                                   2,
                                   b_string2,
                                   b_string3)

        print("TYPE",type(b_string2))
        s = b_string2.value
        data = str(s,'gbk')
        self.showLog("POS_Trans recevie data:"+data)
        self.showLog("POS_Trans result is %d"%result)



