# coding:utf-8
'''
@ author: hogen
@ tools: pycharm 
@ content: 实现串口通讯主类
@ date: 2021.01.29
'''
import threading

import MyThread
import tkinter
from tkinter import ttk, RIGHT, Y, LEFT


from SerialClass import SerialAchieve   # 导入串口通讯类
import MisDll
import ctypes

POLLING_DELAY = 250  # ms
lock = threading.Lock()  # Lock for shared resources.
finished = False



class MainSerial:
    def __init__(self):
        # 定义串口变量
        self.port = None
        self.band = None
        self.check = None
        self.data = None
        self.stop = None
        self.myserial = None
        self.misdll = None
        self.isOpen = None
        self.timeout = "60"

        # 初始化窗体
        self.mainwin = tkinter.Tk()
        self.mainwin.title("MIS模拟器")
        self.mainwin.geometry("600x400")

        # 标签
        self.label1 = tkinter.Label(self.mainwin,text = "串口号:",font = ("宋体",15))
        self.label1.place(x = 5,y = 5)
        self.label2 = tkinter.Label(self.mainwin, text="波特率:", font=("宋体", 15))
        self.label2.place(x=5, y=45)

        # 文本显示，清除发送数据
        self.label6 = tkinter.Label(self.mainwin, text="LOG:", font=("宋体", 15))
        self.label6.place(x=230, y=5)

        self.label7 = tkinter.Label(self.mainwin, text="交易结果:", font=("宋体", 15))
        self.label7.place(x=230, y=200)

        # 串口号
        self.com1value = tkinter.StringVar()  # 窗体中自带的文本，创建一个值
        self.combobox_port = ttk.Combobox(self.mainwin, textvariable=self.com1value,
                                          width = 10,font = ("宋体",13))
        # 输入选定内容
        self.combobox_port["value"] = [""]  # 这里先选定

        self.combobox_port.place(x = 105,y = 5)  # 显示

        # 波特率
        self.bandvalue = tkinter.StringVar()  # 窗体中自带的文本，创建一个值
        self.combobox_band = ttk.Combobox(self.mainwin, textvariable=self.bandvalue, width=10, font=("宋体", 13))
        # 输入选定内容
        self.combobox_band["value"] = ["4800","9600","14400","19200","38400","57600","115200"]  # 这里先选定
        self.combobox_band.current(6)  # 默认选中第0个
        self.combobox_band.place(x=105, y=45)  # 显示

        # 获取文件路径
        self.label6 = tkinter.Label(self.mainwin, text="超时时间:", font=("宋体", 15))
        self.label6.place(x=0, y=80)

        test_str = tkinter.StringVar(value="60")
        self.entrySend = tkinter.Entry(self.mainwin, width=3, textvariable=test_str, font=("宋体", 15))
        self.entrySend.place(x=120, y=80)  # 显示

        # 按键显示，打开串口
        self.button_OK = tkinter.Button(self.mainwin, text="打开串口",
                                        command=self.button_OK_click, font = ("宋体",13),
                                        width = 10,height = 1)
        self.button_OK.place(x = 5,y = 125)  # 显示控件
        # 关闭串口
        self.button_Cancel = tkinter.Button(self.mainwin, text="关闭串口",  # 显示文本
                                 command=self.button_Cancel_click, font = ("宋体",13),
                                 width=10, height=1)
        self.button_Cancel.place(x = 120,y = 125)  # 显示控件

        # 清除发送数据
        self.button_Cancel = tkinter.Button(self.mainwin, text="清LOG",  # 显示文本
                                            command=self.button_clcSend_click, font=("宋体", 13),
                                            width=13, height=1)
        self.button_Cancel.place(x=400, y=2)  # 显示控件

        # 清除接收数据
        self.button_Cancel = tkinter.Button(self.mainwin, text="清除接收数据",  # 显示文本
                                            command=self.button_clcRece_click, font=("宋体", 13),
                                            width=13, height=1)
        self.button_Cancel.place(x=400, y=197)  # 显示控件

        # 人脸交易按键
        self.button_Face = tkinter.Button(self.mainwin, text="人脸",  # 显示文本
                                            command=lambda:self.processTrans("{\"amount\":\"0.01\",\"code\":0,\"consumeType\":4}"), font=("宋体", 13),
                                            width=10, height=1)
        self.button_Face.place(x=5, y=180)  # 显示控件

        # 扫码交易按键
        self.button_QR = tkinter.Button(self.mainwin, text="扫码",  # 显示文本
                                          command=lambda:self.processTrans("{\"amount\":\"0.01\",\"code\":1,\"consumeType\":4}"), font=("宋体", 13),
                                          width=10, height=1)
        self.button_QR.place(x=5, y=230)  # 显示控件

        # 显示框
        # 实现记事本的功能组件
        self.SendDataView = tkinter.Text(self.mainwin,width = 40,height = 9,
                                         font = ("宋体",13))  # text实际上是一个文本编辑器
        self.SendDataView.place(x = 230,y = 35)  # 显示


        self.ReceDataView = tkinter.Text(self.mainwin, width=40, height=9,
                                         font=("宋体", 13))  # text实际上是一个文本编辑器
        self.ReceDataView.place(x=230, y=230)  # 显示



        # 获取界面的参数
        self.band = self.combobox_band.get()
        self.showLog("波特率："+self.band)
        self.myserial = SerialAchieve(int(self.band),self.check,self.data,self.stop)


        # 处理串口值
        self.port_list = self.myserial.get_port()
        port_str_list = []  # 用来存储切割好的串口号
        for i in range(len(self.port_list)):
            # 将串口号切割出来
            lines = str(self.port_list[i])
            str_list = lines.split(" ")
            port_str_list.append(str_list[0])
        self.combobox_port["value"] = port_str_list
        self.combobox_port.current(0)  # 默认选中第0个

    def show(self):
        self.mainwin.mainloop()

    def button_OK_click(self):
        '''
        @ 串口打开函数
        :return: 
        '''
        if self.port == None:
            com = self.combobox_port.get()
            timeout = self.entrySend.get()
            self.showLog("%d"%int(com[3:]))
            port = ctypes.c_int(int(com[3:]))
            self.isOpen = MisDll.SetCommParam(port,int(self.band),int(timeout))
            self.showLog("动态库加载%d(0:成功 其他:失败) "%self.isOpen)
            self.showLog("打开串口成功")
        else:
            pass

    def button_Cancel_click(self):
        self.button_Face.config(state=tkinter.NORMAL)
        self.button_QR.config(state=tkinter.NORMAL)
        self.myserial.delete_port()
        self.isOpen = -1
        self.showLog("关闭串口成功")

    def button_clcSend_click(self):
        self.SendDataView.delete("1.0","end")

    def button_clcRece_click(self):
        self.ReceDataView.delete("1.0", "end")

    def button_Send_click(self):
        self.isbtnClicked = True
        self.thread = threading.Thread()

    def processTrans(self,command):
        global finished
        self.command = command
        self.button_Face.config(state=tkinter.DISABLED)
        self.button_QR.config(state=tkinter.DISABLED)
        with lock:
            finished = False
        t = threading.Thread(target=self.count)
        t.daemon = True
        self.mainwin.after(POLLING_DELAY, self.check_status)  # Start polling.
        t.start()

    def check_status(self):
        with lock:
            if not finished:
                self.mainwin.after(POLLING_DELAY, self.check_status)  # Keep polling.
            else:
                print('end')

    def count(self):
        global finished
        resutl = self.doTrans(self.command)
        with lock:
            self.showLog(tkinter.INSERT,resutl)
            self.button_Face.config(state=tkinter.NORMAL)
            self.button_QR.config(state=tkinter.NORMAL)

    def doTrans(self,command):
        try:
            if self.isOpen >= 0:
                self.showLog("开始交易...")
                send_str = self.entrySend.get()
                self.showLog("超时时间:%s"%send_str)
                t = MyThread.myThread(command)
                t.setDaemon(True)
                t.start()
                t.join()
                return t.get_result()
            else:
                self.showLog("串口没有打开")
        except Exception as e:
            print(e)
            self.showLog("发送失败")

    def showLog(self,data):
        self.SendDataView.insert(tkinter.INSERT,data+"\n")


if __name__ == '__main__':
    my_ser1 = MainSerial()
    my_ser1.show()


