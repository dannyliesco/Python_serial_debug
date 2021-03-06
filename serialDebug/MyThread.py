# coding:utf-8
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

class myThread(threading.Thread):
    def __init__(self, indata,dll):
        threading.Thread.__init__(self)
        self.indata = indata
        self.dll = dll

    def run(self):

        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        # threadLock.acquire()
        self.result = self.trans()
        # 释放锁
        # threadLock.release()

    def trans(self):
        string1 = "{\"amount\":\"0.01\",\"code\":0,\"consumeType\":4}"
        string2 = "trans fail!!!!\n"
        string3 = "fail"

        # create byte objects from the strings
        b_string1 = self.indata.encode('utf-8')
        b_string2 = ctypes.c_char_p(string2.encode('utf-8'))
        b_string3 = string3.encode('utf-8')
        try:
            self.dll.pos_trans(b_string1,
                                      2,
                                      b_string2,
                                      b_string3)
            print("TYPE", type(b_string2))
            print(b_string2)
            s = b_string2.value
            print(s)
            data = str(s,'gbk')
            return data
        except Exception as e:
            print(e)

    def get_result(self):
        try:
            return self.result
        except Exception:
            return None



