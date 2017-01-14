import sys
import socket

HOST, PORT = 'localhost', 8000


while True:
    command = input().strip()

    command += '\n'

    sock = socket.socket()
    sock.connect((HOST, PORT))
    sock.send(command.encode('ascii'))
    sock.close()
