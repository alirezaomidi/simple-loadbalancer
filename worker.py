import sys
from socketserver import ThreadingTCPServer, StreamRequestHandler
from redis import StrictRedis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB_NO = 0
db = None


class WorkerTCPHandler(StreamRequestHandler):

    def handle(self):
        number = self.rfile.readline().strip()
        if db.get(number) is None:
            print('registered')
        else:
            print(db.get(number))
        db.incr(number)


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

    worker.serve_forever()
