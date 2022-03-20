from os import stat
from tkinter import *
import tkinter as tk
import serial
import time
from serial.tools.list_ports import comports
import sys
from PIL import Image, ImageTk
import struct
import os
import pandas as pd

class main_window:
    root = Tk()
    def __init__(_gui):
        # Main Window Parameters (not resizable)
        _gui.win_SIZE  = "1600x900"
        _gui.txt_CLR   = "white"
        _gui.bkgnd_CLR = "gray10"
        _gui.root = main_window.root
        
    def openCommPort(_gui,baud_rate,comm_port):
        # Comm Port Parameters
        _gui.baud_RATE = baud_rate
        _gui.comm_PORT = comm_port
        
        # List Serial Comm Ports 
        if sys.platform.startswith("win"):
            _gui.ports = ["COM%s" % (i + 1) for i in range(256)]

        _gui.available_ports = []
        for port in _gui.ports:
            try:
                s = serial.Serial(port)
                s.close()
                _gui.available_ports.append(port)
            except (OSError, serial.SerialException):
                pass
        # Assume only 1 Device is connected to the Computer
        _gui.comm_PORT = serial.Serial(str(_gui.available_ports[0]), baudrate=_gui.baud_RATE, timeout=0.5)
        
    def openPresetsFile(_gui):
        # CSV File that includes Predefined Presets
        _gui.presets_FILE = pd.read_excel(r'D:\Photogrammetry Table v2\Presets.xlsx',index_col= 'Presets')
        _gui.presets_NUM = _gui.presets_FILE.shape[0]  
        _gui.preset_ID = 1            
            
    def openMainWindow(_gui):
        # Opens Main GUI Window
        _gui.root.configure(bg=_gui.bkgnd_CLR)
        _gui.root.geometry(_gui.win_SIZE)
        _gui.root.resizable(False, False)
        _gui.root.title("CamScan Tool v2.0")
            
        _gui.root.mainloop()   

class sub_window(main_window):
    def __init__(_sub):        
        main_window.__init__(_sub)

    def drawSubWindow(_sub,px,py):
        _sub.sub_FRAME = Frame(_sub.root, padx=5, pady=5, borderwidth=5, relief="groove", bg=_sub.bkgnd_CLR)
        _sub.sub_FRAME.place(x=px, y=py)
        _sub.yaw_rotation_time_label = Label(_sub.sub_FRAME,text="Rotation Time (min:1s)",font=3,bg=_sub.bkgnd_CLR,fg=_sub.txt_CLR)         
        _sub.yaw_rotation_time_label.grid(row=0, column=0)  
             
GUI = main_window()
cont = sub_window()
cont.drawSubWindow(50,450)
GUI.openMainWindow()
