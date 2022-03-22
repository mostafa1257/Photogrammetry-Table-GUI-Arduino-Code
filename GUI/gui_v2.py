
from phgui import *    

mode = IntVar()
duplex_mode = IntVar()
camera_placement = IntVar()
tilt_direction = IntVar()

d = True

def frontSelected():
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='green4')
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'red')

def topSelected():
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["front"]].configure(fg='red')
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["top"]].configure(fg = 'green4')

def fwdSelected():
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='green4')
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'red')

def bwdSelected():
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["forward"]].configure(fg='red')
    main.SETTINGS_RBUTTONS[gui_config["settings rbuttons indicies"]["backward"]].configure(fg = 'green4')

def stepModeSelected():
    for step_entry,step_label,cont_entry,cont_label in product(
        main.STEP_MODE_ENTRIES,
        main.STEP_MODE_LABELS,
        main.CONT_MODE_ENTRIES,
        main.CONT_MODE_LABELS):
        step_entry.configure(state=NORMAL)
        step_label.configure(bg="gray20")
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
        main.STEP_MODE_ENTRIES,
        main.STEP_MODE_LABELS,
        main.CONT_MODE_ENTRIES,
        main.CONT_MODE_LABELS):
        step_entry.configure(state=DISABLED)
        step_label.configure(bg="gray10")
        cont_entry.configure(state=NORMAL)
        cont_label.configure(bg="gray20")

    step_mode_enable_button.configure(fg="red")
    cont_mode_enable_button.configure(fg="green4")

    step_sub_frame.configure(bg = "gray10")
    cont_sub_frame.configure(bg="gray20" )

    global paramBuffer
    mode.set(0) 
    
def lockTilt():
    print("Lock Tilt")

def lockRot():
    print("Lock Rot")
    
def homeTilt():
    print("Home Tilt")

def homeRot():
    print("Home Rot")
    
def upload():
    print("Uploading")
    
def dummy():
    pass

def connect():
    print("connecting")
    
main = main_window()

cont = sub_window()
step = sub_window()
config = sub_window()
operation = sub_window()

tp = table_params(20)
funcs = [tp.validate,lockTilt,lockRot,homeTilt,homeRot,upload,dummy,connect]

""" Main Window Frame """
# Version
version_label = main.createLabel(main.root,"CamScan Tool v2.0",0,0).place(x=1450,y=870)

# Main Window Widgets
step_mode_enable_button = main.createRadioButton(main.root,"Step Mode",10,stepModeSelected,1,mode,0,0)
step_mode_enable_button.place(x=50,y=30)

duplex_mode_enable_button = main.createRadioButton(main.root,"Rotate Step Then Tilt Step",10,duplexModeSelected,1,duplex_mode,0,0)
duplex_mode_enable_button.place(x=200,y=30)

cont_mode_enable_button = main.createRadioButton(main.root,"Continous Mode",10,contModeSelected,0,mode,0,0)
cont_mode_enable_button.place(x=50,y=410)

presets_cycle_button = main.createButton(main.root,"Presets",2,10,1,"white","bisque4",5,tp.cyclePresets,None,None)
presets_cycle_button.place(x=1400,y=20)

main.MAIN_WINDOW_WIDGETS.append(main.createLabel(main.root,"Current Preset :",0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["current preset label"]].place(x=1250,y=30)

main.MAIN_WINDOW_WIDGETS.append(main.createLabel(main.root,str(tp.preset_ID),0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["current preset value"]].place(x=1365,y=30)

""" Continious Mode Frame """
cont_sub_frame = cont.drawSubWindow(50,450)
# Labels
for i in range(len(gui_config["cont mode labels"])):
    main.CONT_MODE_LABELS.append(cont.createLabel(cont_sub_frame,gui_config["cont mode labels"][i],i,0))

# Entries
for i in range(2):
    main.CONT_MODE_ENTRIES.append(cont.createEntry(cont_sub_frame,5,i,1))

""" Step Mode Frame """
step_sub_frame = step.drawSubWindow(50,70)
# Labels
for i in range(len(gui_config["step mode labels"])):
    main.STEP_MODE_LABELS.append(step.createLabel(step_sub_frame,gui_config["step mode labels"][i],i,0))

# Entries
for i in range(7):
    main.STEP_MODE_ENTRIES.append(step.createEntry(step_sub_frame,5,i,1))

""" General Settings Frame """
config_sub_frame = config.drawSubWindow(50,570)
# Labels
for i in range(len(gui_config["settings labels"])):
    main.SETTINGS_LABELS.append(config.createLabel(config_sub_frame,gui_config["settings labels"][i],i,0))

# Entries
for i in range(2,4):
    main.SETTINGS_ENTRIES.append(config.createEntry(config_sub_frame,5,i,1))

# Radio Buttons
main.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Front",10,frontSelected,2,camera_placement,0,1))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Top",10,topSelected,3,camera_placement,0,2))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Forward",10,fwdSelected,1,tilt_direction,1,1))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(config_sub_frame,"Backwards",10,bwdSelected,0,tilt_direction,1,2))

""" Command Buttons Frame """
buttons_sub_frame = operation.drawSubWindow(50,810)
# Buttons
for i in range(len(gui_config["operation buttons"])):
    main.OPERATION_BUTTONS.append(operation.createButton(buttons_sub_frame,gui_config["operation buttons"][i],5,20,None,"white","gray50",1,funcs[i],0,i))

tp.loadPresetData()
main.openMainWindow()