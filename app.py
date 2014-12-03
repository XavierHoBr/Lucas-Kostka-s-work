# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado chat application. By default will listen on port 8080 (for local use).
"""
import tornado.ioloop
import tornado.web

import sockjs.tornado

import os

class IndexHandler(tornado.web.RequestHandler):
    """Handler to serve the master presentation"""
    def get(self):
        self.render('index.html')

class ClientHandler(tornado.web.RequestHandler):
    """Handler for clients"""
    def get(self):
        self.render('client.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """Chat connection implementation"""
    # Class level variable
    participants = set()

    def on_open(self, info):
        # Send that someone joined
        self.broadcast(self.participants, "Someone joined.")

        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
        print "Message recu {}".format(message)
        self.broadcast(self.participants, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)

        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/presentation')

    # 2. Create Tornado application
    app = tornado.web.Application([
		(r"/", IndexHandler),
		(r"/client", ClientHandler)
	] + ChatRouter.urls,
			debug = True,
			static_path = os.path.join(os.path.dirname(__file__), 'static'),
    )

    # 3. Make Tornado app listen on os.environ.PORT if used on Heroku, otherwise on port 8080
    app.listen(os.environ.get('PORT', 8080))

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
