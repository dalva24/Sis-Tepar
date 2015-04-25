#!/usr/bin/env python
# Grand Quest Server - SisTepar group

# Imports ==========================================================================
import socket
import json
import sys
import os
import hashlib
import datetime


# Classes ==========================================================================
class Inventory:
	def __init__(self):
		self.item = {
			'R11': 0,
			'R12': 0,
			'R13': 0,
			'R14': 0,
			'R21': 0,
			'R22': 0,
			'R23': 0,
			'R31': 0,
			'R32': 0,
			'R41': 0
		}

	def collect(self, name, amount):
		self.item[name] += amount
		return True

	def mix(self, name1, name2):
		if name1[1] is name2[1]:
			if int(name1[2]) is int(name2[2])+1 or int(name1[2])+1 is int(name2[2]):
				if self.item[name1] >= 3 and self.item[name2] >= 3:
					self.item[name1] -= 3
					self.item[name2] -= 3
					resultantTier = int(name1[1]) + 1
					if int(name1[2] < name2[2]):
						self.item['R'+str(resultantTier)+name1[2]] += 1
					else:
						self.item['R'+str(resultantTier)+name2[2]] += 1
					return True
				else:
					return "Unable to craft: insufficient ingredients"
			else:
				return "Unable to craft: wrong recipe"
		else:
			return "Unable to craft: cannot mix different tiers"


def xchange(self, bought, sold, boughtAmount, soldAmount):
		self.item[bought] += boughtAmount
		self.item[sold] -= soldAmount


class User:
	def __init__(self, name, pw):
		self.name = name
		self.pw = pw
		self.inv = Inventory()
		self.token = False
		self.location = False

	def getInventory(self):
		return [
			self.inv.item['R11'],
			self.inv.item['R12'],
			self.inv.item['R13'],
			self.inv.item['R14'],
			self.inv.item['R21'],
			self.inv.item['R22'],
			self.inv.item['R23'],
			self.inv.item['R31'],
			self.inv.item['R32'],
			self.inv.item['R41']
		]


class UserContainer:
	user = []

	def __init__(self):
		print("TODO") # TODO: JSON save file loader

	def add(self, usr):
		self.user.append(usr)

	def login(self, uname, pw):
		for usr in self.user:
			if usr.name is uname:
				if usr.pw is pw:
					time = str(datetime.datetime.now())
					usr.token = hashlib.md5(uname.encode()+pw.encode()+time.encode()).hexdigest()
					return True
				else:
					return "username/password combination is not found"

	def signup(self, uname, pw):
		for usr in self.user:
			if usr.name is uname:
				return "username exists"
		self.user.append(User(uname, pw))
		return True


class Map:  # TODO: map JSON loader etc
	def __init__(self):
		map = MAP_FILE


# Functions ==========================================================================

# Prep =============================================================================
if len(sys.argv) < 3:
	sys.exit('Usage: server.py port mapfile\nAvailable mapfiles:\n  map1.json ')

if not os.path.exists(sys.argv[2]):
	sys.exit('ERROR: Map %s was not found!' % sys.argv[2])

TCP_IP = '127.0.0.1'
TCP_PORT = int(sys.argv[1])

TRAC_IP = '127.0.0.1'
TRAC_PORT = '8000'

BUFFER_SIZE = 1024  # TODO: check specified buffsize

MAP_FILE = sys.argv[2]

ip = '192.168.1.112'
port = 8000
a = json.dumps({"method": "join", "ip": ip, "port": port})

print("Broadcasting self existence to Tracker...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TRAC_IP, TRAC_PORT))
s.send(a.encode('utf-8'))  # TODO: send self existence (join) #TAIGA#
packet = json.loads(s.recv(BUFFER_SIZE))
if packet['status'] == 'ok':
	otherServers = packet['value']
else:
	print("ERROR: " + packet['description'])
s.close()

print("Binding port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

MAIN_LOOP = True


# Main Loop =============================================================================
print("Server Init Completed. Listening...")
while MAIN_LOOP is True:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE)
	print("New LoliCON")
	if data != "":
		print("PING")
	else:  # handleJSON
		packet = json.loads(data)
		if packet['method'] == 'serverStatus':  # TAIGA #
			print("nop")
		elif packet['method'] == 'signup':
			print("nop")
		elif packet['method'] == 'login':
			print("nop")
		elif packet['method'] == 'inventory':
			print("nop")
		elif packet['method'] == 'mixitem':
			print("nop")
		elif packet['method'] == 'map':
			print("nop")
		elif packet['method'] == 'move':
			print("nop")
		elif packet['method'] == 'offer':
			print("nop")
		elif packet['method'] == 'tradebox':
			print("nop")
		elif packet['method'] == 'sendfind':
			print("nop")
		elif packet['method'] == 'findoffer':
			print("nop")
		elif packet['method'] == 'sendaccept':
			print("nop")
		elif packet['method'] == 'accept':
			print("nop")
		elif packet['method'] == 'fetchitem':
			print("nop")
		elif packet['method'] == 'killserver':
			if packet['magicString'] == 'q34tAq34tb3qy4IUaXa4t':
				MAIN_LOOP = False
			else:
				print("WARNING: intrusion attempt")
		else:
			print("unknown connection method.")

	conn.shutdown('SHUT_RDWR')
	conn.close()


# Cleanup =============================================================================
# TODO: save all stuff
