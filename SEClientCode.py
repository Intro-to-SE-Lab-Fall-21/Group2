import socket
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import os
import shutil



def forward2(email, recipient, forwardWindow):
    forwardWindow.destroy()
    fwrd = 2
    s.sendall(str(fwrd).encode())
    s.recv(100)
    s.sendall(str(email).encode())
    s.recv(100)
    s.sendall(str(recipient).encode())
    s.recv(100)
    

def forward(email):
    Forw = Toplevel()
    Forw.title("Forward Email")

    fLabel = Label(Forw, text = "Forward to Whom?")
    fLabel.grid(row = 0, column = 0, columnspan = 2)

    fEntry = Entry(Forw, width = 50)
    fEntry.grid(row = 1, column = 1)

    fButton = Button(Forw, text = "Send", command = lambda : forward2(email, fEntry.get(), Forw))
    fButton.grid(row = 1, column = 0)


def mailSearch(username, keyword):

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

    Sea = Toplevel()
    Sea.title("Search Results")

    
    mailList = LabelFrame(Sea, text = "Mail List", padx = 200 , pady = 140)        
    mailList.grid(row = 1, column = 0, columnspan = 3)


            
    j = 0
    for i in results:
        j += 1
        # i[1] = sender     i[2] = recipient    i[3] = subject
        email = Label(mailList, text = i[1] + "/" + i[3])
        email.grid(row = j , column = 1)
        
        
        viewButton = Button(mailList, text = "View", command = lambda i=i : viewEmail(i[0], i[1], i[2], i[3]))
        viewButton.grid(row = j, column = 0)

    

####def saveAtt(attachmentFile):
####    s.sendall(attachmentFile.encode())
####    s.recv(100)
####    fileSize = int(s.recv(100).decode())
####    aFile = open(attachmentFile[36:], "wb")
####    bytesRead = 0
####    while bytesRead < fileSize:
####        attachment = client.recv(1024)
####        bytesRead = bytesRead + 1024
####        aFile.write(attachment)
####    aFile.close()
    
    
    
def viewEmail(email, sender, recipient, subject):

    view = Toplevel()
    view.title("Email")

    L1 = Label(view, text = "Sent from " + sender + " to " + recipient)
    L1.grid(row = 0, column = 0, columnspan = 2)

    L2 = Label(view, text = "Subject: " + subject)
    L2.grid(row = 1, column = 0, columnspan = 2)
    emailDisplay = Text(view, width = 50 , height = 20)
    emailDisplay.grid(row = 2, column = 0, columnspan = 2)

    text = open(email, 'r')
    file = text.read()
    
    emailDisplay.insert(END, file)  
    text.close()
        

    forBut = Button(view, text = "Forward", command = lambda : forward(email))
    forBut.grid(row = 3, column = 1)

####    attButt = Button(view, text = "Attachment", command = lambda : saveAtt())
####    attButt.grid(row = 3, column = 0)

def getAttach(attachmentArray):
    my_filetypes = [('all files', '.*'), ('text files', '.txt')]
    root.filename = filedialog.askopenfilename(initialdir="C:/", title = "Choose an Attachment", filetypes = my_filetypes)
    attachmentArray.append(root.filename)

    
def compose(clientSock, emailSender):


    numAttachments = 0
    attachmentArray = []
    
    #Text Boxes
    comp = Toplevel()
    comp.title("Compose A Message")

    back = Button(comp, text = "Back", padx = 30, pady = 20, command = comp.destroy)
    back.grid(row = 0, column = 2, rowspan = 2)

    to = Label(comp, text = "To: ")
    to.grid(row = 0, column = 0)

    toEntry = Entry(comp, width = 100)
    toEntry.grid(row = 0, column = 1)
    emailReciever = toEntry.get()
    
    subject = Label(comp, text = "Subject: ")
    subject.grid(row = 1, column = 0)

    subEntry = Entry(comp, width = 100)
    subEntry.grid(row = 1, column = 1)
    emailSubj = subEntry.get()

    message = Label(comp, text = "Message: ")
    message.grid(row = 2, column = 0)
    
    msg = Text(comp, width = 100, height = 20)
    msg.grid(row = 2, column = 1)
    email = msg.get(1.0, END)
    
    atch = Button(comp, text = "Attach Files", padx = 30, pady = 20, command = lambda : getAttach(attachmentArray))
    atch.grid(row = 3, column = 1)

    numAttachments = len(attachmentArray)
                                                                                            
    sendmsg = Button(comp, text = "Send", padx = 30, pady = 20,command = lambda : sendEmail(clientSock, emailSender, toEntry.get(), subEntry.get(), msg.get(1.0, END), len(attachmentArray), attachmentArray, comp))
    sendmsg.grid(row = 3, column = 0)

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
        
        ## WIP Code 
