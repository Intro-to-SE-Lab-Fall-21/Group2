import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost' , 1001))
accept = 0
results = "buh"
while accept == 0:
    Username = input("Please enter your username: ")

    s.sendall(Username.encode())
    s.recv(1000)

    Password = input("Please enter your password: ")
    s.sendall(Password.encode())
    results = s.recv(1000).decode()

    if results == "Login Successful":
        accept = 1
        print(results)
    else:
        print("Invalid credentials, please try again.")
