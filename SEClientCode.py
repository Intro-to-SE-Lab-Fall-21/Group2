import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import sys
import shutil

global searchButton

def logout(s):
    os.execl(sys.executable, sys.executable, *sys.argv)
        

def searchWipe():
    for widget in mailList.winfo_children():
        widget.destroy()
    Search.delete(0, 'end')

def viewWipe(s):
    emailDisplay.config(state = 'normal')
    emailDisplay.delete('1.0', END)
    for widget in view.winfo_children():
        widget.grid_remove()
    view.grid_remove()
    MainGUI(userGlobal, s)

def unlock(*args):
    a = uservar.get()
    b = passvar.get()
    if a and b:
        myButton.config(state = 'normal')
    else:
        myButton.config(state = 'disabled')

def unlock2(*args):
    a = srchvar.get()
    if a:
        searchButton.config(state = 'normal')    
    else:
        searchButton.config(state = 'disabled')

def unlock3(*args):
    a = recpvar.get()
    b = subjvar.get()
    if a and b:
        sendmsg.config(state = 'normal')
        atch.config(state = 'normal')
    else:
        sendmsg.config(state = 'disabled')
        atch.config(state = 'disabled')


def forward2(email, recipient, forwardWindow):
    forwardWindow.grid_remove()
    fwrd = 2
    s.sendall(str(fwrd).encode())
    s.recv(100)
    s.sendall(str(email).encode())
    s.recv(100)
    s.sendall(str(recipient).encode())
    s.recv(100)
    

def forward(email):
    Forw = Frame(view, width = 70)
    Forw.grid(row = 4, column = 0, columnspan = 3)
    
    fLabel = Label(Forw, text = "Forward to Whom?")
    fLabel.grid(row = 0, column = 0, columnspan = 3)

    fEntry = Entry(Forw, width = 50)
    fEntry.grid(row = 1, column = 1, columnspan = 2)

    fButton = Button(Forw, text = "Send", command = lambda : forward2(email, fEntry.get(), Forw))
    fButton.grid(row = 1, column = 0)


def mailSearch(username, keyword):

    searchWipe()
    resetButton.config(state = 'normal')
    srch = 4
    results = []
    
    s.sendall(str(srch).encode())
    s.recv(100)
    s.sendall(str(username).encode())
    s.recv(100)
    s.sendall(str(keyword).encode())
    s.recv(100)

    i = 0
    length = int(s.recv(1000).decode())
    s.send(b'Connected')
    if length == 0:
        return
    
    while i < length:
        results.append([])
        j = 0
        
        while j < 4:
            results[i].append(s.recv(1000).decode())
            s.send(b'Connected')
            j = j + 1
        i = i + 1
        
        #mailList = LabelFrame(myFrame, text = "Mail List     Sender                                      Subject", width = 700, height = 500)
        mailList.config(width = 700)
        mailList.config(height = 500)
    
##    searchRes = LabelFrame(mailList, text = " text = "Mail List     Sender                                      Subject", width = 700, height = 500)        
##    searchRes.grid(row = 1, column = 0, columnspan = 3)
    i = 0    
    j = 0
    for i in results:
        email = Label(mailList, text = i[1])
        subj = Label(mailList, text = i[3])
            
        j += 1
        # i[1] = sender     i[2] = recipient    i[3] = subject
        email.place(x = 40, y = j*25, anchor = "w")
        subj.place(x = 210, y = j*25, anchor = "w")
        
        viewButton = Button(mailList, text = "View", command = lambda i=i : viewEmail(i[0], i[1], i[2], i[3], ))
        viewButton.place(x = 0, y = j*25, anchor = "w")

    
def saveAtt(emailFile):
    direct = filedialog.askdirectory(title = "Save")
    download = 6
    s.sendall(str(download).encode())
    s.recv(100)
    s.sendall(emailFile.encode())
    s.recv(100)
    fileSize = int(s.recv(100).decode())
    s.sendall(b'Connected')
    attachmentFile = s.recv(1000).decode()
    s.sendall(b'Connected')
    attachmentFile = direct + "/" + attachmentFile[36:]
    aFile = open(attachmentFile, "wb")
    bytesRead = 0
    while bytesRead < fileSize:
        attachment = s.recv(1024)
        bytesRead = bytesRead + 1024
        aFile.write(attachment)
    aFile.close()
    s.sendall(b'Connected')
    
        
def getAttach(attachmentArray):
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]
    root.filename = filedialog.askopenfilename(initialdir="C:/", title = "Choose an Attachment", filetypes = my_filetypes)
    attachmentArray.append(root.filename)



#client side part of function that iterates through the database for all results   
def scryClient(username):

    results = []
    attResults = []
    scry = 3
    s.sendall(str(scry).encode())
    s.recv(100)
    s.sendall(str(username).encode())
    s.recv(100)
    

    i = 0
    length = int(s.recv(1000).decode())
    s.send(b'Connected')
    if length == 0:
        return
     
    while i < length:
        results.append([])
        
        j = 0
