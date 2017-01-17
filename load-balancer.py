from socketserver import ThreadingTCPServer, StreamRequestHandler
import socket
import signal

should_serve = True

addresses = {
    'L': ('localhost', 8001),
    'P': ('localhost', 8002),
    'D': ('localhost', 8003)
}


class LoadBalancerTCPHandler(StreamRequestHandler):

    def handle(self):
        worker, data = self.rfile.readline().strip().decode('ascii').split(',')
        sock = socket.socket()
        sock.connect(addresses[worker])
        data += '\n'
        sock.sendall(data.encode('ascii'))
        response = sock.recv(4096).decode('ascii')
        sock.close()
        self.wfile.write(response.encode('ascii'))


def sigint_handler(signum, frame):
    global should_serve
    should_serve = False
    print('sigint')


if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    load_balancer = ThreadingTCPServer((HOST, PORT), LoadBalancerTCPHandler)

    signal.signal(signal.SIGINT, sigint_handler)

    while should_serve:
        print(should_serve)
        load_balancer.handle_request()

    print('Load Balancer shutdown')
