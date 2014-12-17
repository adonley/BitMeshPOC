import zmq
import random
import sys
import time
import pairserver

port = "5556"
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.connect("tcp://localhost:%s" % port)

while True:
	socket.send(client_start_connection)
	time.sleep(1)
	msg = socket.recv()
	print msg



    #if(msg == server_start_connection):
    #	print msg
    #socket.send("client message to server2")

