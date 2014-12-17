import zmq
import random
import sys
import time

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

# start connection phrease
client_start_connection = 'HI'

# start connection response
server_start_connection = "HELLO"

# end connection phrase
end_connection = 'END'

while True:
    
    msg = socket.recv()
    print msg

    # handle connection states
    if(msg == client_start_connection):
    	time.sleep(.5)
    	socket.send(server_start_connection)
    elif(msg == end_connection):
    	socket.sent(end_connection)

    print msg

