from os import stat
from sre_parse import State
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
from itertools import product

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
            
    def openMainWindow(_gui):
        # Opens Main GUI Window
        _gui.root.configure(bg=_gui.bkgnd_CLR)
        _gui.root.geometry(_gui.win_SIZE)
        _gui.root.resizable(False, False)
        _gui.root.title("CamScan Tool v2.0")
            
        _gui.root.mainloop()  

    def drawLabel(_lbl,parent_frame,txt,gy,gx):
        _lbl.label = Label(parent_frame,text=txt,font=3,bg=_lbl.bkgnd_CLR,fg=_lbl.txt_CLR)         
        _lbl.label.grid(row=gy, column=gx) 

        return _lbl.label

    def drawEntry(_ent,parent_frame,w,gy,gx):
        _ent.entry = Entry(parent_frame,width=w,font=3,disabledbackground="gray50")
        _ent.entry.grid(row=gy,column=gx,padx=5,pady=10)

        return _ent.entry

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

    def drawSubWindow(_sub,px,py):
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
        _file.preset_ID = 1 

        return _file.presets_FILE

mode = IntVar()
duplex_mode = IntVar()
camera_placement = IntVar()
tilt_direction = IntVar()

d = True

presets_file_path = r'D:\Photogrammetry-Table-GUI-Arduino-Code\Presets.xlsx'

def frontSelected():
    SETTINGS_RBUTTONS[0].configure(fg='green4')
    SETTINGS_RBUTTONS[1].configure(fg = 'red')

def topSelected():
    SETTINGS_RBUTTONS[0].configure(fg='red')
    SETTINGS_RBUTTONS[1].configure(fg = 'green4')

def fwdSelected():
    SETTINGS_RBUTTONS[2].configure(fg='green4')
    SETTINGS_RBUTTONS[3].configure(fg = 'red')

def bwdSelected():
    SETTINGS_RBUTTONS[2].configure(fg='red')
    SETTINGS_RBUTTONS[3].configure(fg = 'green4')

def stepModeSelected():
    for step_entry,step_label,cont_entry,cont_label in product(
        STEP_MODE_ENTRIES,
        STEP_MODE_LABELS,
        CONT_MODES_ENTRIES,
        CONT_MODE_LABELS):
        step_entry.configure(state=NORMAL)
        step_label.configure(bg="gray10")
        cont_entry.configure(state=DISABLED)
        cont_label.configure(bg="gray10")

    step_mode_enable_button.configure(fg="green4")
    cont_mode_enable_button.configure(fg="red")

    step_sub_frame.configure(bg="gray20")
    cont_sub_frame.configure(bg="gray10" )

def duplexModeSelected():
    global d
    d = not d
    duplex_mode.set(d)
    if d == True:
        duplex_mode_enable_button.configure(fg = "green4")
    if d == False:
        duplex_mode_enable_button.configure(fg = "red")

def contModeSelected():
    for step_entry,step_label,cont_entry,cont_label in product(
        STEP_MODE_ENTRIES,
        STEP_MODE_LABELS,
        CONT_MODES_ENTRIES,
        CONT_MODE_LABELS):
        step_entry.configure(state=DISABLED)
        step_label.configure(bg="gray10")
        cont_entry.configure(state=NORMAL)
        cont_label.configure(bg="gray10")

    step_mode_enable_button.configure(fg="red")
    cont_mode_enable_button.configure(fg="green4")

    step_sub_frame.configure(bg = "gray10")
    cont_sub_frame.configure(bg="gray20" )

    global paramBuffer
    mode.set(0)
    
prst = presets(presets_file_path,'Presets')  
prst_file = prst.openPresetsFile()  
main = main_window()

cont = sub_window()
step = sub_window()
config = sub_window()

""" Main Window Frame """
# Version
version_label = main.drawLabel(main.root,"CamScan Tool v2.0",0,0)
version_label.place(x=1450,y=870)

# Main Window Widgets
step_mode_enable_button = main.createRadioButton(main.root,"Step Mode",10,stepModeSelected,1,mode,0,0).place(x=50,y=30)
duplex_mode_enable_button = main.createRadioButton(main.root,"Rotate Step Then Tilt Step",duplexModeSelected,10,1,duplex_mode,0,0).place(x=200,y=30)
cont_mode_enable_button = main.createRadioButton(main.root,"Continous Mode",10,contModeSelected,0,mode,0,0).place(x=50,y=410)

current_preset_label = main.drawLabel(main.root,"Current Preset :",0,0).place(x=1250,y=30)
current_preset = main.drawLabel(main.root,str(prst.preset_ID),0,0).place(x=1365,y=30)

""" Continious Mode Frame """
cont_sub_frame = cont.drawSubWindow(50,450)
# Labels
CONT_MODE_LABELS = []

CONT_MODE_LABELS.append(cont.drawLabel(cont_sub_frame,"Rotation Time (min:1s)",0,0))
CONT_MODE_LABELS.append(cont.drawLabel(cont_sub_frame,"Rotation Angel (max:360°)",1,0))

# Entries
CONT_MODES_ENTRIES = []

CONT_MODES_ENTRIES.append(cont.drawEntry(cont_sub_frame,5,0,1))
CONT_MODES_ENTRIES.append(cont.drawEntry(cont_sub_frame,5,1,1))

""" Step Mode Frame """
step_sub_frame = step.drawSubWindow(50,70)
# Labels
STEP_MODE_LABELS = []

STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Rotation Step Angle (Max: 45°)",0,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Rotation Angle (Max: 360°)",1,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Tilt Step Angle (Max: 45°)",2,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Tilt Rotation Angle (Max: 90°)",3,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Delay Between Steps (min:1s)",4,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Home Tilt (-90°~+90)",5,0))
STEP_MODE_LABELS.append(step.drawLabel(step_sub_frame,"Home Rotation (0°~360°)",6,0))

# Entries
STEP_MODE_ENTRIES = []
for i in range(0,7):
    STEP_MODE_ENTRIES.append(step.drawEntry(step_sub_frame,5,i,1))

""" General Settings Frame """
config_sub_frame = config.drawSubWindow(50,570)
# Labels
SETTINGS_LABELS = []

SETTINGS_LABELS.append(config.drawLabel(config_sub_frame,"Camera Position",0,0))
SETTINGS_LABELS.append(config.drawLabel(config_sub_frame,"Tilt Direction",1,0))
SETTINGS_LABELS.append(config.drawLabel(config_sub_frame,"Rotation Speed (Max: 100°/s)",2,0))
SETTINGS_LABELS.append(config.drawLabel(config_sub_frame,"Tilt Speed (Max: 100°/s)",3,0))

# Entries
SETTINGS_ENTRIES = []

SETTINGS_ENTRIES.append(config.drawEntry(config_sub_frame,5,2,1))
SETTINGS_ENTRIES.append(config.drawEntry(config_sub_frame,5,3,1))

# Radio Buttons
SETTINGS_RBUTTONS = []

SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Front",10,frontSelected,2,camera_placement,0,1))
SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Top",10,topSelected,3,camera_placement,0,2))
SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Forward",10,fwdSelected,1,tilt_direction,1,1))
SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Backwards",10,bwdSelected,0,tilt_direction,1,2))

main.openMainWindow()