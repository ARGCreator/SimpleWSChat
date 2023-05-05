# SimpleWSChat

A simple Web Sockets Server and Client Example, using Web Sockets, and asyncio, with command handling example built in.


To install required modules: pip install -r requirements.txt


Be sure to run the Server first, that way the clients can connect to something.

To get the server online: python server.py
To get clients online (Autoconnected, each run in multiple windows to get multiple chatters): python client.py


There's one included slash command, along with command handling. this command is: 
/nick <new_nickname_here>