####    k = 0
        while j < 4:
            results[i].append(s.recv(1000).decode())
            s.send(b'Connected')
            j = j + 1
        i = i + 1
        

    return results

def sendEmail(clientSock, emailSender, emailReciever, emailSubj, email, numAttachments, attachmentArray, comp):
    for widget in comp.winfo_children():
        widget.grid_remove()
    toEntry.delete(0, 'end')
    subEntry.delete(0, 'end')
    msg.delete('1.0', END)
    comp.grid_remove()
    
    sending = 1
    clientSock.sendall(str(sending).encode())
    clientSock.recv(100)
    clientSock.sendall(emailSender.encode())
    clientSock.recv(100)
    clientSock.sendall(emailReciever.encode())
    clientSock.recv(100)
    clientSock.sendall(emailSubj.encode())
    clientSock.recv(100)
    clientSock.sendall(email.encode())
    clientSock.recv(100)
    clientSock.sendall(str(numAttachments).encode())
    clientSock.recv(100)
    #print("Sending Email...")
    for i in attachmentArray:
        sendAttachment(clientSock, i)

    MainGUI(userGlobal, s)

def sendAttachment(clientSock, attachmentFile):
    attachment = open(attachmentFile, "rb")
    fileSize = os.path.getsize(attachmentFile)
    s.sendall(str(fileSize).encode())
    s.recv(100)
    s.sendall(attachmentFile.encode())
    s.recv(100)
    s.sendfile(attachment)
    s.recv(100)
    #print("Sending Attachment...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost' , 1001))
newPort = s.recv(1000).decode()
newPort = int(newPort)
s.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('localhost', newPort))
accept = 0
results = ""

root = Tk()
root.title('Email Client')
root.geometry("380x160")

myFrame = Frame()
myFrame.grid(row = 1, column = 0, columnspan = 2)

Welcome = Label(myFrame, text = "Welcome")
Welcome.grid(row = 0, column = 0, pady = 10, columnspan = 2)

#setting up tKinter variables for detecting input
uservar = StringVar(myFrame)
passvar = StringVar(myFrame)

uservar.trace("w", unlock)
passvar.trace("w", unlock)

#creating Username and password blocks
ULabel = Label(myFrame, text = "Username:")
ULabel.grid(row = 1, column = 0)

UEntry = Entry(myFrame, width = 50, textvariable = uservar)
UEntry.grid(row=1, column=1)

PLabel = Label(myFrame, text = "Password:")
PLabel.grid(row = 2, column = 0)
        
PEntry = Entry(myFrame, width = 50, textvariable = passvar)
PEntry.grid(row=2, column =1)

myButton = Button(myFrame, text = "Submit", state = DISABLED, command = lambda : authenticate(UEntry.get(), PEntry.get(), s))
myButton.grid(row = 3, column = 0, columnspan = 2)



##Making GUI elements Global for ease of manipulation
searchFrame = Frame(myFrame, pady = 5)
srchvar = StringVar(searchFrame)
Search = Entry(searchFrame, width = 74, textvariable = srchvar)
searchButton = Button(searchFrame, text = "Search", state = DISABLED, padx = 30)
resetButton = Button(searchFrame, text = "Refresh", padx = 30)
mailList = LabelFrame(myFrame, text = "Mail List     Sender                                      Subject", width = 700, height = 500)
ComposeButton = Button(myFrame, text = "Compose Email", width = 40, height = 3)
ExitButton = Button(myFrame, text = "Logout", width = 40, height = 3)

comp = LabelFrame(myFrame, text = "Compose A Message", width = 450, height = 300)
recpvar = StringVar(comp)
subjvar = StringVar(comp)
to = Label(comp, text = "To: ")
toEntry = Entry(comp, width = 100, text = '', textvariable = recpvar)
subject = Label(comp, text = "Subject: ")
subEntry = Entry(comp, width = 100, text = '', textvariable = subjvar)
message = Label(comp, text = "Message: ")
msg = Text(comp, width = 100, height = 20)
back = Button(comp, text = "Back", width = 23, height = 5)
atch = Button(comp, text = "Attach Files", state = DISABLED, width = 55, height = 5)
sendmsg = Button(comp, text = "Send", state = DISABLED, width = 55, height = 5)

