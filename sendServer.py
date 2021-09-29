import socket
host = 'localhost'
port = 5500


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
s.close()
