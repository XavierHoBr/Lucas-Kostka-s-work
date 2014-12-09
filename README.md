tornado-sockjs-revealjs
=======================

A RevealJS presentation with tornado and sockJS to allow realtime sliding on every types of devices. 
This is my first project, so please don't hesitate to criticize it. It would help me improve ;) 

Dependencies: 

* Tornado-SockJS by mrjoes (https://github.com/mrjoes/sockjs-tornado) that I thank a lot for this amazing lib. 
* While not a dependency, it is written in python 2.7. 

Purpose : 

This project is fully inspired from Shameer C. excellent tutorial 
(http://www.sitepoint.com/create-multi-user-presentation-reveal-js/) to create multi-user presentation with revealJS
The stack used in the tutorial was only Javascript (Yeoman, Grunt and Node.js) and so as I am learning python, I wanted
to try to adapt the app with a python backend. I used tornado for it (because of its ease for handling websockets and the 
existence of the marvellous lib from mrjoes) and sockJS instead of socketIO used in the tutorial. Ngrok (awesome too) is 
present to allow you testing, or use it for your final presentation. You'll be abl to test the realtime changing effect
only through tunneling with ngrok (local test on 0.0.0.0:8080 won't produce any change) 

And RevealJS is freaking awesome !

Heroku-ready: 

The presentation was hosted on heroku so it should normally work for you (normally :p) Still heroku did 
not accept http, ws and wss:// protocols for connecting, so the application is using https, while there is no ssl connection
setup. I would be eternally grateful to anyone willing to point me to the right direction to solve that problem. 

Client / Master : 

In the templates folder, you will find client.html and index.html files. The two files only differ in the SockJS 
possibilities present in the file. The index.html has an additional "notifyServer" function to send event-changes
informations to the server. That way, index.html is the master controlling the presentation. 

HOW TO RUN : 

1/ Init a virtual environment in the folder where you want your application to reside with: 

                        virtualenv virtual_environment_name

2/ CD in this envrionment and activate it with source bin/activate. If everything works fine you should see 
(virtual_environment_name) appear at the beginning of the shell line. 

3/ Clone the repo : git clone https://github.com/coffee-mug/tornado-sockjs-revealjs.git

4/ Go in the folder tornado-sockjs-revealjs and install everything with (Your virtual_environment should still
be activated, it won't work otherwise. Go step 2 in case of troubles) : 
                        pip install -r requirements.txt

5/ Right. Now launch the app in local with : 
                        python app.py
  The server will listen to port 8080, so you can basically go in your browser and go : 
                        http://0.0.0.0:8080 to access the master and 
                        http://0.0.0.0/8080/client to access the client presentation
                        
5.bis/ The example presentation is mine, feel free to criticize, even if there is not much information :p 

6/ To test out the realtime, open another tab in your shell and type :
                        ./ngrok 8080
  You should see ngrok launching and telling you on which URL to connect. Following the same rules as before, go
  in your browser and type the ngrok address give you. To control the presentation, just use the ngrok address, to 
  see presentation change on client, just open a new tab in your browser with ngrok address suffixed with /client.
  
  You can also test to control your presentation from your mobile and see real-time updates on your laptop for instance.
  That is what I used for this presentation and it was really cool ! 
  

EXAMPLE : 

If you want to see it in action before playing with it, just go to http://welovemarketresearch.herokuapp.com and http://welovemarketresearch.herokuapp.com/client in another browser tab, window or device. Every change on welovemarketresearch.herokuapp.com will be repercuted on welovemarketresearch.herokuapp.com/client 


  TROUBLESHOOTING : do not hesitate to report any bugs or difficulties on Github or to send me an email. 
  
  Hoping you could have some fun with it, Cheers ! 
