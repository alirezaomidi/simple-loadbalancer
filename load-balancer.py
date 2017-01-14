from socketserver import ThreadingTCPServer, StreamRequestHandler
import socket


class LoadBalancerTCPHandler(StreamRequestHandler):

    WORKERS = {
        'L': ('localhost', 8001),
        'P': ('localhost', 8002),
        'D': ('localhost', 8003)
    }

    def handle(self):
        worker, data = self.rfile.readline().strip().decode('ascii').split(',')
        print(worker, data)
        sock = socket.socket()
        sock.connect(self.WORKERS[worker])
        sock.sendall(data.encode('ascii'))
        sock.close()


if __name__ == '__main__':
    HOST, PORT = 'localhost', 8000

    load_balancer = ThreadingTCPServer((HOST, PORT), LoadBalancerTCPHandler)

    load_balancer.serve_forever()
