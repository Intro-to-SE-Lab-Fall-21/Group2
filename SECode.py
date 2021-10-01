import psycopg2

DB_HOST = "127.0.0.1"
DB_NAME = "email"
DB_USER = "emailClient"
DB_PASS = "password123"


conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)
csr = conn.cursor()

exit = 0
results = "hey"

while exit == 0:
    
    print("Please enter your username:", end=' ')
    Username = input()
    try:
        csr.execute("SELECT username FROM login WHERE username = %s", (Username,))
        results = (csr.fetchall())
        conn.commit()
        results = results[0][0]
    except:
        print("Username Not Found")
    
    if results == Username:
        print("Welcome user ", Username)
        print("Please enter your Password:", end=' ')
        Password = input()
        
        csr.execute("SELECT pass FROM login WHERE username = %s", (Username,))
        results = (csr.fetchall())
        conn.commit()
        results = results[0][0]
        
        if results == Password:
            print("Login Successful")
            exit = 1
        else:
            print("Incorrect Password")
        
    

csr.close()
conn.close()
