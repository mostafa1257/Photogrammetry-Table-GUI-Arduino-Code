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


# GUI Parameters
WINDOW_SIZE = "1600x900"
TEXT_COLOR = "white"
BACKGROUND_COLOR = "gray10"

connected = False
validated = False

# Serial Port Parameters
BAUD = 115200
TIMEOUT = 0.2
uart = 0 
# Parameters Buffer
paramBuffer = [None]*20

def loadParams(pos,data):
    global paramBuffer
    paramBuffer[pos] = int(data)

def serial_ports():
    if sys.platform.startswith("win"):
        ports = ["COM%s" % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


uart = serial.Serial(str(serial_ports()[0]), baudrate=BAUD, timeout=TIMEOUT)
presets_file = pd.read_excel(r'D:\kamscan presets\Presets.xlsx',index_col= 'Presets')
presets_numbers = presets_file.shape[0]
preset_id = 1

# Root
root = Tk()
root.configure(bg=BACKGROUND_COLOR)
root.geometry(WINDOW_SIZE)
root.resizable(False, False)
root.title("CamScan Tool v2.0")

version_label = Label(
    root,
    text="CamScan Tool v2.0",
    bg=BACKGROUND_COLOR, 
    fg=TEXT_COLOR
)
version_label.place(x=1490, y=880)

mode = IntVar()
duplexMode = IntVar()
d = True
"""----------------------------------------------------------------------------------"""
# Step Mode Frame
"""----------------------------------------------------------------------------------"""
def loadPresetData(id):
    yaw_step_angle.insert(0,presets_file.iloc[id]["Rotation Step Angle"])
    yaw_rotation_angle.insert(0,presets_file.iloc[id]["Rotation Angle"])
    roll_step_angle.insert(0,presets_file.iloc[id]["Tilt Step Angle"])
    roll_rotation_angle.insert(0,presets_file.iloc[id]["Tilt Rotation Angle"])
    delay_between_steps.insert(0,presets_file.iloc[id]["Delay Between Steps"])
    home_yaw.insert(0,presets_file.iloc[id]["Home Rotation"])
    home_roll.insert(0,presets_file.iloc[id]["Home Tilt"])
    yaw_speed_set.insert(0,presets_file.iloc[id]["Rotation Speed"])
    roll_speed_set.insert(0,presets_file.iloc[id]["Tilt Speed"])
    yaw_rotation_time.insert(0,presets_file.iloc[id]["Rotation Time"])
    yaw_rotation_angle_c.insert(0,presets_file.iloc[id]["Rotation Angle (cont)"])

    

def clearPresetData():
    yaw_step_angle.delete(0,END)
    yaw_rotation_angle.delete(0,END)
    roll_step_angle.delete(0,END)
    roll_rotation_angle.delete(0,END)
    delay_between_steps.delete(0,END)
    home_yaw.delete(0,END)
    home_roll.delete(0,END)
    yaw_speed_set.delete(0,END)
    roll_speed_set.delete(0,END)
    yaw_rotation_time.delete(0,END)
    yaw_rotation_angle_c.delete(0,END)

def cycleStepPresets():
    clearPresetData()
    global presets_numbers,preset_id
    if preset_id >= presets_numbers:
        preset_id = 0
    loadPresetData(preset_id)
    current_preset.configure(text=str(preset_id + 1))
    preset_id += 1
    

def stepModeSelected():
    yaw_step_angle.configure(state=NORMAL)
    yaw_rotation_angle.configure(state=NORMAL)
    roll_step_angle.configure(state=NORMAL)
    roll_rotation_angle.configure(state=NORMAL)
    delay_between_steps.configure(state=NORMAL)
    home_roll.configure(state=NORMAL)
    home_yaw.configure(state=NORMAL)
    step_mode_enable_button.configure(fg="green4")
    continuous_mode_enable_button.configure(fg = "red")

    yaw_rotation_time.configure(state=DISABLED)
    yaw_rotation_angle_c.configure(state=DISABLED)

    step_mode_frame.configure(bg = "gray20")

    yaw_step_angel_label.configure(bg = "gray20")
    yaw_rotation_angel_label.configure(bg = "gray20")
    roll_step_angel_label.configure(bg = "gray20")
    roll_rotation_angel_label.configure(bg = "gray20")
    delay_between_steps_label.configure(bg = "gray20")
    home_yaw_label.configure(bg = "gray20")
    home_roll_label.configure(bg = "gray20")

    continuous_mode_frame.configure(bg="gray10" )
    yaw_rotation_angle_c_label.configure(bg = "gray10")
    yaw_rotation_time_label.configure(bg = "gray10")

    global paramBuffer
    mode.set(1)

def duplexModeSelected():
    global d
    d = not d
    duplexMode.set(d)
    if d == True:
        duplex_mode_enable_button.configure(fg = "green4")
    if d == False:
        duplex_mode_enable_button.configure(fg = "red")
    
step_mode_enable_button = Radiobutton(
    root,
    text="Step Mode",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    command=stepModeSelected,
    value=1,
    variable=mode

)
step_mode_enable_button.place(x=50, y=30)

duplex_mode_enable_button = Radiobutton(
    root,
    text="Rotate Step Then Tilt Step",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    command=duplexModeSelected,
    value=1,
    variable=duplexMode

)
duplex_mode_enable_button.place(x=200, y=30)

current_preset_label = Label(
    root,
    text = "Current Preset :",
    font = 10,
    bg = BACKGROUND_COLOR,
    fg = TEXT_COLOR
)
current_preset_label.place(x=1250,y=30)

current_preset = Label(
    root,
    text = str(preset_id),
    font = 10,
    bg = BACKGROUND_COLOR,
    fg = "green2"
)
current_preset.place(x=1365,y = 30)

step_mode_presets_cycle_button = Button(
    root,
    text="Presets",
    font=2,
    fg="white",
    bg="bisque4",
    width=10,
    height=1,
    borderwidth=5,
    command = cycleStepPresets
)
step_mode_presets_cycle_button.place(x=1400, y=20)

step_mode_frame = Frame(
    root,
    padx=5,
    pady=5,
    borderwidth=5,
    relief="groove",
    bg=BACKGROUND_COLOR
)
step_mode_frame.place(x=50, y=70)

yaw_step_angel_label = Label(
    step_mode_frame,
    text="Rotation Step Angle (Max: 45°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
yaw_step_angel_label.grid(row=0, column=0)
yaw_step_angle = Entry(step_mode_frame,
width=5,
font=3,
disabledbackground="gray80"
)
yaw_step_angle.grid(row=0, column=1, padx=5, pady=10)

yaw_rotation_angel_label = Label(
    step_mode_frame,
    text="Rotation Angle (Max: 360°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
yaw_rotation_angel_label.grid(row=1, column=0)
yaw_rotation_angle = Entry(
    step_mode_frame,
    width=5,
    font=3,
    disabledbackground="gray80"
)
yaw_rotation_angle.grid(row=1, column=1, padx=5, pady=10)

roll_step_angel_label = Label(
    step_mode_frame,
    text="Tilt Step Angle (Max: 45°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
roll_step_angel_label.grid(row=2, column=0)
roll_step_angle = Entry(step_mode_frame,
width=5,
font=3,
disabledbackground="gray80"
)
roll_step_angle.grid(row=2, column=1, padx=5, pady=10)

roll_rotation_angel_label = Label(
    step_mode_frame,
    text="Tilt Rotation Angle (Max: 90°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
roll_rotation_angel_label.grid(row=3, column=0)
roll_rotation_angle = Entry(
    step_mode_frame,
    width=5,
    font=3,
    disabledbackground="gray80"
)
roll_rotation_angle.grid(row=3, column=1, padx=5, pady=10)

delay_between_steps_label = Label(
    step_mode_frame,
    text="Delay Between Steps (min:1s)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
delay_between_steps_label.grid(row=4, column=0)
delay_between_steps = Entry(
    step_mode_frame,
    width=5,
    font=3,
    disabledbackground="gray80"
)
delay_between_steps.grid(row=4, column=1, padx=5, pady=10)

home_roll_label = Label(
    step_mode_frame,
    text="Home Tilt (-90°~+90)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
home_roll_label.grid(row=5, column=0)
home_roll = Entry(step_mode_frame,
width=5,
font=3,
disabledbackground="gray80"
)
home_roll.grid(row=5, column=1, padx=5, pady=10)

home_yaw_label = Label(
    step_mode_frame,
    text="Home Rotation (0°~360°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
home_yaw_label.grid(row=6, column=0)
home_yaw = Entry(step_mode_frame,
width=5,
font=3,
disabledbackground="gray80"
)
home_yaw.grid(row=6, column=1, padx=5, pady=10)
"""----------------------------------------------------------------------"""
# Continous Mode Frame
"""----------------------------------------------------------------------"""
def continuousModeSelected():
    yaw_step_angle.configure(state=DISABLED)
    yaw_rotation_angle.configure(state=DISABLED)
    roll_step_angle.configure(state=DISABLED)
    roll_rotation_angle.configure(state=DISABLED)
    delay_between_steps.configure(state=DISABLED)
    home_roll.configure(state=DISABLED)
    home_yaw.configure(state=DISABLED)
    step_mode_enable_button.configure(fg="red")
    continuous_mode_enable_button.configure(fg = "green4")

    yaw_rotation_time.configure(state=NORMAL)
    yaw_rotation_angle_c.configure(state=NORMAL)

    step_mode_frame.configure(bg = "gray10")
    
    continuous_mode_frame.configure(bg="gray20" )
    yaw_rotation_angle_c_label.configure(bg = "gray20")
    yaw_rotation_time_label.configure(bg = "gray20")

    yaw_step_angel_label.configure(bg = "gray10")
    yaw_rotation_angel_label.configure(bg = "gray10")
    roll_step_angel_label.configure(bg = "gray10")
    roll_rotation_angel_label.configure(bg = "gray10")
    delay_between_steps_label.configure(bg = "gray10")
    home_yaw_label.configure(bg = "gray10")
    home_roll_label.configure(bg = "gray10")

    global paramBuffer
    mode.set(0)

continuous_mode_enable_button = Radiobutton(
    root,
    text="Continuous Mode",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    command=continuousModeSelected,
    value = 0,
    variable=mode
)
continuous_mode_enable_button.place(x=50, y=410)

continuous_mode_frame = Frame(
    root, padx=5, pady=5, borderwidth=5, relief="groove", bg=BACKGROUND_COLOR
)
continuous_mode_frame.place(x=50, y=450)

yaw_rotation_time_label = Label(
    continuous_mode_frame,
    text="Rotation Time (min:1s)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
yaw_rotation_time_label.grid(row=0, column=0)
yaw_rotation_time = Entry(
    continuous_mode_frame,
    width=5,
    font=3,
    disabledbackground="gray80"
)
yaw_rotation_time.grid(row=0, column=1, padx=5, pady=10)

yaw_rotation_angle_c_label = Label(
    continuous_mode_frame,
    text="Rotation Angel (max:360°)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
yaw_rotation_angle_c_label.grid(row=1, column=0)
yaw_rotation_angle_c = Entry(
    continuous_mode_frame,
    width=5,
    font=3,
    disabledbackground="gray80"
)
yaw_rotation_angle_c.grid(row=1, column=1, padx=5, pady=10)
"""----------------------------------------------------------------------------------"""
# General Settings Frame
"""----------------------------------------------------------------------------------"""
camera_placement = IntVar()
roll_direction = IntVar()

def frontSelected():
    camera_position_select_front_button.configure(fg='green4')
    camera_position_select_top_button.configure(fg = 'red')

def topSelected():
    camera_position_select_front_button.configure(fg='red')
    camera_position_select_top_button.configure(fg = 'green4')

def fwdSelected():
    roll_cw_select_button.configure(fg='green4')
    roll_ccw_select_button.configure(fg = 'red')

def bwdSelected():
    roll_cw_select_button.configure(fg='red')
    roll_ccw_select_button.configure(fg = 'green4')

general_settings_frame = Frame(
    root, padx=5, pady=5, borderwidth=0, relief="groove", bg=BACKGROUND_COLOR
)
general_settings_frame.place(x=50, y=570)

camera_position_select_label = Label(
    general_settings_frame,
    text="Camera Position:",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
camera_position_select_label.grid(row=0, column=0)

camera_position_select_front_button = Radiobutton(
    general_settings_frame,
    text="Front",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    activebackground=BACKGROUND_COLOR,
    activeforeground=TEXT_COLOR,
    value=2,
    variable = camera_placement,
    command=frontSelected
)
camera_position_select_front_button.grid(row=0, column=1)

camera_position_select_top_button = Radiobutton(
    general_settings_frame,
    text="TOP",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    activebackground=BACKGROUND_COLOR,
    activeforeground=TEXT_COLOR,
    value=3,
    variable=camera_placement,
    command=topSelected
)
camera_position_select_top_button.grid(row=0, column=2)

roll_direction_select_label = Label(
    general_settings_frame,
    text="Tilt Direction:",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
roll_direction_select_label.grid(row=1, column=0)

roll_cw_select_button = Radiobutton(
    general_settings_frame,
    text="Forward",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    activebackground=BACKGROUND_COLOR,
    activeforeground=TEXT_COLOR,
    value=1,
    variable = roll_direction,
    command=fwdSelected
)
roll_cw_select_button.grid(row=1, column=1)

roll_ccw_select_button = Radiobutton(
    general_settings_frame,
    text="Backward",
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR,
    font=10,
    activebackground=BACKGROUND_COLOR,
    activeforeground=TEXT_COLOR,
    value=0,
    variable = roll_direction,
    command=bwdSelected
)
roll_ccw_select_button.grid(row=1, column=2)

yaw_speed_set_label = Label(
    general_settings_frame,
    text="Rotation Speed (Max: 100°/s)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
yaw_speed_set_label.grid(row=2, column=0)
yaw_speed_set = Entry(
    general_settings_frame,
    width=5,
    font=3,
    disabledbackground="gray50"
)
yaw_speed_set.grid(row=2, column=1, padx=5, pady=10)

roll_speed_set_label = Label(
    general_settings_frame,
    text="Tilt Speed (Max: 100°/s)",
    font=3,
    bg=BACKGROUND_COLOR,
    fg=TEXT_COLOR
)
roll_speed_set_label.grid(row=3, column=0)
roll_speed_set = Entry(
    general_settings_frame,
    width=5,
    font=3,
    disabledbackground="gray50"
)
roll_speed_set.grid(row=3, column=1, padx=5, pady=10)
"""----------------------------------------------------------------------"""
# Validation
"""----------------------------------------------------------------------"""
validation = {
    "max_yaw_step_angle":45,"min_yaw_step_angle":1,
    "max_yaw_rotation_angle":360,"min_yaw_rotation_angle":0,
    "max_roll_step_angle":45,"min_roll_step_angle":1,
    "max_roll_rotation_angle":90,"min_roll_rotation_angle":0,
    "max_yaw_home":360,"min_yaw_home":0,
    "max_cont_angle":360,"min_cont_angle":0,
    "max_motor_speed":100,"min_motor_speed":10,
    "max_roll_home":90,
    "min_cont_time":1,
    "min_delay_between_steps":1,
    
    }
def validate():
    if(
        (int(yaw_step_angle.get()) <= validation["max_yaw_step_angle"] and int(yaw_step_angle.get()) >= validation["min_yaw_step_angle"]) and
        (int(yaw_rotation_angle.get()) <= validation["max_yaw_rotation_angle"] and int(yaw_rotation_angle.get()) >= validation["min_yaw_rotation_angle"]) and
        ((int(yaw_rotation_angle.get()) % int(yaw_step_angle.get())) == 0) and
        (int(roll_step_angle.get()) <= validation["max_roll_step_angle"] and int(roll_step_angle.get()) >= validation["min_roll_step_angle"]) and
        (int(roll_rotation_angle.get()) <= validation["max_roll_rotation_angle"] and int(roll_rotation_angle.get()) >= validation["min_roll_rotation_angle"]) and
        ((int(roll_rotation_angle.get()) % int(roll_step_angle.get())) == 0) and
        (int(home_yaw.get()) <= validation["max_yaw_home"] and int(home_yaw.get()) >= validation["min_yaw_home"]) and
        (int(yaw_rotation_angle_c.get()) <= validation["max_cont_angle"] and int(yaw_rotation_angle_c.get()) >= validation["min_cont_angle"]) and
        (int(yaw_speed_set.get()) <= validation["max_motor_speed"] and int(yaw_speed_set.get()) >= validation["min_motor_speed"]) and
        (int(roll_speed_set.get()) <= validation["max_motor_speed"] and int(roll_speed_set.get()) >= validation["min_motor_speed"]) and

        (int(home_roll.get()) <= validation["max_roll_home"]) and
        (int(yaw_rotation_time.get()) >= validation["min_cont_time"]) and 
        (int(delay_between_steps.get()) >= validation["min_delay_between_steps"])
      ):

        global validated,connected,paramBuffer

        # loadParams(0,mode.get())
        # loadParams(1,yaw_step_angle.get())
        # loadParams(2,yaw_rotation_angle.get())
        # loadParams(3,roll_step_angle.get())
        # loadParams(4,roll_rotation_angle.get())
        # loadParams(5,delay_between_steps.get())
        # loadParams(6,home_roll.get())
        # loadParams(7,home_yaw.get())
        # loadParams(8,yaw_rotation_time.get())
        # loadParams(9,yaw_rotation_angle_c.get())
        # loadParams(10,camera_placement.get())
        # loadParams(11,roll_direction.get())
        # loadParams(12,yaw_speed_set.get())
        # loadParams(13,roll_speed_set.get())
        # loadParams(14,duplexMode.get())
        loadParams(15,int(lr))
        loadParams(16,int(ly))
        loadParams(17,1)
        loadParams(18,1)

        loadParams(19,0)
        
        validated = True

        validate_button.configure(bg="dodger blue")
        print("Validated")
        print(paramBuffer)
    else:
        validated = False
        validate_button.configure(bg="red")
        print("Error")
    if validated and connected:
        upload_button.configure(state=NORMAL)
    else:
        upload_button.configure(state=DISABLED)
"""----------------------------------------------------------------------------------"""
# Buttons Frame
"""----------------------------------------------------------------------------------"""
lr = True
ly = True

def lockRoll():
    global lr
    lr = not lr
    loadParams(15,int(lr))
    loadParams(17,int(0))
    loadParams(18,int(0))
    upload(0)

def lockYaw():
    global ly
    ly = not ly
    loadParams(16,int(ly))
    loadParams(17,int(0))
    loadParams(18,int(0))
    upload(0)

def homeRoll():
    loadParams(17,int(1))
    loadParams(18,int(0))
    upload(0)

def homeYaw():
    loadParams(17,int(0))
    loadParams(18,int(1))
    upload(0)


buttons_frame = Frame(
    root, padx=5, pady=5, borderwidth=0, relief="groove", bg=BACKGROUND_COLOR
)
buttons_frame.place(x=50, y=730)

validate_button = Button(
    buttons_frame,
    text="Validate & save",
    font=5,
    fg="white",
    bg="red",
    width=22,
    borderwidth=5,
    command=validate
)
validate_button.grid(row=0, column=0, columnspan=2)

lock_roll_motor_button = Button(
    buttons_frame,
    text="Lock Tilt",
    font=5,
    fg="white",
    bg="gray50",
    width=10,
    borderwidth=4,
    state=DISABLED,
    command=lockRoll
)
lock_roll_motor_button.grid(row=1, column=0)

lock_yaw_motor_button = Button(
    buttons_frame,
    text="Lock Rotation",
    font=5,
    fg="white",
    bg="gray50",
    width=10,
    borderwidth=4,
    state=DISABLED,
    command = lockYaw
)
lock_yaw_motor_button.grid(row=1, column=1)

home_roll_axis_button = Button(
    buttons_frame,
    text="Home Tilt",
    font=5,
    fg="white",
    bg="gray50",
    width=10,
    borderwidth=4,
    state=DISABLED,
    command=homeRoll
)
home_roll_axis_button.grid(row=2, column=0)

home_yaw_axis_button = Button(
    buttons_frame,
    text="Home Rot",
    font=5,
    fg="white",
    bg="gray50",
    width=10,
    borderwidth=4,
    state=DISABLED,
    command=homeYaw
)
home_yaw_axis_button.grid(row=2, column=1)

def upload(af):
    uart = serial.Serial(str(serial_ports()[0]), baudrate=BAUD, timeout=TIMEOUT)
    loadParams(19,af)
    time.sleep(2)
    buf = []
    for d in paramBuffer:
        buf.append(struct.pack(">H",d))
    for b in buf:
        uart.write(b)
        #time.sleep(0.1)        
    root.after(1000, updateImage)
    print(paramBuffer)

def updateImage():
    os.chdir("C:\\Users\\DR. mostafa\\Pictures\\digiCamControl\\Session1\\")
    try:
        image = Image.open(os.listdir()[-1])
        resize_image = image.resize((1100, 619))
        img = ImageTk.PhotoImage(resize_image)
        image_frame = Label(image=img, borderwidth=2, relief="groove")
        image_frame.image = img
        image_frame.place(x=470, y=100)
    except:
        print("folder is empty")

    root.after(1000, updateImage)

upload_button = Button(
    buttons_frame,
    text="Upload & Start",
    font=5,
    fg="white",
    bg="gray50",
    width=22,
    borderwidth=5,
    state=DISABLED,
    command = lambda:upload(255)
)
upload_button.grid(row=3, column=0, columnspan=2)

def connect():
    try:
        uart = serial.Serial(str(serial_ports()[0]), baudrate=BAUD, timeout=TIMEOUT)

        global connected,validated

        connected = True

        connect_button.configure(bg='green3',text="Connected")

        lock_roll_motor_button.configure(bg="dodger blue",state=NORMAL)
        lock_yaw_motor_button.configure(bg="dodger blue",state=NORMAL)
        home_yaw_axis_button.configure(bg="dodger blue",state=NORMAL)
        home_roll_axis_button.configure(bg="dodger blue",state=NORMAL)
        if validated and connected:
            upload_button.configure(bg="dodger blue",state=NORMAL)

    except:

        connected = False

        connect_button.configure(bg='red',text="Connect")

        lock_roll_motor_button.configure(bg="gray50",state=DISABLED)
        lock_yaw_motor_button.configure(bg="gray50",state=DISABLED)
        home_yaw_axis_button.configure(bg="gray50",state=DISABLED)
        home_roll_axis_button.configure(bg="gray50",state=DISABLED)
        if not connected or not validated:
            upload_button.configure(bg="gray50",state=DISABLED)

        print("Error Connecting to Device")
        
connect_button = Button(
    root,
    text="Connect",
    font=5,
    fg="white",
    bg="red",
    width=20,
    borderwidth=5,
    command=connect
)
connect_button.place(x = 1250 ,y = 850)

loadPresetData(0)
stepModeSelected()
duplexModeSelected()
topSelected()
bwdSelected()

root.mainloop()