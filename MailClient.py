from socket import *
import base64
import ssl
import sys

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ('smtp.gmail.com', 587)

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024)
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')

# Send HELO command and print server response.
heloCommand = 'HELO Alice\r\n'
clientSocket.send(heloCommand)
recv1 = clientSocket.recv(1024)
print(recv1)
if recv1[:3] != '250':
    print('250 reply not received from server.')


# Send STARTTLS command and print server response.
command="STARTTLS\r\n"
clientSocket.send(command.encode())
recv2 = clientSocket.recv(1024)
print(recv2)
if recv2[:3] != '220':
    print('220 reply not received from server.')

tlsSocket=ssl.wrap_socket(clientSocket)

#Username informations.
username = "username@gmail.com"                     
password = "****"                                    
base64_str = ("\x00"+username+"\x00"+password).encode()
base64_str = base64.b64encode(base64_str)
authMsg = "AUTH PLAIN ".encode()+base64_str+"\r\n".encode()
tlsSocket.send(authMsg)
recv3 = tlsSocket.recv(1024)
print(recv3.decode())
if recv3[:3] != '235':
    print('235 reply not received from server.')


# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <username@gmail.com> \r\n"
tlsSocket.send(mailFrom.encode())
recv4 = tlsSocket.recv(1024)
print(recv4)
if recv4[:3] != '250':
    print('250 reply not received from server.')

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <username@gtu.edu.tr> \r\n"
tlsSocket.send(rcptTo.encode())
recv5 = tlsSocket.recv(1024)
print(recv5)
if recv5[:3] != '250':
    print('250 reply not received from server.')

# Send DATA command and print server response.
data = "DATA\r\n"
tlsSocket.send(data.encode())
recv6 = tlsSocket.recv(1024)
print(recv6)
if recv6[:3] != '354':
    print('354 reply not received from server.')

# Send message data.
subject = "Subject: SMTP mail client testing \r\n\r\n"
print('The message is: I love computer networks!\n')
tlsSocket.send(subject.encode())
tlsSocket.send(msg.encode())
tlsSocket.send(endmsg.encode())
recv7 = tlsSocket.recv(1024)
print(recv7.decode())
if recv7[:3] != '250':
    print('250 reply not received from server.')

# Send QUIT command and get server response.
tlsSocket.send("QUIT\r\n".encode())
message = tlsSocket.recv(1024)
print(message)
tlsSocket.close()