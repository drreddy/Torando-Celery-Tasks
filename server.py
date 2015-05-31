import os

from tornado.ioloop import IOLoop
from tornado.web import Application, RequestHandler, asynchronous
from tornado import gen
from tornado.httpserver import HTTPServer

import tcelery, tasks
import sockjs.tornado
from celery.task.control import inspect

import json

tcelery.setup_nonblocking_producer()

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")
        
class webSockConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()
    def on_open(self, info):   
        temp = {}
        temp['type'] = 'connectionLogs'
        temp['resp'] = 'connected'
        self.send(temp)
        # self.send(self.participants, "Someone joined.")
        self.participants.add(self)

    def on_message(self, message):
        # Broadcast message
        if message == "doTask":
            self.do_task()
        elif message == "getQueue":
            self.getQueueList()
        else:
            pass
            # self.broadcast(self.participants, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)
#         temp = {}
#         temp['type'] = 'connectionLogs'
#         temp['resp'] = 'disconnected'
#         self.send(temp)
        # self.broadcast(self.participants, "Someone left.")

    @gen.coroutine
    def do_task(self):
        response = yield gen.Task(tasks.sleep.apply_async, args=[5])
        temp = {}
        temp['type'] = 'taskCompletionData'
        temp['resp'] = json.dumps(response.result)
        self.send(temp)

    def getQueueList(self):
        i = inspect()
        temp = {}
        temp['type'] = 'queuedList'
        temp['resp'] = json.dumps(i.active())
        self.send(temp)

def main():
    
    sockRouter = sockjs.tornado.SockJSRouter(webSockConnection, '/wsconn')
    
    settings = {
        "template_path":os.path.join(os.path.dirname(__file__), "templates"),
        "debug": True
    }
    application = Application([
        (r"/", IndexHandler)
    ] + sockRouter.urls, **settings)
    http_server = HTTPServer(application)
    port = int(os.environ.get("PORT", 3000))
    http_server.listen(port)
    IOLoop.instance().start()

if __name__ == "__main__":
    main()