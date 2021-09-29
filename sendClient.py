import socket
from tkinter import *
from tkinter import ttk

host = 'localhost'
port = 5500
testEmail = open("testEmailSend.txt", "rb")
testEmailAddr = "cortblackwell@bulldogmail.com"
testEmailSender = "blahblha@bulldogmail.com"
testEmailSubj = "Testing"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
s.sendall(b'Connected')
data = s.recv(1000).decode()
print("Recieved From Server: " + data)
s.sendall(testEmailSender.encode())
s.recv(100)
s.sendall(testEmailAddr.encode())
s.recv(100)
s.sendall(testEmailSubj.encode())
s.recv(100)
s.sendfile(testEmail)
s.close()
