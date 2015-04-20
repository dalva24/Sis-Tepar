#!/usr/bin/env python
# Grand Quest Server - SisTepar group

#Imports ===========================================================================
import socket
import json
import sys

#Functions ==========================================================================


#Prep =============================================================================
MAIN_LOOP = True
TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])
TRAC_IP = '127.0.0.1'
TRAC_PORT = '8000'
BUFFER_SIZE = 1024 #TODO: check specified buffsize

print("Broadcasting self existence to Tracker...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TRAC_IP, TRAC_PORT))
s.send("stringhere".encode('utf-8')) #TODO: send self existence (join) #TAIGA#
s.close()

print("Binding port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

#Main Loop =============================================================================
print("Server Init Completed. Listening...")
while (MAIN_LOOP == True) :
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	print("New LoliCON")
	if (data != "") :
		#process ping (kayanya ga perlu)
	else #handle JSON
		packet = json.loads(data)
		if (packet['method'] == 'serverStatus') #TAIGA#
			# process
		elif (packet['method'] == 'signup')
			# process
		elif (packet['method'] == 'login')
			# process
		elif (packet['method'] == 'inventory')
			# process
		elif (packet['method'] == 'mixitem')
			# process
		elif (packet['method'] == 'map')
			# process
		elif (packet['method'] == 'move')
			# process
		elif (packet['method'] == 'offer')
			# process
		elif (packet['method'] == 'tradebox')
			# process
		elif (packet['method'] == 'sendfind')
			# process
		elif (packet['method'] == 'findoffer')
			# process
		elif (packet['method'] == 'sendaccept')
			# process
		elif (packet['method'] == 'accept')
			# process
		elif (packet['method'] == 'fetchitem')
			# process
		else
			#ERROR not found
		
	conn.shutdown('SHUT_RDWR')
	conn.close()

#Cleanup =============================================================================

