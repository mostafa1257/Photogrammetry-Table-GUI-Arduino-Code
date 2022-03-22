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

class main_window:
    root = Tk()
    
    STEP_MODE_LABELS = []
    STEP_MODE_ENTRIES = []
    CONT_MODE_LABELS = []
    CONT_MODE_ENTRIES = []
    SETTINGS_LABELS = []
    SETTINGS_ENTRIES = []
    SETTINGS_RBUTTONS = []
    
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
    
    def createButton(_but,parent_frame,txt,fnt,w,h,fgc,bgc,bw,cmd,gy,gx,cs):
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
        _but.button.grid(row=gy,column=gx,columnspan=cs)
        
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

mode = IntVar()
duplex_mode = IntVar()
camera_placement = IntVar()
tilt_direction = IntVar()

d = True

def cyclePresets():
    tp.clearPresetData()
    if tp.preset_ID >= tp.presets_NUM:
        tp.preset_ID = 0
    tp.loadPresetData()
    tp.preset_ID += 1
    print(tp.preset_ID)

def frontSelected():
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='green4')
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'red')

def topSelected():
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='red')
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'green4')

def fwdSelected():
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='green4')
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'red')

def bwdSelected():
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='red')
    main_window.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'green4')

def stepModeSelected():
    for step_entry,step_label,cont_entry,cont_label in product(
        main_window.STEP_MODE_ENTRIES,
        main_window.STEP_MODE_LABELS,
        main_window.CONT_MODE_ENTRIES,
        main_window.CONT_MODE_LABELS):
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
        main_window.STEP_MODE_ENTRIES,
        main_window.STEP_MODE_LABELS,
        main_window.CONT_MODE_ENTRIES,
        main_window.CONT_MODE_LABELS):
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

main = main_window()

cont = sub_window()
step = sub_window()
config = sub_window()

tp = table_params(20)

""" Main Window Frame """
# Version
version_label = main.createLabel(main.root,"CamScan Tool v2.0",0,0)
version_label.place(x=1450,y=870)

# Main Window Widgets
step_mode_enable_button = main.createRadioButton(main.root,"Step Mode",10,stepModeSelected,1,mode,0,0).place(x=50,y=30)
duplex_mode_enable_button = main.createRadioButton(main.root,"Rotate Step Then Tilt Step",duplexModeSelected,10,1,duplex_mode,0,0).place(x=200,y=30)
cont_mode_enable_button = main.createRadioButton(main.root,"Continous Mode",10,contModeSelected,0,mode,0,0).place(x=50,y=410)

presets_cycle_button = main.createButton(main.root,"Presets",2,10,1,"white","bisque4",5,cyclePresets,None,None,None).place(x=1400,y=20)

current_preset_label = main.createLabel(main.root,"Current Preset :",0,0).place(x=1250,y=30)
current_preset = main.createLabel(main.root,str(tp.preset_ID),0,0).place(x=1365,y=30)

""" Continious Mode Frame """
cont_sub_frame = cont.drawSubWindow(50,450)
# Labels
for i in range(len(gui_config["cont mode labels"])):
    main_window.CONT_MODE_LABELS.append(cont.createLabel(cont_sub_frame,gui_config["cont mode labels"][i],i,0))

# Entries
for i in range(2):
    main_window.CONT_MODE_ENTRIES.append(cont.createEntry(cont_sub_frame,5,i,1))

""" Step Mode Frame """
step_sub_frame = step.drawSubWindow(50,70)
# Labels
for i in range(len(gui_config["step mode labels"])):
    main_window.STEP_MODE_LABELS.append(step.createLabel(step_sub_frame,gui_config["step mode labels"][i],i,0))

# Entries
for i in range(7):
    main_window.STEP_MODE_ENTRIES.append(step.createEntry(step_sub_frame,5,i,1))

""" General Settings Frame """
config_sub_frame = config.drawSubWindow(50,570)
# Labels
for i in range(len(gui_config["settings labels"])):
    main_window.SETTINGS_LABELS.append(config.createLabel(config_sub_frame,gui_config["settings labels"][i],i,0))

# Entries
for i in range(2,4):
    main_window.SETTINGS_ENTRIES.append(config.createEntry(config_sub_frame,5,i,1))

# Radio Buttons
main_window.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Front",10,frontSelected,2,camera_placement,0,1))
main_window.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Top",10,topSelected,3,camera_placement,0,2))
main_window.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Forward",10,fwdSelected,1,tilt_direction,1,1))
main_window.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Backwards",10,bwdSelected,0,tilt_direction,1,2))

tp.loadPresetData()

main.openMainWindow()