'''
@ author: hogen
@ tools: pycharm
@ content: 动态库加载
@ date: 2021.01.29
'''
import ctypes
import os

# Try to locate the .so file in the same directory as this file
_file = 'PortComm.dll'
_path = os.path.join(*(os.path.split(__file__)[:-1] + (_file,)))
_mod = ctypes.cdll.LoadLibrary(_path)



# SetCommParam(int nCommPort, int nBps, int nTimeout)
SetCommParam = _mod.SetCommParam
SetCommParam.argtypes = (ctypes.c_int, ctypes.c_int,ctypes.c_int)
SetCommParam.restype = ctypes.c_int

# POS_Trans(char *pInData, int nQuertyTimes, char *pOutData, char *psMsgID)
POS_Trans = _mod.POS_Trans
POS_Trans.argtypes = (ctypes.c_char_p, ctypes.c_int,ctypes.c_char_p,ctypes.c_char_p)
POS_Trans.restype = ctypes.c_int







