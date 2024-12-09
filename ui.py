import logic
from tkinter import *
from tkinter import ttk
from functools import partial
from PIL import Image, ImageTk

BASE_DN = "dc=snums,dc=local"
root = Tk()

#serverIP = input("What's the IP of the server? ") # Current test IP is 10.0.0.27
serverIP = '10.0.0.27'

connection = logic.connectToSLAPd(serverIP, "cn=admin,dc=snums,dc=local", "admin")
mainInfoList = []
selectedUser = StringVar() # The currently clicked user.
selectedUser.set("0")

def desc():
    print("Button pressed")

def setSelectedUser(user):
    selectedUser.set(user[0])
    print(selectedUser.get())

def deleteUser():
    try:
        logic.DelUser(connection, selectedUser.get())
        UserGet()
    except:
        pass

def UserGet():
    mainInfoList.clear() # Clear information list.
    
    for widget in leftFrame.winfo_children(): # Clear frame.
        widget.destroy()

    print("Fetching users...")
    users = logic.GetUsers(connection, BASE_DN)
    print(users)
    #textOutput = Text(leftFrame, height=8, width=30)
    #textOutput.pack(pady=30)
    x = 0
    for user in users:
        mainInfoList.append(user)
        setSelectedUserPartial = partial(setSelectedUser, user)
        entry = Button(leftFrame, text=user, command=setSelectedUserPartial)   
        entry.grid(row=x, column=0, padx=5,pady=5)
        x = x + 1

def ComputerGet():
    mainInfoList.clear()

    for widget in leftFrame.winfo_children(): # Clear frame.
        widget.destroy()

    print("Fetching computers...")
        
def createUserMenu():

    username_var = StringVar()
    password_var = StringVar()
    ou_dn_var = StringVar()

    def createUserCall():
        username = username_var.get()
        password = password_var.get()
        ou_dn = ou_dn_var.get()
        print([username, password, ou_dn])
        logic.CreateUser(connection, username, password, ou_dn)
        UserGet()
        popup.destroy()

    popup = Toplevel(root)
    popup.geometry("400x400")
    popup.title("Creating user...")

    infoLabel = Label(popup, text="Please input the username, password, and OU of the new user.")
    infoLabel.grid(row=0,column=0)
    usernameEntry = Entry(popup, textvariable=username_var)
    usernameEntry.grid(row=1,column=0)
    passwordEntry = Entry(popup, textvariable=password_var, show='*')
    passwordEntry.grid(row=2,column=0)
    ouEntry = Entry(popup, textvariable=ou_dn_var)
    ouEntry.grid(row=3,column=0)
    submitButton = Button(popup, command=createUserCall, text="Submit")
    submitButton.grid(row=4,column=0)

    

root.title("SNUMS Client")
root.configure(background="skyblue")
root.minsize(1280,720)
root.maxsize(1280, 720)
root.geometry("300x300+50+50")

# Information screen buttons frame
topFrame = Frame(root, width=800, height=100)
topFrame.grid(row=0,column=0,padx=3,pady=3)
usersButton = Button(topFrame, command=UserGet, text="Users")
usersButton.grid(row=0,column=0,padx=10,pady=5)
computersButton = Button(topFrame, command=ComputerGet, text="Computers")
computersButton.grid(row=0,column=1,padx=10,pady=5)

# Main information frame
leftFrame = Frame(root, width=800, height=600)
leftFrame.grid(row=1,column=0,padx=10,pady=5)

# SNUMS logo frame
topRightFrame = Frame(root, width=420, height=100)
topRightFrame.grid(row=0,column=1,padx=10,pady=5)
logoSNUMS = Image.open("./SNUMSLogo.png")
logoPhoto = ImageTk.PhotoImage(logoSNUMS)
logoLabel = Label(topRightFrame, image=logoPhoto)
logoLabel.pack()

# Common actions button frame
rightFrame = Frame(root, width=420, height=600)
rightFrame.grid(row=1,column=1,padx=10,pady=5)
selectedUserLabel = Label(rightFrame, textvariable=selectedUser)
selectedUserLabel.grid(row=0, column=0, padx=10, pady=5)
createUserButton = Button(rightFrame, command=createUserMenu, text="Create User")
createUserButton.grid(row=1,column=0,padx=10,pady=5)
deleteUserButton = Button(rightFrame, command=deleteUser, text="Delete Selected User")
deleteUserButton.grid(row=2,column=0,padx=10,pady=5)

root.mainloop()