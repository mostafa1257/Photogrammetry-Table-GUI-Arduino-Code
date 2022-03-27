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
import serial.tools.list_ports

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
        _tp.eof = 255
        _tp.paramBuffer = [None]*20
        _tp.dplx = True
        _tp.connected = False
        _tp.validated = False
        _tp.lock_TILT = True
        _tp.lock_ROT  = True
        _tp.comm_PORT = None

    def openCommPort(_ocp,baud_rate):        
        _ocp.ports = [tuple(p) for p in list(serial.tools.list_ports.comports())]
        try:
            _ocp.port = str(_ocp.ports[0][0])
            if _ocp.connected == False:
                _ocp.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["operation status"]].configure(text = "found 1 device")
                _ocp.comm_PORT = serial.Serial(str(_ocp.ports[0][0]), baudrate=baud_rate, timeout=0.5)
                _ocp.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["operation status"]].configure(text ="connecting ...")
                _ocp.connected = True
                _ocp.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["operation status"]].configure(text = "connected",fg="green2")
        except:
            _ocp.connected = False
            _ocp.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["operation status"]].configure(text = "couldn't connect , retrying ...",fg="yellow")
            pass            
                  
    def loadPresetData(_lpd):
        _lpd.ENTRIES = [*_lpd.STEP_MODE_ENTRIES,*_lpd.SETTINGS_ENTRIES,*_lpd.CONT_MODE_ENTRIES]
        i = 0
        for entry in _lpd.ENTRIES:
            entry.insert(0,_lpd.openPresetsFile().iloc[_lpd.preset_ID][gui_config["preset keys"][i]])
            i += 1 
    
    def clearPresetData(_cpd):
        i = 0
        for entry in _cpd.ENTRIES:
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
        _dms.dplx = not _dms.dplx
        _dms.duplex_mode.set(_dms.dplx)
        if _dms.dplx == True:
            _dms.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["duplex mode select button"]].configure(fg="green4")
        if _dms.dplx == False:
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

    def loadParams(_lp,pos,data):
        _lp.paramBuffer[pos] = int(data)

    def updateParamBuffer(_upb):
        if _upb.validated:
            _upb.loadParams(0,_upb.mode.get())

            for i in range(1,len(_upb.ENTRIES)+1):
                _upb.loadParams(i,_upb.ENTRIES[i-1].get())
            
            _upb.loadParams(12,_upb.camera_placement.get())
            _upb.loadParams(13,_upb.tilt_direction.get())
            _upb.loadParams(14,_upb.duplex_mode.get())
            _upb.loadParams(15,_upb.lock_TILT)
            _upb.loadParams(16,_upb.lock_ROT)
            _upb.loadParams(19,_upb.eof)

            print(_upb.paramBuffer)
        else:
            print("Not Validated")

    def validate(_v):
        try:
            for i in range(len(_v.ENTRIES)):
                max_key = (list(gui_config["validation"].keys())[2*i])
                min_key = (list(gui_config["validation"].keys())[2*i+1])
                assert (int(_v.ENTRIES[i].get()) <= gui_config["validation"][max_key]) and (int(_v.ENTRIES[i].get()) >= gui_config["validation"][min_key]) , "not correct"
            _v.validated = True
            print("Validated")
            _v.updateParamBuffer()
        except AssertionError as msg:
            _v.validated = False
            print(msg)
        
    def lockTilt(_lt):
        _lt.lock_TILT = not _lt.lock_TILT
        print("Lock Tilt")

    def lockRot(_lr):
        _lr.lock_ROT = not _lr.lock_ROT
        print("Lock Rot")
        
    def homeTilt(_ht):
        _ht.loadParams(17,int(1))
        _ht.loadParams(18,int(0))
        print("Home Tilt")

    def homeRot(_hr):
        _hr.loadParams(17,int(0))
        _hr.loadParams(18,int(1))
        print("Home Rot")
        
    def upload(_up):
        print("Uploading")

    def auto_connect(_cnt):
        _cnt.openCommPort(115200)
        _cnt.root.after(2000,_cnt.auto_connect)