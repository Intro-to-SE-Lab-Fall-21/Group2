import psycopg2

DB_HOST = "127.0.0.1"
DB_NAME = "IntroSE_EmailDB"
DB_USER = "postgres"
DB_PASS = "phoenix6877$"


conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)
csr = conn.cursor()

##csr.execute("CREATE TABLE login (id SERIAL PRIMARY KEY, username VARCHAR, password VARCHAR);")
##csr.execute("INSERT INTO login (username, password) VALUES('CadeB', 'buh')")

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