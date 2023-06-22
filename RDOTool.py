import tkinter as tk
import os, requests
from tkinter import messagebox
from tkinter import filedialog

win=tk.Tk()
win.title('RDO Tool')
win.geometry('725x375')
newUniqueKey = tk.StringVar()

def choosePath():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askdirectory()
    while file_path == "":
        messagebox.showerror("Choose Folder", "No Path Selected !")
        file_path = filedialog.askdirectory()
        root.update()
        showPath()
    else:
        file = open("path.txt", "w")
        file.write(file_path)
        file.close()
        messagebox.showinfo("Choose Folder", "Path saved successfully !")
        showPath()

def showPath():
    if (os.path.exists("path.txt")):
        path = open("path.txt", "r")
        value = path.readline()
        path.close()
        return value
    else:
        return "No path yet choosen"

def checkACL():
    try:
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
    except FileNotFoundError:
            pass

def installFile():
    boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        
    if (os.path.isfile(boot_disable) & os.path.isfile(startup_disable)):
        return messagebox.showinfo("Install file", "Files already installed but deactivated !")
    if (os.path.isfile(boot_enable) & os.path.isfile(startup_enable)):
        return messagebox.showinfo("Install file", "Files already installed and activated !")
    else:
        path = open("path.txt", "r")
        value = path.readline()
        path.close()
    
        bootLauncherFlowYMT = value + '/x64/' + 'boot_launcher_flow.ymt'
        startupMETA = value + '/x64/data/' + 'startup.meta'

        if (os.path.isfile(bootLauncherFlowYMT) | os.path.isfile(startupMETA)):
            messagebox.showinfo("Install file", "Files already installed !")
            pass
        else:
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
    if (showCurrentFileStatus() == "File activated"):
        messagebox.showinfo("Activate file", "Files already activated")
    else:
        try:
            boot_disable, startup_disable, boot_enable, startup_enable = readFile()
            os.rename(boot_disable, boot_enable)
            os.rename(startup_disable, startup_enable)
            messagebox.showinfo("Activate file", "File activated !")
        except FileNotFoundError:
            messagebox.showerror("Activate file", "No files yet installed! Install it first")

def deactivateFile():
    checkACL()
    if (showCurrentFileStatus() == "File deactivated"):
        messagebox.showinfo("Dectivate file", "Files already deactivated")
    else:
        try:
            boot_disable, startup_disable, boot_enable, startup_enable = readFile()
            os.rename(boot_enable, boot_disable)
            os.rename(startup_enable, startup_disable)
            messagebox.showinfo("Deactivate file", "File deactivated !")
        except FileNotFoundError:
            messagebox.showerror("Deactivate file", "Path not found or file already deactivated. Retry")

def findOldString():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()

        if (os.path.isfile(boot_enable) & os.path.isfile(startup_enable)):
            files = [boot_enable, startup_enable]

            for x in files:
                with open(x, 'r') as file:
                    file_contents = file.readlines()
                    secondline = file_contents[1].strip()

            oldKey = secondline[4: -3]
            win.update()
            return oldKey
        if (os.path.isfile(boot_disable) & os.path.isfile(startup_disable)):
            return "No key detected from deactivated files"

    except FileNotFoundError:
        return "No files yet installed"

def replaceString():
    try:
        path = open("path.txt", "r")
        directory = path.readline()
        path.close()
        boot_enable = directory + "/x64/boot_launcher_flow.ymt"
        startup_enable = directory + "/x64/data/startup.meta"
        old_string = findOldString()
        new_string = newUniqueKey.get()

        if (not new_string):
            messagebox.showerror("Replace unique key", "Empty unique key")
        else:
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
        messagebox.showerror("Replace unique key", "Path of files not found!")

def showCurrentFileStatus():
    try:
        boot_disable, startup_disable, boot_enable, startup_enable = readFile()
        
        if (os.path.isfile(boot_disable) & os.path.isfile(startup_disable)):
            return "File deactivated"
        if (os.path.isfile(boot_enable) & os.path.isfile(startup_enable)):
            return "File activated"
    
    except FileNotFoundError:
        return "No files yet installed"

def showInstructions(tkWindow, xValue, textList):
    yStartValue = 175
    for value in textList:
        instructions = tk.Label(tkWindow, text=value)
        instructions.pack(fill="x", expand=True)
        instructions.place(x = xValue, y = yStartValue)
        yStartValue += 20

def createLabels():
    currentPath = tk.Label(win, text="Current Folder Path:")
    currentPath.pack(fill='x', expand=True)
    currentPath.place(x = 300, y=30)
    
    currentPathValue = tk.Label(win, text=showPath())
    currentPathValue.pack(fill='x', expand=True)
    currentPathValue.place(x = 300, y=50)

    currentUniqueKey_label = tk.Label(win, text="Current unique key: ")
    currentUniqueKey_label.pack(fill='x', expand=True)
    currentUniqueKey_label.place(x = 300, y = 70)

    currentUniqueKeyValue = tk.Label(win, text=findOldString())
    currentUniqueKeyValue.pack(fill='x', expand=True)
    currentUniqueKeyValue.place(x = 425, y = 70)

    newUniqueKey_label = tk.Label(win, text="New unique key: ")
    newUniqueKey_label.pack(fill='x', expand=True)
    newUniqueKey_label.place(x = 300, y = 90)

    newUniqueKey_entry = tk.Entry(win, textvariable=newUniqueKey)
    newUniqueKey_entry.pack(fill='x', expand=True)
    newUniqueKey_entry.place(x = 425, y = 90)

    fileStatus = tk.Label(win, text="Current file status: ")
    fileStatus.pack(fill='x', expand=True)
    fileStatus.place(x = 300, y = 110)

    fileStatusValue = tk.Label(win, text=showCurrentFileStatus())
    fileStatusValue.pack(fill='x', expand=True)
    fileStatusValue.place(x = 425, y = 110)

def createButtons():
    folder = tk.Button(win, text="Choose Folder", width=15, height=5, command=choosePath)
    install = tk.Button(win, text="Install file", width=15, height=5, command=installFile)
    activate = tk.Button(win, text = "Activate file", width=15, height=5, command=activateFile)
    deactivate = tk.Button(win, text = "Deactivate file", width=15, height=5, command=deactivateFile)
    replace = tk.Button(win, text="Replace unique key", width=32, height=5, command=replaceString)

    folder.place(x = 30,y = 30)
    install.place(x = 150, y = 30)
    activate.place(x = 30, y = 120)
    deactivate.place(x = 150, y = 120)
    replace.place(x = 30, y = 210)

def main():
    createButtons()
    createLabels()
    showPath()
    instructionsText = ["--------------------Instructions--------------------", "1. Choose folder to Red Dead Redemption 2 game path", "2. Press Install file to download the needed text files", "3. Change the unique key to one of your liking and press Replace Unique Key", "4. You're ready to play with your friends!", "Note: the tool is correctly working when no splash screen appears"]
    showInstructions(win, 300, instructionsText)
    win.mainloop()
    os._exit(0)

if __name__ == "__main__": main()