view = Frame(myFrame, width = 30)
emailDisplay = Text(view, width = 50 , height = 20)
forBut = Button(view, text = "Forward", width = 20)
attBut = Button(view, text = "No Attachments", width = 20, state = DISABLED)
XButton = Button(view, text = "Back", width = 20)
def viewEmail(email, sender, recipient, subject):

    mainWipe(s, 1)

    root.geometry("450x500")
    
    viewing = 5
    s.sendall(str(viewing).encode())
    s.recv(100)
    s.sendall(str(email).encode())
    s.recv(100)
    file = s.recv(10000).decode()
    s.sendall(b'Connected')
    numAttach = s.recv(100).decode()
    
    
    view.grid(row = 0, column = 0)

    L1 = Label(view, text = "Sent from " + sender + " to " + recipient)
    L1.grid(row = 0, column = 0, columnspan = 3)

    L2 = Label(view, text = "Subject: " + subject)
    L2.grid(row = 1, column = 0, columnspan = 3)
    
    emailDisplay.grid(row = 2, column = 0, columnspan = 3)
    
    emailDisplay.insert(END, file)
    emailDisplay.config(state = 'disabled')
        
    forBut.config(command = lambda : forward(email))
    forBut.grid(row = 3, column = 1)

    attBut.config(command = lambda : saveAtt(email))
    attBut.grid(row = 3, column = 0)

    XButton.config(command = lambda : viewWipe(s))
    XButton.grid(row = 3, column = 2)

    if int(numAttach) == 1:
        attBut.config(text = "Save Attachment")
        attBut.config(state = 'normal')
        
    elif int(numAttach) > 1:
        conc = "Save " + str(numAttach) + " Attachments"
        attBut.config(state = 'normal')
        attBut.config(text = conc)

def compose(clientSock, emailSender):

    mainWipe(s, 1)
    numAttachments = 0
    attachmentArray = []

    root.geometry("850x500")
    #Text Boxes
    
    comp.grid(row = 0, column = 0)

    recpvar.trace("w", unlock3)
    subjvar.trace("w", unlock3)
    

    back.config(command = lambda : mainWipe(s, 0))
    back.grid(row = 0, column = 2, rowspan = 2, sticky = "e")

    to.grid(row = 0, column = 0)

    toEntry.grid(row = 0, column = 1, columnspan = 2, sticky = "w")
    emailReciever = toEntry.get()
    
    subject.grid(row = 1, column = 0)

    subEntry.grid(row = 1, column = 1, columnspan = 2, sticky = "w")
    emailSubj = subEntry.get()

    message.grid(row = 2, column = 0)
    
    msg.grid(row = 2, column = 1, columnspan = 2)
    email = msg.get(1.0, END)
    
    atch.config(command = lambda : getAttach(attachmentArray))
    atch.grid(row = 3, column = 2, sticky = "w")

    numAttachments = len(attachmentArray)
                                                                                            
    sendmsg.config(command = lambda : sendEmail(clientSock, emailSender, toEntry.get(), subEntry.get(), msg.get(1.0, END), len(attachmentArray), attachmentArray, comp))
    sendmsg.grid(row = 3, column = 1, sticky = "w")
    
def mainWipe(s, arg):
    for widget in searchFrame.winfo_children():
        widget.grid_remove()

    searchWipe()

    for widget in myFrame.winfo_children():
        widget.grid_remove()

    if arg == 0:
        MainGUI(userGlobal, s)

def MainGUI(username, s):
    root.geometry("735x600")
    root.title('Email Client')
    emailaddr = username + "@bulldogmail.com"

    searchFrame.grid(row = 0 , column = 0, columnspan = 2)
    searchButton.config(command = lambda :  mailSearch(emailaddr, Search.get()))
    resetButton.config(command = lambda : mainWipe(s, 0))
    searchButton.grid(row = 0, column = 0)
    resetButton.grid(row = 0, column = 2)

    srchvar.trace("w", unlock2)

    Search.grid(row = 0, column = 1)
        
    mailList.grid(row = 1, column = 0, columnspan = 2)

    #Mail List
  
    emailList = scryClient(emailaddr)
    ####numAtt = len

    j = 0     ####emailList[0] 
    for i in emailList:
        email = Label(mailList, text = i[1])
        subj = Label(mailList, text = i[3])
            
        j += 1
        # i[1] = sender     i[2] = recipient    i[3] = subject
        email.place(x = 40, y = j*25, anchor = "w")
        subj.place(x = 210, y = j*25, anchor = "w")
        
        viewButton = Button(mailList, text = "View", command = lambda i=i : viewEmail(i[0], i[1], i[2], i[3], ))
        viewButton.place(x = 0, y = j*25, anchor = "w")
        


    #Compose
    ComposeButton.config(command = lambda : compose(s, emailaddr))
    ComposeButton.grid(row = 2, column = 0, sticky = "w")

##    welcLabel = Label(myFrame, text = "Welcome")
##    welcLabel.place(x = 333, y = 540)
##    userName = Label(myFrame, text = username)
##    userName.place(x = 340, y = 565)

    ExitButton.config(command = lambda : logout(s))
    ExitButton.grid(row = 2, column = 1, sticky = "e")

    
def errormsg():
    err = messagebox.showerror("Login error", "Invalid Credentials")

def authenticate(username, password, s):

    s.sendall(username.encode())
    s.recv(1000)


    s.sendall(password.encode())
    results = s.recv(1000).decode()

    clear = 0

    if results == "Login Successful":
        global userGlobal
        
        Welcome.grid_remove()
        ULabel.grid_remove()
        UEntry.grid_remove()
        PLabel.grid_remove()
        PEntry.grid_remove()
        myButton.grid_remove()
        userGlobal = username

        MainGUI(username, s)
    else:
        errormsg()
        access = 0
        UEntry.delete(0, END)
        PEntry.delete(0, END)


            
root.mainloop()
