import socket

if __name__ == '__main__':

    while True:
        command = input().strip()

        command += '\n'

        sock = socket.socket()
        status = sock.connect(('localhost', 8000))

        sock.sendall(command.encode('ascii'))
        response = sock.recv(4096).decode('ascii')
        print(response)
