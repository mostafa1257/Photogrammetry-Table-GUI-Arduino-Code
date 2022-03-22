from tkinter import *
import tkinter as tk
import serial
import time
import sys
from PIL import Image, ImageTk
import struct
import os
import pandas as pd
from itertools import product
import json

presets_file_path = f'{os.getcwd()}\Presets.xlsx'
gui_config_file = open(f'{os.getcwd()}\gui_configs.json')
gui_config = json.load(gui_config_file)  

d = True

class main_window:
    root = Tk()
    
    mode = IntVar()
    duplex_mode = IntVar()
    camera_placement = IntVar()
    tilt_direction = IntVar()
    
    SUB_WINDOWS = []
    MAIN_WINDOW_WIDGETS = []
    STEP_MODE_LABELS = []
    STEP_MODE_ENTRIES = []
    CONT_MODE_LABELS = []
    CONT_MODE_ENTRIES = []
    SETTINGS_LABELS = []
    SETTINGS_ENTRIES = []
    SETTINGS_RBUTTONS = []
    OPERATION_BUTTONS = []
    
    def __init__(_gui):
        # Main Window Parameters (not resizable)
        _gui.win_SIZE  = gui_config["window properties"]["window size"]
        _gui.txt_CLR   = gui_config["window properties"]["text color"]
        _gui.bkgnd_CLR = gui_config["window properties"]["background color"]
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
            
    def openMainWindow(_gui):
        # Opens Main GUI Window
        _gui.root.configure(bg=_gui.bkgnd_CLR)
        _gui.root.geometry(_gui.win_SIZE)
        _gui.root.resizable(False, False)
        _gui.root.title("CamScan Tool v2.0")
            
        _gui.root.mainloop()  

    def createLabel(_lbl,parent_frame,txt,gy,gx):
        _lbl.label = Label(parent_frame,text=txt,font=3,bg=_lbl.bkgnd_CLR,fg=_lbl.txt_CLR)         
        _lbl.label.grid(row=gy, column=gx) 

        return _lbl.label

    def createEntry(_ent,parent_frame,w,gy,gx):
        _ent.entry = Entry(parent_frame,width=w,font=3,disabledbackground="gray50")
        _ent.entry.grid(row=gy,column=gx,padx=5,pady=10)

        return _ent.entry
    
    def createButton(_but,parent_frame,txt,fnt,w,h,fgc,bgc,bw,cmd,gy,gx):
        _but.button = Button(
                            parent_frame,
                            text=txt,
                            font=fnt,
                            fg=fgc,
                            bg=bgc,
                            width=w,
                            height=h,
                            borderwidth=bw,
                            command=cmd)
        _but.button.grid(row=gy,column=gx)
        
        return _but.button

    def createRadioButton(_radb,parent_frame,txt,fnt,cmd,val,var,gy,gx):
        _radb.radio_B = Radiobutton(
                                    parent_frame,
                                    text=txt,
                                    bg=_radb.bkgnd_CLR,
                                    fg=_radb.txt_CLR,
                                    font=fnt,
                                    command=cmd,
                                    value=val,
                                    variable=var)
        _radb.radio_B.grid(row=gy,column=gx)

        return _radb.radio_B

class sub_window(main_window):
    def __init__(_sub):        
        main_window.__init__(_sub)

    def createSubWindow(_sub,px,py):
        _sub.sub_FRAME = Frame(_sub.root, padx=5, pady=5, borderwidth=5, relief="groove", bg=_sub.bkgnd_CLR)
        _sub.sub_FRAME.place(x=px, y=py)  

        return _sub.sub_FRAME

class presets:
    def __init__(_prst,file_path,idx_column):
        _prst.file_PATH = file_path
        _prst.idx_COLUMN = idx_column

    def openPresetsFile(_file):
        # CSV File that includes Predefined Presets
        _file.presets_FILE = pd.read_excel(_file.file_PATH,index_col=_file.idx_COLUMN)
        _file.presets_NUM = _file.presets_FILE.shape[0]  

        return _file.presets_FILE
    
