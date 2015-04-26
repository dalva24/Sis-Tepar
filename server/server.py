#!/usr/bin/env python
# Grand Quest Server - SisTepar group

# Imports ==========================================================================
import socket
import json
import sys
import os
import hashlib
import datetime
import random
import inspect
import pickle

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
		self.newestItem = None

	def collect(self, name, amount):
		self.item[name] += amount
		return item2id(name)

	def mix(self, name1, name2):
		name1 = id2item(name1)
		name2 = id2item(name2)
		if name1[1] is name2[1]:
			if int(name1[2]) is int(name2[2])+1 or int(name1[2])+1 is int(name2[2]):
				if self.item[name1] >= 3 and self.item[name2] >= 3:
					self.item[name1] -= 3
					self.item[name2] -= 3
					resultantTier = int(name1[1]) + 1
					if int(name1[2] < name2[2]):
						self.item['R'+str(resultantTier)+name1[2]] += 1
						return item2id('R'+str(resultantTier)+name1[2])
					else:
						self.item['R'+str(resultantTier)+name2[2]] += 1
						return item2id('R'+str(resultantTier)+name2[2])
				else:
					raise Fail("Unable to craft: insufficient ingredients")
			else:
				raise Fail("Unable to craft: wrong recipe")
		else:
			raise Fail("Unable to craft: cannot mix different tiers")

	def xchange(self, bought, sold, boughtAmount, soldAmount):
			self.item[bought] += boughtAmount
			self.item[sold] -= soldAmount


class User:
	def __init__(self, name, pw):
		self.name = name
		self.pw = pw
		self.inv = Inventory()
		self.token = None
		self.location = None
		self.newLocation = None
		self.moveTime = None

	def invToList(self):
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

	def move(self, newLoc):
		if int(self.newLocation[0]) is int(self.location[0])+1 or int(self.newLocation[0]) is int(self.location[0])-1:
			if int(self.newLocation[1]) is int(self.location[1])+1 or int(self.newLocation[1]) is int(self.location[1])-1:
				self.newLocation = newLoc
				self.moveTime = random.randint(60, 120)   # TODO: time, and what happens when time reaches zero? threads?
				return self.moveTime
			else:
				raise Fail("move location is too far")
		else:
			raise Fail("move location is too far")


class UserContainer:
	user = []

	def __init__(self):
		file = open("savefile.obj", 'rb')
		self.user = pickle.load(file)

	def login(self, uname, pw):
		for usr in self.user:
			if usr.name is uname:
				if usr.pw is pw:
					time = str(datetime.datetime.now())
					usr.token = hashlib.md5(uname.encode()+pw.encode()+time.encode()).hexdigest()
					usr.location = str(random.randint(0, MAP.width-1)) + str(random.randint(0, MAP.height-1))
					return usr
				else:
					raise Fail("username/password combination is not found")
		raise Fail("username/password combination is not found")

	def signup(self, uname, pw):
		for usr in self.user:
			if usr.name is uname:
				raise Fail("username exists")
		self.user.append(User(uname, pw))
		return True

	def save(self):
		for usr in self.user:
			usr.token = None
			usr.location = None
			usr.newLocation = None
			usr.moveTime = None
		#with open("usersave.p","wb") as f:  # TODO fix
			#pickle.dump(self, f)
		#with open("users.json", "w") as f:
			#json.dump(self.user, f, default=lambda o: o.__dict__, indent=4)
			# i have NO IDEA how that ^ works, but whatever -_- just works.
			# indent optional.
		filehandler = open(b"savefile.obj", "wb")
		pickle.dump(self.user, filehandler)

	def mix(self, token, name1, name2):
		for usr in self.user:
			if usr.token is token:
				return usr.inv.mix(name1, name2)
		raise Fail("User not found")

	def inv(self, token):
		for usr in self.user:
			if usr.token is token:
				return usr.invToList()
		raise Fail("User not found")

	def move(self, token, newLoc):
		for usr in self.user:
			if usr.token is token:
				return usr.move(newLoc)
		raise Fail("User not found")

	def collect(self, token):
		for usr in self.user:
			if usr.token is token:
				item = MAP.items[usr.location[0]][usr.location[1]]
				return usr.inv.collect(item, 1)
		raise Fail("User not found")

	def offer(self, token, iSell, iBuy, iSellVal, iBuyVal):
		for usr in self.user:
			if usr.token is token:
				if usr.inv[id2item(iSell)] >= iSellVal: #TODO: check if possible to call dict straight away like this
					X.offer(iSell, iBuy, iSellVal, iBuyVal, usr.name)
					return True
				raise Fail("insufficient item")
		raise Fail("User not found")

	def getuserbox(self, token):
		for usr in self.user:
			if usr.token is token:
				return X.getuserbox(usr.name)
		raise Fail("User not found")

