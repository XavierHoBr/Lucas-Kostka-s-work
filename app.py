# -*- coding: utf-8 -*-
"""
    Simple sockjs-tornado-revealJS application, to allow realtime presentations on multiple devices 
	This projetc is an adaptation of this wondeful tutorial  by Shameer C on how to create multi-users 
	revealJS presentations in Javascript with Grunt, Yeoman, Node and SocketIO. It also relies on 
	the marvellous lib created by mrjoes (https://github.com/mrjoes/sockjs-tornado) that allows to bind
	SockJS to Tornado on the backend. Thanks to this plugin, I decided to try to do the 
	same as in the tutorial but with Python/Tornado on the backend, and SockJS instead of SocketIO. It worked for me, 
	so I hope it will work for you. As I hosted my presentation on Heroku, you should normally be able
	to host it on Heroku as it is. 

	For any comments or questions, please mail me at lucas.kostka@escdijon.eu. I'll do my best
	to answer as quickly as possible. 

	Finally, please Fork, correct and crictize, I am here to learn ;) Cheers !  
"""
import tornado.ioloop
import tornado.web
import sockjs.tornado
import os



class IndexHandler(tornado.web.RequestHandler):
    """Handler to serve the master presentation
		At the moment, there can be only one master 
		controlling the presentation changes. Two masters 
		will just result in the application crashing """
    def get(self):
        self.render('index.html')

class ClientHandler(tornado.web.RequestHandler):
    """Handler for clients, normally responsive"""
    def get(self):
        self.render('client.html')


class ChatConnection(sockjs.tornado.SockJSConnection):
    """SockJS connection implementation. This
	uses Tornado-SockJS plugin created by mrjoes, 
	available here: https://github.com/mrjoes/sockjs-tornado"""
    # Class level variable
    participants = set()


    def on_open(self, info):
        # Send that someone joined, it will show in 
	# browser console. The broadcast method here				
	# is a useufl way to update all connected clients on
	# event. It is proper to Tornado-SockJS lib. 

        # Add client to the clients list
        self.participants.add(self)

    def on_message(self, message):
	# While RevealJs listen on the event 'slidechanged', 
	# I did not achieve implementing this custom event here, so instead
	# Tornado-SockJS is listening on the traditionnal "on_message"

        self.broadcast(self.participants, message)

    def on_close(self):
        # Remove client from the clients list and broadcast leave message
        self.participants.remove(self)
        self.broadcast(self.participants, "Someone left.")

if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG) # Comment these two lines in production

    
    # This is the endpoint where sockJS client will connect. 
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection, '/presentation')

    # Our Tornado application routing
    app = tornado.web.Application([
		(r"/", IndexHandler),
		(r"/client", ClientHandler)
	] + ChatRouter.urls, # The .urls method will generate the urls associated with the endpoint itself. 
		debug = True,
		static_path = os.path.join(os.path.dirname(__file__), 'static'),
		template_path = os.path.join(os.path.dirname(__file__), 'templates'),
    )

    # I pushed that app on Heroku, so it will try to listen on the "PORT" env variable. 
    # Otherwise and for local test, it will listen on port 8080. You can change it if you want. 
    app.listen(os.environ.get('PORT', 8080))

    # Finally start Tornado IOLoop.  
    tornado.ioloop.IOLoop.instance().start()
