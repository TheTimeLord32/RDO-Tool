import tkinter as tk
import os, winreg, requests
from tkinter import filedialog

def fileReg():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()

    fileReg = open("RDR2.reg", 'w')
    fileReg.write("Windows Registry Editor Version 5.00\n")
    fileReg.write("[HKEY_LOCAL_MACHINE\SOFTWARE\Rockstar Games]\n")
    fileReg.write("[HKEY_LOCAL_MACHINE\SOFTWARE\Rockstar Games\Red Dead Redemption 2]\n")
    s = "\"Install Dir\"="+"\""+file_path+"\""+"\n"
    x = s.replace("\\", "\\\\")
    fileReg.write(str(x))

    fileReg.write("\"DisplayName\"=""\"Red Dead Redempion 2\"")
    fileReg.close()
    print("Registry file created in your folder.\nUse it to correctly continue with the other operations \n")

def readReg():
    access_registry = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    key = winreg.OpenKey(access_registry, r"SOFTWARE\Rockstar Games\Red Dead Redemption 2")
    dir, regtype = winreg.QueryValueEx(key, "Install Dir")
    return dir

def installazioneFile():
    value = readReg()
    bootLauncherFlowYMT = value + '\\x64\\' + 'boot_launcher_flow.ymt'
    startupMETA = value + '\\x64\\data\\' + 'startup.meta'

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

    print("File installed successfully \n")

def readFile():
    directory = readReg()
    boot_disable = directory + "\\x64\\boot_launcher_flow.bak"
    startup_disable = directory + "\\x64\\data\\startup.bak"
    boot_enable = directory + "\\x64\\boot_launcher_flow.ymt"
    startup_enable = directory + "\\x64\\data\\startup.meta"
    return boot_disable, startup_disable, boot_enable, startup_enable;
    
def attivaFile():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_disable, boot_enable)
        os.rename(startup_disable, startup_enable)
        print("File activated \n")
    except:
        print("File already activated \n")

def disattivaFile():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_enable, boot_disable)
        os.rename(startup_enable, startup_disable)
        print("File deactivated \n")
    except:
        print("File already deactivated \n")

operazione = input("Choose operation: \n1)Create Reg file \n2)Install file \n3)Activate \n4)Deactivate \n\nInsert number: ")
match operazione:
    case "1":
        fileReg()
    case "2":
        installazioneFile()
    case "3":
        attivaFile()
    case "4":
        disattivaFile()
    case unknown_command:
        print("Wrong operation \n")
