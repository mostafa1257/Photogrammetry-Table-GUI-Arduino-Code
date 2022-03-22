from phgui import *    
    
main = main_window()
cont = sub_window()
step = sub_window()
config = sub_window()
operation = sub_window()

tp = table_params(20)

def updateImage():
    os.chdir("D:\\Photogrammetry-Table-GUI-Arduino-Code\\test images\\")
    try:
        image = Image.open(os.listdir()[-1])
        resize_image = image.resize((1150, 647))
        img = ImageTk.PhotoImage(resize_image)
        image_frame = Label(image=img, borderwidth=2, relief="groove")
        image_frame.image = img
        image_frame.place(x=700, y=100)
    except:
        print("folder is empty")

    main.root.after(1000, updateImage)

funcs = [tp.validate,tp.lockTilt,tp.lockRot,tp.homeTilt,tp.homeRot,tp.upload,tp.dummy,tp.connect]

""" Main Window Frame """
# Version
version_label = main.createLabel(main.root,"CamScan Tool v2.10",0,0).place(x=1710,y=970)

# Main Window Widgets
main.MAIN_WINDOW_WIDGETS.append(main.createRadioButton(main.root,"Step Mode",10,tp.stepModeSelected,1,tp.mode,0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["step mode select button"]].place(x=50,y=30)

main.MAIN_WINDOW_WIDGETS.append(main.createRadioButton(main.root,"Rotate Step Then Tilt Step",10,tp.duplexModeSelected,1,tp.duplex_mode,0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["duplex mode select button"]].place(x=200,y=30)

main.MAIN_WINDOW_WIDGETS.append(main.createRadioButton(main.root,"Continous Mode",10,tp.contModeSelected,0,tp.mode,0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["cont mode select button"]].place(x=50,y=440)

main.MAIN_WINDOW_WIDGETS.append(main.createButton(main.root,"Presets",2,10,1,"white","bisque4",5,tp.cyclePresets,None,None))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["preset cycle button"]].place(x=1750,y=20)

main.MAIN_WINDOW_WIDGETS.append(main.createLabel(main.root,"Current Preset :",0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["current preset label"]].place(x=1550,y=30)

main.MAIN_WINDOW_WIDGETS.append(main.createLabel(main.root,str(tp.preset_ID),0,0))
main.MAIN_WINDOW_WIDGETS[gui_config["main window widgets indicies"]["current preset value"]].place(x=1715,y=30)

""" Step Mode Frame """
main.SUB_WINDOWS.append(step.createSubWindow(50,70))
# Labels
for i in range(len(gui_config["step mode labels"])):
    main.STEP_MODE_LABELS.append(step.createLabel(main.SUB_WINDOWS[gui_config["sub window indicies"]["step mode sub window"]],gui_config["step mode labels"][i],i,0))

# Entries
for i in range(7):
    main.STEP_MODE_ENTRIES.append(step.createEntry(main.SUB_WINDOWS[gui_config["sub window indicies"]["step mode sub window"]],5,i,1))

""" Continious Mode Frame """
main.SUB_WINDOWS.append(cont.createSubWindow(50,480))
# Labels
for i in range(len(gui_config["cont mode labels"])):
    main.CONT_MODE_LABELS.append(cont.createLabel(main.SUB_WINDOWS[gui_config["sub window indicies"]["cont mode sub window"]],gui_config["cont mode labels"][i],i,0))

# Entries
for i in range(2):
    main.CONT_MODE_ENTRIES.append(cont.createEntry(main.SUB_WINDOWS[gui_config["sub window indicies"]["cont mode sub window"]],5,i,1))

""" Configuration Window """
main.SUB_WINDOWS.append(config.createSubWindow(50,600))
# Labels
for i in range(len(gui_config["settings labels"])):
    main.SETTINGS_LABELS.append(config.createLabel(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],gui_config["settings labels"][i],i,0))

# Entries
for i in range(2,4):
    main.SETTINGS_ENTRIES.append(config.createEntry(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],5,i,1))

# Radio Buttons
main.SETTINGS_RBUTTONS.append(config.createRadioButton(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],"Front",10,tp.frontSelected,2,tp.camera_placement,0,1))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],"Top",10,tp.topSelected,3,tp.camera_placement,0,2))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],"Forward",10,tp.fwdSelected,1,tp.tilt_direction,1,1))
main.SETTINGS_RBUTTONS.append(config.createRadioButton(main.SUB_WINDOWS[gui_config["sub window indicies"]["config sub window"]],"Backwards",10,tp.bwdSelected,0,tp.tilt_direction,1,2))

""" Operations Window """
main.SUB_WINDOWS.append(operation.createSubWindow(50,900))
# Buttons
for i in range(len(gui_config["operation buttons"])):
    main.OPERATION_BUTTONS.append(operation.createButton(main.SUB_WINDOWS[gui_config["sub window indicies"]["operation sub window"]],gui_config["operation buttons"][i],5,18,None,"white","gray50",1,funcs[i],0,i))

tp.loadPresetData()
main.root.after(1000, updateImage)
main.openMainWindow()