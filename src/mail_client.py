# Data Communication - Mandatory Assignment 2
# s205129 - Jonas Stenholt Melchior Jensen
# 23/03 - 2021

# Mail client using SMTP protocol via socket programming.
# Can either connect to DTU's mailserver or google's smtp server on users choice.

from socket import*
import base64
import ssl
#TCP connection


choice = input("What mail server, do you want to connect to?\nA: DTU's mail server\nB: Google's smtp mail server\n")
if (choice.lower() == 'a'): #DTU
    # Make TCP connection with DTU mail server
    mailServer = "dtu-dk.mail.protection.outlook.com"
    #mailServer = "localhost"
    serverPort = 25
    clientSocket = socket(AF_INET, SOCK_STREAM) #TCP socket type
    clientSocket.connect((mailServer, serverPort))
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')
    heloCommand = 'EHLO Jonas\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
    DTU = 1
elif (choice.lower() == 'b'): #google
    # Make TCP connection with google's smtp mail server
    mailServer = "smtp.gmail.com"
    serverPort = 587 #port for smtp
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((mailServer, serverPort))
    recv = clientSocket.recv(1024).decode()
    print(recv)
    if recv[:3] != '220':
        print('220 reply not received from server.')
    heloCommand = 'EHLO Jonas\r\n'
    clientSocket.send(heloCommand.encode())
    recv1 = clientSocket.recv(1024).decode()
    print(recv1)
    if recv1[:3] != '250':
        print('250 reply not received from server.')
    # Start TLS mode - Transport Layer Security
    clientSocket.send("STARTTLS\r\n".encode())
    recv2 = clientSocket.recv(1024)
    print(recv2.decode())
    # Make SSL socket
    sslSocket = ssl.wrap_socket(clientSocket)
    # Authenticate login information - sender
    sslSocket.send("AUTH LOGIN\r\n".encode())
    recv3 = sslSocket.recv(1024)
    print(recv3.decode())
    DTU = 0
    clientSocket = sslSocket # assign sslSocket to clientSocket for less code..


# MAIL FROM
def sender():
    emailf = input("Mail from: ")
    if (DTU == 1): # DTU
        mailCommand = ("MAIL FROM:<%s>\r\n" % emailf)
        clientSocket.send(mailCommand.encode())
        recv2 = clientSocket.recv(1024).decode()
        print(recv2)
        if recv2[:3] != '250':
            print('250 reply not received from server.')
        return recv2
    elif (DTU == 0): # Google - email and password
        encodedEmail = base64.b64encode(emailf.encode())
        clientSocket.send(encodedEmail)
        clientSocket.send("\r\n".encode())
        recv2 = clientSocket.recv(1024).decode()
        print(recv2)
        pw = input("Password: ")
        pwEncoded = base64.b64encode(pw.encode())
        clientSocket.send(pwEncoded)
        clientSocket.send("\r\n".encode())
        recv3 = clientSocket.recv(1024).decode()
        print(recv3)
        clientSocket.send(("MAIL FROM:<%s>\r\n" % emailf).encode())

# RCPT TO
def to():
    emailt = input("Mail to: ")
    rcptCommand = ("RCPT TO:<%s>\r\n" % emailt)
    clientSocket.send(rcptCommand.encode())
    recv3 = clientSocket.recv(1024).decode()
    print(recv3)
    if recv3[:3] != '250':
        print('250 reply not received from server.')
    return recv3

# DATA
def sendMessage():
    choice = input("Do you wish to add a picture as an attachment? - Y/N\n")
    if(choice.lower() == 'y'):
        dataCommand = "DATA\r\n"
        clientSocket.send(dataCommand.encode())
        recv4 = clientSocket.recv(1024).decode()
        print(recv4)
        if recv4[:3] != '354':
            print('354 reply not received from server.')
        # Subject
        subject = input("Subject: ")
        subCommand = ("Subject: %s\r\n" % subject)
        clientSocket.send(subCommand.encode())
        MIME = "MIME-version: 1.0\r\n"
        clientSocket.send(MIME.encode())
        ContentType = "Content-Type: multipart/mixed; boundary=simple boundary\r\n"
        clientSocket.send(ContentType.encode())

        # Preamble
        PreAmble = "\r\nThis is the preamble\r\n"
        clientSocket.send(PreAmble.encode())
        bound1 = "--simple boundary\r\n"
        clientSocket.send(bound1.encode())

        # Text part
        message = input("Enter your message below\n")
        message = ("\r\n%s\r\n" % message)
        clientSocket.send(message.encode())

        # Picture part
        # picture encoded in base64
        bound2 = "--simple boundary\r\n"
        clientSocket.send(bound2.encode())
        clientSocket.send("Content-Type: image/jpg\r\n".encode())
        clientSocket.send("Content-Disposition:attachment;filename=picture.jpg\r\n".encode())
        clientSocket.send("Content-Transfer-Encoding:base64\r\n".encode())
        path = input("Write path of picture, or it's name if your in same directory\n")
        with open(path, "rb") as image2string: # open .jpg/image file and encode it
            converted_string = base64.b64encode(image2string.read())
        clientSocket.send("\r\n".encode())
        clientSocket.send(converted_string) # no need to encode, since it is already a byte-like object
        bound3 = "\r\n--simple boundary--\r\n"
        clientSocket.send(bound3.encode())
        end = "\r\n.\r\n"
        clientSocket.send(end.encode())
        recv7 = clientSocket.recv(1024).decode()
        print(recv7)
    else:
        dataCommand = "DATA\r\n"
        clientSocket.send(dataCommand.encode())
        recv4 = clientSocket.recv(1024).decode()
        print(recv4)
        if recv4[:3] != '354':
            print('354 reply not received from server.')
        # Subject
        subject = input("Subject: ")
        subCommand = ("Subject: %s\r\n" % subject)
        clientSocket.send(subCommand.encode())
        # Message
        message = input("Enter your message below\n")
        mesCommand = ("\r\n%s" % message)
        clientSocket.send(mesCommand.encode())
        # end
        end = "\r\n.\r\n"
        clientSocket.send(end.encode())
        recv7 = clientSocket.recv(1024).decode()
        print(recv7)

# QUIT
def quit(): # end session
    quit = "QUIT\r\n"
    clientSocket.send(quit.encode())
    recv8 = clientSocket.recv(1024).decode()
    print(recv8)
    if recv8[:3] != '221':
        print('221 reply not received from server.')

def menu():
    while(1):
        choice = input("M: Send mail\nQ: Quit\n")
        if (choice.lower() == 'm'):
            sender()
            to()
            sendMessage()
        elif (choice.lower() == 'q'):
            quit() # close connection
            exit(0)
        else:
            print("Please enter a valid character")

menu()
