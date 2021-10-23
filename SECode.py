import socket
import psycopg2
import uuid
import shutil
import os

    ##WIP CODE
####def uploadAttachment():
####    attachmentFile = client.recv(200).decode()
####    client.send(b'Connected')
####    attachment = open(attachmentFile, "rb")
####    fileSize = os.path.getsize(attachmentFile)
####    client.sendall(str(fileSize).encode())
####    client.recv(100)
####    client.sendall(attachmentFile.encode())
####    client.recv(100)
####    client.sendfile(attachment)
####    client.recv(100)
####    print("Sending Attachment...")


#function that iterates through the database for all results    
def scry(username, csr, conn, socket):
    
    csr.execute("SELECT * FROM emaildb WHERE recipient = %s", (username,))
    results = csr.fetchall()
    length = len(results)
    client.send(str(length).encode())
    client.recv(100)
    if length == 0:
        return
    
    for i in results:
        ##WIP CODE
####        csr.execute("SELECT * FROM attachdb WHERE emailname = %s", (i[0],))
####        attResults = csr.fetchall()
####        numAttachments = len(attResults)

        for j in i:
            client.send(j.encode())
            client.recv(100)
        ## WIP CODE
####        client.send(str(numAttachments).encode())
####        client.recv(100)
####        for k in numAttachments:
####            client.send(k[0].encode())
####            client.recv(100)


def searchDisplay(results, csr, conn):
    length = len(results)
    client.send(str(length).encode())
    client.recv(100)
    if length == 0:
        return
    
    for i in results:
        for j in i:
            client.send(j.encode())
            client.recv(100)


def searching(recipient, keyword, csr, conn):
    csr.execute("SELECT * FROM emaildb WHERE (sender = %s AND recipient = %s)", (keyword, recipient))
    senderResults = (csr.fetchall())
    csr.execute("SELECT * FROM emaildb WHERE (subj = %s AND recipient = %s)", (keyword, recipient))
    subjResults = (csr.fetchall())

    totalResults = []
    totalResults = senderResults + subjResults

    searchDisplay(totalResults, csr, conn)


def receiveEmail(serverSocket, csr, conn):
    filename = uuid.uuid4()
    filename = str(filename) + ".txt"
    print("Recieving Email...")
    testEmailSender = client.recv(1000).decode()
    client.send(b'Connected')
    testEmailAddr = client.recv(1000).decode()
    client.send(b'Connected')
    testEmailSubj = client.recv(1000).decode()
    client.send(b'Connected')
    testEmail = client.recv(10000).decode()
    client.send(b'Connected')
    csr.execute("INSERT INTO emaildb (emailFile, sender, recipient, subj) VALUES('%s','%s','%s','%s')" % (filename, testEmailSender, testEmailAddr, testEmailSubj))
    conn.commit()
    i = 0
    file = open(filename, "w")
    file.write(str(testEmail))
    file.close()
    numAttachments = int(client.recv(1000).decode())
    client.send(b'Connected')
    #numAttachments = 1
    while i < numAttachments:
        receiveAttachment(serverSocket, filename, csr, conn)
        i = i + 1;
    #forwardEmail(filename, "forwardTesting@bulldogmail.com", csr, conn)

##WIP CODE    
####def sendAttachment(clientSock, attachmentFile):
####    attachment = open(attachmentFile, "rb")
####    fileSize = os.path.getsize(attachmentFile)
####    s.sendall(str(fileSize).encode())
####    s.recv(100)
####    s.sendall(attachmentFile.encode())
####    s.recv(100)
####    s.sendfile(attachment)
####    s.recv(100)
####    print("Sending Attachment...")

