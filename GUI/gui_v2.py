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
    def __init__(_gui,baud_rate,comm_port):
        # Main Window Parameters (not resizable)
        _gui.win_SIZE  = "1600x900"
        _gui.txt_CLR   = "white"
        _gui.bkgnd_CLR = "gray10"
        
        # Comm Port Parameters
        _gui.baud_RATE = baud_rate
        _gui.comm_PORT = comm_port
        
    def openCommPort(_gui):
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
                
GUI = main_window(115200,"COM3")

        
root = Tk()
root.configure(bg=GUI.bkgnd_CLR)
root.geometry(GUI.win_SIZE)
root.resizable(False, False)
root.title("CamScan Tool v2.0")
    
root.mainloop()    