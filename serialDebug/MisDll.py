# coding:utf-8
'''
@ author: hogen
@ tools: pycharm
@ content: 动态库加载
@ date: 2021.01.29
'''
import ctypes
import os
import shutil

# Try to locate the .so file in the same directory as this file
class CommDll:

    def __init__(self):
        self.mod = 'nothing'

    def loadDll(self,filename):
        os.add_dll_directory(os.getcwd())
        os.add_dll_directory(os.path.dirname(filename))
        print("path:"+os.path.dirname(filename))
        # SetCommParam(int nCommPort, int nBps, int nTimeout)
        print("filename:"+filename)
        result = self.mod = ctypes.windll.LoadLibrary(filename)
        print("动态库加载结果",result)
        self.mod.SetCommParam.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int)
        self.mod.SetCommParam.restype = ctypes.c_int


        # POS_Trans(char *pInData, int nQuertyTimes, char *pOutData, char *psMsgID)
        self.mod.POS_Trans.argtypes = (ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p)
        self.mod.POS_Trans.restype = ctypes.c_int
        return result

    def setcommparam(self,band,int,timeout):
        return self.mod.SetCommParam(band,int,timeout)

    def pos_trans(self,p1,p2,p3,p4):
        return self.mod.POS_Trans(p1,p2,p3,p4)