def receiveAttachment(serverSocket, filename, csr, conn):
    print("Receiving Attachment...")
    fileSize = int(client.recv(1000).decode())
    client.send(b'Connected')
    attachmentFile = client.recv(1000).decode()
    client.send(b'Connected')
    aFileName = uuid.uuid4()
    head,tail = os.path.split(attachmentFile)
    aFileName = str(aFileName) + tail;
    aFile = open(aFileName, "wb")
    bytesRead = 0
    while bytesRead < fileSize:
        attachment = client.recv(1024)
        bytesRead = bytesRead + 1024
        aFile.write(attachment)
    client.send(b'Connected')
    aFile.close()
    csr.execute("INSERT INTO attachdb (attachname, emailname) VALUES('%s','%s')" % (aFileName, filename))
    conn.commit()

def forwardEmail(emailname, target, csr, conn):
    print("Forwarding Email")
    fullPathOrig = os.path.abspath(emailname)
    csr.execute("SELECT * FROM emaildb WHERE emailfile = %s", (emailname,))
    emailDetails = csr.fetchall()
    emailSender = emailDetails[0][2]
    emailSubj = emailDetails[0][3]
    csr.execute("SELECT attachname FROM attachdb WHERE emailname = %s", (emailname,))
    results = (csr.fetchall())
    attachList = []
    pathCopy = str(uuid.uuid4()) + ".txt"
    copy = open(pathCopy, "w")
    fullPathCopy = os.path.abspath(pathCopy)
    shutil.copyfile(fullPathOrig, fullPathCopy)
    csr.execute("INSERT INTO emaildb (emailFile, sender, recipient, subj) VALUES('%s','%s','%s','%s')" % (pathCopy, emailSender, target, emailSubj))
    conn.commit()
    for i in results:
        for j in i:
            attachList.append(str(j))
            attachPath = j[36:]
            print("Attachments: " + str(j))
            fullAttachPath = os.path.abspath(attachPath)
            attachPathCopy = str(uuid.uuid4()) + attachPath
            fullAttachPathCopy = os.path.abspath(attachPathCopy)
            shutil.copyfile(fullAttachPath, fullAttachPathCopy)
            csr.execute("INSERT INTO attachdb (attachname, emailname) VALUES('%s','%s')" % (attachPathCopy, pathCopy))
            conn.commit()


DB_HOST = "127.0.0.1"
DB_NAME = "IntroSE_EmailDB"
DB_USER = "emailClient"
DB_PASS = "password123"


conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)
csr = conn.cursor()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost' , 1001))
s.listen()
client, address = s.accept()



results = ""
check = 0
while check == 0:

    Username = client.recv(1000).decode()
    
    try:
        csr.execute("SELECT username FROM login WHERE username = %s", (Username,))
        results = (csr.fetchall())
        conn.commit()
        results = results[0][0]
    except:
        client.sendall(b"Username Not Found")

    
    if results == Username:
        client.sendall(b"Welcome!")
        Password = client.recv(1000).decode()
        
        csr.execute("SELECT pass FROM login WHERE username = %s", (Username,))
        results = (csr.fetchall())
        conn.commit()
        results = results[0][0]
        
        if results == Password:
            client.sendall(b"Login Successful")
            check = 1
        else:
            client.sendall(b"Incorrect Password")


while True:
    optChosen = int(client.recv(100).decode())
    
    if optChosen == 1:
        client.send(b'Connected')
        receiveEmail(client, csr, conn)
        
    if optChosen == 2:
        client.send(b'Connected')
        email = client.recv(1000).decode()
        client.send(b'Connected')
        recipient = client.recv(1000).decode()
        client.send(b'Connected')
        forwardEmail(email, recipient, csr, conn)
        
    if optChosen == 3:
        client.send(b'Connected')
        username = client.recv(1000).decode()
        client.send(b'Connected')
        scry(username, csr, conn, client)
        
    if optChosen == 4:
        client.send(b'Connected')
        username = client.recv(1000).decode()
        client.send(b'Connected')
        keyword = client.recv(1000).decode()
        client.send(b'Connected')
        searching(username, keyword, csr, conn)
    #if optChosen == 5:
        
    

csr.close()
conn.close()