class Map:
	def __init__(self):
		with open(sys.argv[2]) as f:
			mapdata = json.load(f)
		self.name = mapdata['name']
		self.width = mapdata['width']
		self.height = mapdata['height']
		self.items = mapdata['map']


class Xchange:
	def __init__(self):
		self.stock = []
		self.server = []

	def addServer(self, ip, port):
		self.server.append(Server(ip, port))

	def offer(self, iSell, iBuy, iSellVal, iBuyVal, user):
		self.stock.append(XItem(iSell, iBuy, iSellVal, iBuyVal, user))

	def transaction(self, token):  # TODO fix
		for stk in self.stock:
			if stk.token is token:
				stk.sold = True
		raise Fail("User not found")

	def formatStockList(self, stockList):
		retStr = "["
		for stock in stockList:
			retStr += "["
			retStr += item2id(stock.iSell)
			retStr += ","
			retStr += str(stock.iSellVal)
			retStr += ","
			retStr += item2id(stock.iBuy)
			retStr += ","
			retStr += str(stock.iBuyVal)
			retStr += ","
			retStr += not stock.sold
			retStr += ","
			retStr += stock.token
			retStr += "]"
			retStr += ","
		retStr += retStr[:-1]
		retStr += "]"
		return retStr

	def getuserbox(self, user):
		userstk = []
		for stk in self.stock:
			if stk.user is user:
				userstk.append(stk)
		return self.formatStockList(userstk)

	def find(self, user, iBuy):
		retstk = []
		for stk in self.stock:
			if stk.iSell is iBuy and stk.user is not user:
				retstk.append(stk)
		for srv in self.server:
			# TODO call findOffer
			for stk in srv:
				if stk.iSell is iBuy and stk.user is not user:
					retstk.append(stk)
		return self.formatStockList(retstk)

	def findInSelf(self, item):
		retstk = []
		for stk in self.stock:
			if stk.iSell is item:
				retstk.append(stk)
		return self.formatStockList(retstk)



class XItem:
	def __init__(self, iSell, iBuy, iSellVal, iBuyVal, user):
		self.iBuy = iBuy
		self.iSell = iSell
		self.iBuyVal = iBuyVal
		self.iSellVal = iSellVal
		self.user = user
		self.sold = False
		time = str(datetime.datetime.now())
		self.token = hashlib.md5(self.iBuy.encode()+self.iSell.encode()+time.encode()).hexdigest()


class Server:
	def __init__(self, ip, port):
		self.ip = ip;
		self.port = port
		self.stock = []


