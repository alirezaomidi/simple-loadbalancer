import sys
from socketserver import ThreadingTCPServer, StreamRequestHandler
from redis import StrictRedis
import signal

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB_NO = 0
db = None

should_serve = True


class WorkerTCPHandler(StreamRequestHandler):

    def handle(self):
        number = self.rfile.readline().strip()
        if db.get(number) is None:
            self.wfile.write('registration completed'.encode('ascii'))
        else:
            self.wfile.write('has been registered before'.encode('ascii'))
        db.incr(number)


def sigint_handler(signum, frame):
    global should_serve
    should_serve = False


if __name__ == '__main__':

    try:
        global REDIS_DB_NO
        HOST = 'localhost'
        PORT, REDIS_DB_NO = map(int, sys.argv[1:])
    except Exception as e:
        print(e, file=sys.stderr)

    global db
    db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB_NO)

    worker = ThreadingTCPServer((HOST, PORT), WorkerTCPHandler)

    signal.signal(signal.SIGINT, sigint_handler)

    while should_serve:
        worker.handle_request()

    print('worker %d shutdown' % PORT)
