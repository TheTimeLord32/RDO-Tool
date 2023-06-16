import tkinter as tk
import os, requests
from tkinter import messagebox
from tkinter import filedialog

win=tk.Tk()
win.title('RDO Tool')
win.geometry('600x300')

uniqueKey = tk.StringVar()
uniqueKey_label = tk.Label(win, text="Unique key: ")
uniqueKey_label.pack(fill='x', expand=True)
uniqueKey_label.place(x = 210, y = 70)

uniqueKey_entry = tk.Entry(win, textvariable=uniqueKey)
uniqueKey_entry.pack(fill='x', expand=True)
uniqueKey_entry.place(x = 210, y = 90)

def choosePath():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    while file_path == "":
        messagebox.showerror("Choose Folder", "No Path Selected !")
        file_path = filedialog.askdirectory()
        showPath()
    else:
        file = open("path.txt", "w")
        file.write(file_path)
        file.close()
        messagebox.showinfo("Choose Folder", "Path saved successfully !")
        showPath()

def showPath():
    # try:
        path = open("path.txt", "r")
        value = path.readline()
        path.close()
        currentPath = tk.Label(win, text="Current Folder Path:")
        currentPath.pack(fill='x', expand=True)
        currentPath.place(x = 210, y=30)
        
        currentPathValue = tk.Label(win, text=value)
        currentPathValue.pack(fill='x', expand=True)
        currentPathValue.place(x = 210, y=50)
    # except FileNotFoundError:
        # choosePath()

def checkACL():
    path = open("path.txt", "r")
    value = path.readline()
    path.close()
    try:
        os.access(value, os.W_OK)               #check write acl
        os.access(value, os.R_OK)               #check read acl
        os.access(value, os.X_OK)               #check exec acl
        os.access(value, os.X_OK | os.W_OK)     #check write file acl
    except PermissionError:
        messagebox.showerror("RDO Tool", "Restart the program with Administrator permission to access this folder !")

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
    checkACL()
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_disable, boot_enable)
        os.rename(startup_disable, startup_enable)
        messagebox.showinfo("Activate file", "File activated !")
    except FileNotFoundError:
        messagebox.showerror("Activate file", "Path not found or file already activated. Retry")

def deactivateFile():
    checkACL()
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        os.rename(boot_enable, boot_disable)
        os.rename(startup_enable, startup_disable)
        messagebox.showinfo("Deactivate file", "File deactivated !")
    except FileNotFoundError:
        messagebox.showerror("Deactivate file", "Path not found or file already deactivated. Retry")

def findOldString():
    try:
        path = open("path.txt", "r")
        directory = path.readline()
        path.close()
        boot_enable = directory + "/x64/boot_launcher_flow.ymt"
        startup_enable = directory + "/x64/data/startup.meta"

        files = [boot_enable, startup_enable]

        for x in files:
            with open(x, 'r') as file:
                file_contents = file.readlines()
                secondline = file_contents[1].strip()

        oldKey = secondline[4: -3]
        return oldKey

    except FileNotFoundError:
        messagebox.showerror("Files not found!")

def replaceString():
    try:
        path = open("path.txt", "r")
        directory = path.readline()
        path.close()
        boot_enable = directory + "/x64/boot_launcher_flow.ymt"
        startup_enable = directory + "/x64/data/startup.meta"
        old_string = findOldString()
        new_string = uniqueKey.get()

        files = [boot_enable, startup_enable]
        for file_path in files:
            # Read the contents of the file
            with open(file_path, 'r') as file:
                file_contents = file.read()

            # Replace the old string with the new string
            modified_contents = file_contents.replace(old_string, new_string)

            # Write the modified contents back to the file
            with open(file_path, 'w') as file:
                file.write(modified_contents)

        messagebox.showinfo("Replace unique key", "Unique key saved successfully!")
    except FileNotFoundError:
        messagebox.showerror("Replace unique key", "Path not found!")

folder = tk.Button(win, text="Choose Folder", width=10, height=5, command=choosePath)
install = tk.Button(win, text="Install file", width=10, height=5, command=installFile)
activate = tk.Button(win, text = "Activate file", width=10, height=5, command=activateFile)
deactivate = tk.Button(win, text = "Deactivate file", width=10, height=5, command=deactivateFile)
replace = tk.Button(win, text="Replace unique key", width=25, height=5, command=replaceString)

folder.place(x = 30,y = 30)
install.place(x = 120, y = 30)
activate.place(x = 30, y = 120)
deactivate.place(x = 120, y = 120)
replace.place(x = 210, y = 120)

win.mainloop()
os._exit(0)