# Exceptions =======================================================================
class Fail(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return repr(self.msg)


# Functions ========================================================================
def lineno():
	return inspect.currentframe().f_back.f_lineno


def id2item(val):
	translator = {
		0: 'R11',
		1: 'R12',
		2: 'R13',
		3: 'R14',
		4: 'R21',
		5: 'R22',
		6: 'R23',
		7: 'R31',
		8: 'R32',
		9: 'R41'
	}
	return translator[val]


def item2id(name):
	translator = {
		'R11': 0,
		'R12': 1,
		'R13': 2,
		'R14': 3,
		'R21': 4,
		'R22': 5,
		'R23': 6,
		'R31': 7,
		'R32': 8,
		'R41': 9
	}
	return translator[name]


# Prep =============================================================================
if len(sys.argv) < 3:
	sys.exit('Usage: server.py port mapfile\nAvailable mapfiles:\n  map1.json ')

if not os.path.exists(sys.argv[2]):
	sys.exit('ERROR: Map %s was not found!' % sys.argv[2])

TCP_IP = '127.0.0.1'  # TODO: customize self IP from argv
TCP_PORT = int(sys.argv[1])

TRAC_IP = '127.0.0.1'
TRAC_PORT = 8000

MAP = Map()
UC = UserContainer()
X = Xchange()

BUFFER_SIZE = 4096

#print("Broadcasting self existence to Tracker...")
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((TRAC_IP, TRAC_PORT))
#a = json.dumps({"method": "join", "ip": TCP_IP, "port": TCP_PORT})
#s.send(a.encode('utf-8'))
#packet = json.loads(s.recv(BUFFER_SIZE))
#OTHER_SERVERS = None
#if packet['status'] == 'ok':
	#OTHER_SERVERS = packet['value']
#else:
	#sys.exit("ERROR: " + packet['description'])
#s.close()

print("Binding port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

MAIN_LOOP = True

SRVT = "0"  # TODO TIME using epoch time in UTC


# Functions ========================================================================


# Main Loop =============================================================================

print("Server Init Completed. Listening...")
while MAIN_LOOP is True:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE).decode('utf-8')
	print("New LoliCON")
	if str(data) is "":
		print("PING")
	else:  # handleJSON
		#try:
			packet = json.loads(str(data))
			if packet['method'] == 'serverStatus':
				OTHER_SERVERS = packet['server']
				msg = {'status': 'ok'}
				conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'signup':
				try:
					if UC.signup(packet['username'], packet['password']):
						msg = {'status': 'ok'}
						conn.send(json.dumps(msg).encode('utf-8'))
					else:
						msg = {'status': 'error'}
						conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'login':
				try:
					usrv = UC.login(packet['username'], packet['password'])
					msg = {
						'status': 'ok',
						'token': usrv.token,
						'x': usrv.location[0],
						'y': usrv.location[1],
						'time': SRVT  # TODO TIME
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print(UC.user[0].name)
					print(UC.user[0].pw)
			elif packet['method'] == 'inventory':
				try:
					msg = {
						'status': 'ok',
						'inventory': str(UC.inv(packet['token']))
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'mixitem':
				try:
					msg = {
						'status': 'ok',
						'item': UC.mix(packet['token'], packet['item1'], packet['item2'])
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'map':
				msg = {
					'status': 'ok',
					'name': MAP.name,
					'width': MAP.width,
					'height': MAP.height
				}
				conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'move':
				try:
					msg = {
						'status': 'ok',
						'time': UC.move(packet['token'], str(packet['x'] + str(packet['y'])))  # TODO TIME
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'field':
				try:
					msg = {
						'status': 'ok',
						'item': UC.collect(packet['token'])
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'offer':
				try:
					UC.offer(packet['token'], packet['offered_item'], packet['n1'], packet['demanded_item'], packet['n2'])
					msg = {
						'status': 'ok'
					}
					conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'fail',
						'description': e.msg
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'tradebox':
				try:
					userbox = UC.getuserbox(packet['token'])
					msg = '{"status": "ok", "offers": ' + userbox + '}'
					conn.send(msg.encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'error'
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'sendfind':
				print("nop")
			elif packet['method'] == 'findoffer':
				try:
					items = X.findInSelf(id2item(packet['item']))
					msg = '{"status": "ok", "offers": ' + items + '}'
					conn.send(msg.encode('utf-8'))
				except Fail as e:
					print("an operation has failed - " + lineno())
					print(e.msg)
					msg = {
						'status': 'error'
					}
					conn.send(json.dumps(msg).encode('utf-8'))
			elif packet['method'] == 'sendaccept':
				print("nop")
			elif packet['method'] == 'accept':
				print("nop")
			elif packet['method'] == 'fetchitem':
				print("nop")
			elif packet['method'] == 'killserver':
				if packet['magicString'] == 'q34tAq34tb3qy4IUaXa4t':
					print("Shutting down server...")
					MAIN_LOOP = False
				else:
					print("WARNING: intrusion attempt")
			else:
				print("unknown connection method.")
		#except Exception as ex:
		#	print("ERROR: unknown exception in handling connection data.")
		#	print(ex)

	# conn.shutdown('SHUT_RDWR')
	conn.close()
	UC.save()  # save aaaall the time. really safe for times when server suddenly crash for no reason whatsoever.

# Cleanup =============================================================================
