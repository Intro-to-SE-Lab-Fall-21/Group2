import socket
import psycopg2
import uuid

host = 'localhost'
port = 5500

DB_HOST = "127.0.0.1"
DB_NAME = "email"
DB_USER = "emailClient"
DB_PASS = "password123"


conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)
csr = conn.cursor()

filename = uuid.uuid4()
filename = str(filename) + ".txt"
print(filename)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen()
client, address = s.accept()
data = client.recv(1000).decode()
print(data)
client.send(b'Connected')
testEmailSender = client.recv(1000).decode()
print("From: " + testEmailSender)
client.send(b'Connected')
testEmailAddr = client.recv(1000).decode()
print("Email Address: " + testEmailAddr)
client.send(b'Connected')
testEmailSubj = client.recv(1000).decode()
print("Subject: " + testEmailSubj)
client.send(b'Connected')
testEmail = client.recv(10000).decode()
print("Email: " + testEmail)
client.send(b'Connected')
csr.execute("INSERT INTO emaildb (sender, recipient, subj, emailFile) VALUES('%s','%s','%s','%s')" % (testEmailSender, testEmailAddr, testEmailSubj, filename))
conn.commit()
csr.close()
conn.close()
s.close()
