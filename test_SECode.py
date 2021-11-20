import pytest
from SECode4, SECodeServer import *

@pytest.mark.parametrize("recipient, keyword", [("CortB", "Buh"), ("HayesG", "football", ("CortB", "CadeB"))])
def test_searching(recipient, keyword):
    assert searchDisplay(totalResults, csr, conn, client)

@pytest.mark.parametrize("filename",[('testing.txt', "bunny.txt", "helloworld.txt")]
def test_recieveAttachment(filename):
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

@pytest.mark.parametrize("email, target", [("cadeb@bulldog.com", "hayesg@bulldog.com"), ("hayesg@bulldog.com", "cadeb@bulldog.com"), ("cortb@bulldog.com", "cadeb@bulldog.com"), ("hayesg@bulldog.com", "cortb@bulldog.com")]
def test_forwardEmail(email, target):
    assert for in in results:
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

@pytest.mark.parametrize("results", [("CadeB", "CortB", "HayesG", "Hello", "World")]
def test_serchDisplay(results):
    assert searchDisplay == "None"


@pytest.mark.parametrize("recipient, email", [("CortB","cortb@bulldog@gmail.com"), ("HayesG", "hayesgbulldog@gmail.com"), ("CadeB", "cadebbulldog@gmail.com")]
def test_openEmail(recipient, email, csr):
    assert csr.execute("SELECT * FROM emaildb WHERE (emailfile = %s AND recipient = %s)", (email, recipient))
    senderResults = (csr.fetchall())
    emailFile = senderResults[0][0]
    emailFile = open(emailFile, "rb")
    text = emailFile.read()
    client.sendall(text)
    client.recv(100)
    client.sendall(str(numAttach).encode())