####        numAtt = s.recv(1000).decode()
####        s.send(b'Connected')
####            
####        while k < numAtt:
####            attResults.append([])
####            attResults[i].append(s.recv(200).decode())
####            attResults[i].append(results[i][0])
####            s.send(b'Connected')
####            k = k + 1
    
####    return [results,attResults]
    return results

def sendEmail(clientSock, emailSender, emailReciever, emailSubj, email, numAttachments, attachmentArray, comp):
    comp.destroy()
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
    #clientSock.sendfile(email)
    clientSock.recv(100)
    clientSock.sendall(str(numAttachments).encode())
    clientSock.recv(100)
    print("Sending Email...")
    for i in attachmentArray:
        sendAttachment(clientSock, i)

    #re = showinfo(comp, text = "Sent!")

def sendAttachment(clientSock, attachmentFile):
    attachment = open(attachmentFile, "rb")
    fileSize = os.path.getsize(attachmentFile)
    s.sendall(str(fileSize).encode())
    s.recv(100)
    s.sendall(attachmentFile.encode())
    s.recv(100)
    s.sendfile(attachment)
    s.recv(100)
    print("Sending Attachment...")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost' , 1001))
accept = 0
results = ""

root = Tk()
root.title('Email Client')
root.geometry("800x600")

global access
access = 1

myFrame = Frame()
myFrame.grid()

Welcome = Label(root, text = "Welcome")
Welcome.grid(row = 0, column = 0, pady = 10, columnspan = 2)

ULabel = Label(root, text = "Username:")
ULabel.grid(row = 1, column = 0)

UEntry = Entry(root, width = 50)
UEntry.grid(row=1, column=1)

PLabel = Label(root, text = "Password:")
PLabel.grid(row = 2, column = 0)
        
PEntry = Entry(root, width = 50)
PEntry.grid(row=2, column =1)

myButton = Button(text = "Submit", command = lambda : authenticate(UEntry.get(), PEntry.get(), s))
myButton.grid(row = 3, column = 0, columnspan = 2)


if access == 0:
    access = 1
    
    ULabel.grid_forget()
    UEntry.grid_forget()
    PLabel.grid_forget()
    PEntry.grid_forget()
    myButton.grid_forget()

    ULabel = Label(root, text = "Username:")
    ULabel.grid(row = 1, column = 0)

    UEntry = Entry(root, width = 50)
    UEntry.grid(row=1, column=1)

    PLabel = Label(root, text = "Password:")
    PLabel.grid(row = 2, column = 0)
        
    PEntry = Entry(root, width = 50)
    PEntry.grid(row=2, column =1)
    
    myButton = Button(text = "Submit", command = lambda : authenticate(UEntry.get(), PEntry.get()))
    myButton.grid(row = 3, column = 0, columnspan = 2)

def MainGUI(username, s):

    Welcome['text'] = "Emails"
    emailaddr = username + "@bulldogmail.com"

    Search = Entry(root, width = 70)
    Search.grid(row = 2, column = 2)

    SearchButton = Button(root, text = "Search", command = lambda :  mailSearch(emailaddr, Search.get()))
    SearchButton.grid(row = 3, column = 2)

    mailList = LabelFrame(root, text = "Mail List", padx = 200 , pady = 140)        
    mailList.grid(row = 1, column = 0, columnspan = 3)

    #Mail List
  
    emailList = scryClient(emailaddr)
    ####numAtt = len

    j = 0     ####emailList[0] 
    for i in emailList:
        email = Label(mailList, text = i[1] + "/" + i[3])
            
        j += 1
        # i[1] = sender     i[2] = recipient    i[3] = subject
        email.grid(row = j , column = 1)
        
        
        viewButton = Button(mailList, text = "View", command = lambda i=i : viewEmail(i[0], i[1], i[2], i[3], ))
        viewButton.grid(row = j, column = 0)
        


    #Compose
    ComposeButton = Button(root, text = "Compose Email", padx = 30, pady = 20, command = lambda : compose(s, emailaddr))
    ComposeButton.grid(row = 2, column = 0)
    

    ExitButton = Button(root, text = "Exit", padx = 30, pady = 20, command = root.destroy)
    ExitButton.grid(row = 2, column = 4)

    
def errormsg():
    err = messagebox.showerror("Login error", "Invalid Credentials")

def authenticate(username, password, s):

    s.sendall(username.encode())
    s.recv(1000)


    s.sendall(password.encode())
    results = s.recv(1000).decode()

    clear = 0

    if results == "Login Successful":
        Welcome.grid_forget()
        ULabel.grid_forget()
        UEntry.grid_forget()
        PLabel.grid_forget()
        PEntry.grid_forget()
        myButton.grid_forget()

        MainGUI(username, s)
        print(results)
    else:
        errormsg()
        access = 0
        UEntry.delete(0, END)
        PEntry.delete(0, END)


    
    






            
root.mainloop()
