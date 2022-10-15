import tkinter as tk
import os, requests
from tkinter import messagebox
from tkinter import filedialog

win=tk.Tk()
win.title('RDO Tool')
win.geometry('300x300')

def path():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    while file_path == "":
        messagebox.showerror("Choose Folder", "No Path Selected !")
        file_path = filedialog.askdirectory()
    else:
        file = open("path.txt", "w")
        file.write(file_path)
        file.close()
        messagebox.showinfo("Choose Folder", "Path saved successfully !")

def installFile():
    path = open("path.txt", "r")
    value = path.readline()
    path.close()
    
    bootLauncherFlowYMT = value + '/x64/' + 'boot_launcher_flow.ymt'
    startupMETA = value + '/x64/data/' + 'startup.meta'
    try: 
        urlBootLauncherFlowYMT = "https://raw.githubusercontent.com/TheTimeLord32/Red-Dead-Online-Tool/master/src/boot_launcher_flow.ymt"
        r1 = requests.get(urlBootLauncherFlowYMT)
        with open(bootLauncherFlowYMT, 'wb') as f:
            f.write(r1.content)
        f.close()
    
        urlstartupMETA = "https://raw.githubusercontent.com/TheTimeLord32/Red-Dead-Online-Tool/master/src/startup.meta"
        r2 = requests.get(urlstartupMETA)
        with open(startupMETA, 'wb') as f:
            f.write(r2.content)
        f.close()
    except FileNotFoundError:
        messagebox.showerror("Install file", "Needed folders not found. Rechoose Path !")
    else:
        messagebox.showinfo("Install file", "Files installed successfully !")

def readFile():
    path = open("path.txt", "r")
    directory = path.readline()
    path.close()
    boot_disable = directory + "/x64/boot_launcher_flow.bak"
    startup_disable = directory + "/x64/data/startup.bak"
    boot_enable = directory + "/x64/boot_launcher_flow.ymt"
    startup_enable = directory + "/x64/data/startup.meta"
    return boot_disable, startup_disable, boot_enable, startup_enable

def activateFile():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_disable, boot_enable)
        os.rename(startup_disable, startup_enable)
        messagebox.showinfo("Activate file", "File activated !")
    except FileNotFoundError:
        messagebox.showerror("Activate file", "Path not found or file already activated. Retry")

def deactivateFile():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_enable, boot_disable)
        os.rename(startup_enable, startup_disable)
        messagebox.showinfo("Deactivate file", "File deactivated !")
    except FileNotFoundError:
        messagebox.showerror("Deactivate file", "Path not found or file already deactivated. Retry")

folder = tk.Button(win, text="Choose Folder", width=10 ,height=5 ,command=path)
install = tk.Button(win, text="Install file", width=10 ,height=5 ,command=installFile)
activate = tk.Button(win, text = "Activate file", width=10, height=5, command=activateFile)
deactivate = tk.Button(win, text = "Deactivate file", width=10, height=5, command=deactivateFile)

folder.place(x = 30,y = 30)
install.place(x = 120, y = 30)
activate.place(x = 30, y = 120)
deactivate.place(x = 120, y = 120)

win.mainloop()