class table_params(main_window,presets):
    def __init__(_tp,packet_size):
        main_window.__init__(_tp)
        presets.__init__(_tp,presets_file_path,"Presets")
        _tp.pckt_SIZE = packet_size
        _tp.preset_ID = 1
        
    def loadPresetData(_tp):
        _tp.ENTRIES = [*_tp.STEP_MODE_ENTRIES,*_tp.SETTINGS_ENTRIES,*_tp.CONT_MODE_ENTRIES]
        i = 0
        for entry in _tp.ENTRIES:
            entry.insert(0,_tp.openPresetsFile().iloc[_tp.preset_ID][gui_config["preset keys"][i]])
            i += 1 
    
    def clearPresetData(_tp):
        i = 0
        for entry in _tp.ENTRIES:
            entry.delete(0,END)  
            i += 1
    
    def cyclePresets(_cp):
        _cp.clearPresetData()
        if _cp.preset_ID >= _cp.presets_NUM:
            _cp.preset_ID = 0
        _cp.loadPresetData()
        _cp.preset_ID += 1
        _cp.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["current preset value"]].configure(text=str(_cp.preset_ID))
        
    def stepModeSelected(_sms):
        for step_entry,step_label,cont_entry,cont_label in product(
        _sms.STEP_MODE_ENTRIES,
        _sms.STEP_MODE_LABELS,
        _sms.CONT_MODE_ENTRIES,
        _sms.CONT_MODE_LABELS):
            step_entry.configure(state=NORMAL)
            step_label.configure(bg="gray20")
            cont_entry.configure(state=DISABLED)
            cont_label.configure(bg="gray10")

        _sms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["step mode select button"]].configure(fg="green4")
        _sms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["cont mode select button"]].configure(fg="red")

        _sms.SUB_WINDOWS[gui_config["sub window indicies"]["step mode sub window"]].configure(bg="gray20")
        _sms.SUB_WINDOWS[gui_config["sub window indicies"]["cont mode sub window"]].configure(bg="gray10" )
        
        _sms.mode.set(1)

    def duplexModeSelected(_dms):
        global d
        d = not d
        _dms.duplex_mode.set(d)
        if d == True:
            _dms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["duplex mode select button"]].configure(fg="green4")
        if d == False:
            _dms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["duplex mode select button"]].configure(fg="red")

    def contModeSelected(_cms):
        for step_entry,step_label,cont_entry,cont_label in product(
            _cms.STEP_MODE_ENTRIES,
            _cms.STEP_MODE_LABELS,
            _cms.CONT_MODE_ENTRIES,
            _cms.CONT_MODE_LABELS):
                step_entry.configure(state=DISABLED)
                step_label.configure(bg="gray10")
                cont_entry.configure(state=NORMAL)
                cont_label.configure(bg="gray20")

        _cms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["step mode select button"]].configure(fg="red")
        _cms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["cont mode select button"]].configure(fg="green4")

        _cms.SUB_WINDOWS[gui_config["sub window indicies"]["cont mode sub window"]].configure(bg="gray20")
        _cms.SUB_WINDOWS[gui_config["sub window indicies"]["step mode sub window"]].configure(bg="gray10" )

        _cms.mode.set(0) 
        
    def frontSelected(_fs):
        _fs.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='green4')
        _fs.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'red')

    def topSelected(_ts):
        _ts.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='red')
        _ts.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'green4')

    def fwdSelected(_fws):
        _fws.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='green4')
        _fws.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'red')

    def bwdSelected(_bws):
        _bws.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='red')
        _bws.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'green4')
            
    def validate(_v):
        for i in range(len(_v.ENTRIES)):
            max_key = (list(gui_config["validation"].keys())[2*i])
            min_key = (list(gui_config["validation"].keys())[2*i+1])
            assert (int(_v.ENTRIES[i].get()) <= gui_config["validation"][max_key]) and (int(_v.ENTRIES[i].get()) >= gui_config["validation"][min_key]) , "not correct"
        print("Validated")
        
    def lockTilt(_lt):
        print("Lock Tilt")

    def lockRot(_lr):
        print("Lock Rot")
        
    def homeTilt(_ht):
        print("Home Tilt")

    def homeRot(_hr):
        print("Home Rot")
        
    def upload(_up):
        print("Uploading")
        
    def dummy(_d):
        pass

    def connect(_cnt):
        print("connecting")