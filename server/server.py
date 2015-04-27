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
import time
import calendar
import threading

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
		if name1[1] == name2[1]:
			if int(name1[2]) == int(name2[2])+1 or int(name1[2])+1 == int(name2[2]):
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
		l = list()
		l.append(self.inv.item['R11'])
		l.append(self.inv.item['R12'])
		l.append(self.inv.item['R13'])
		l.append(self.inv.item['R14'])
		l.append(self.inv.item['R21'])
		l.append(self.inv.item['R22'])
		l.append(self.inv.item['R23'])
		l.append(self.inv.item['R31'])
		l.append(self.inv.item['R32'])
		l.append(self.inv.item['R41'])
		return l

	def move(self, newLoc):
		if int(newLoc[0]) == int(self.location[0])+1 or int(newLoc[0]) == int(self.location[0])-1 or int(newLoc[0]) == int(self.location[0]):
			if int(newLoc[1]) == int(self.location[1])+1 or int(newLoc[1]) == int(self.location[1])-1 or int(newLoc[1]) == int(self.location[1]):
				self.newLocation = newLoc
				ttm = random.randint(10, 30)
				self.moveTime = srvTime() + ttm
				t = threading.Thread(target=self.doMove)
				t.start()
				print("moving user " + self.name + " in " + str(self.moveTime-srvTime()) + " seconds")
				return self.moveTime
			else:
				print(newLoc + ' - ' + self.location)
				raise Fail("Move Y too far")
		else:
			print(newLoc + ' - ' + self.location)
			raise Fail("Move X too far")

	def doMove(self):
		time.sleep(self.moveTime-srvTime())
		self.location = self.newLocation
		self.newLocation = None
		print("user has been moved: " + self.name + " to " + self.location)


class UserContainer:
	user = []

	def __init__(self):
		file = open("savefile.obj", 'rb')
		self.user = pickle.load(file)

	def login(self, uname, pw):
		for usr in self.user:
			if usr.name == uname:
				if usr.pw == pw:
					time = str(datetime.datetime.now())
					usr.token = hashlib.md5(uname.encode()+pw.encode()+time.encode()).hexdigest()
					usr.location = str(random.randint(0, MAP.width-1)) + str(random.randint(0, MAP.height-1))
					return usr
				else:
					raise Fail("incorrect password")
		raise Fail("username not found")

	def signup(self, uname, pw):
		for usr in self.user:
			if usr.name == uname:
				raise Fail("username exists")
		self.user.append(User(uname, pw))
		return True

	def save(self):
		# with open("usersave.p","wb") as f:
			# pickle.dump(self, f)
		# with open("users.json", "w") as f:
			# json.dump(self.user, f, default=lambda o: o.__dict__, indent=4)
			# i have NO IDEA how that ^ works, but whatever -_- just works.
			# indent optional.
		filehandler = open(b"savefile.obj", "wb")  # dont fix binary warning. it works.
		pickle.dump(self.user, filehandler)

	def shutdown(self):
		for usr in self.user:
			usr.token = None
			usr.newLocation = None
			usr.moveTime = None

	def mix(self, token, name1, name2):
		for usr in self.user:
			if usr.token == token:
				return usr.inv.mix(name1, name2)
		raise Fail("User not found")

	def inv(self, token):
		for usr in self.user:
			if usr.token == token:
				return usr.invToList()
		raise Fail("User not found")

	def move(self, token, newLoc):
		for usr in self.user:
			if usr.token == token:
				return usr.move(newLoc)
		raise Fail("User not found")

	def collect(self, token):
		for usr in self.user:
			if usr.token == token:
				item = MAP.items[int(usr.location[0])][int(usr.location[1])]
				return usr.inv.collect(item, 1)
		raise Fail("User not found")

	def offer(self, token, iSell, iBuy, iSellVal, iBuyVal):
		for usr in self.user:
			if usr.token == token:
				if usr.inv.item[id2item(iSell)] >= iSellVal:
					X.offer(iSell, iBuy, iSellVal, iBuyVal, usr.name)
					return True
				raise Fail("insufficient item")
		raise Fail("User not found")

	def getuserbox(self, token):
		for usr in self.user:
			if usr.token == token:
				return X.getuserbox(usr.name)
		raise Fail("User not found")

	def cancelOffer(self, token, itemtok):
		for usr in self.user:
			if usr.token == token:
				return X.cancel(itemtok)
		raise Fail("User not found")

	def find(self, token, itemID):
		for usr in self.user:
			if usr.token == token:
				return X.find(usr.name, itemID)
		raise Fail("User not found")

	def fetch(self, token, itemTok):
		for usr in self.user:
			if usr.token == token:
				fetched = X.fetchInSelf(usr.name, itemTok)
				usr.inv.collect(id2item(fetched[0]), fetched[1])
				return True
		raise Fail("User not found")

	def acceptOffer(self, token, itemTok):
		for usr in self.user:
			if usr.token == token:
				fetched = X.accept(usr.name, itemTok)
				usr.inv.collect(id2item(fetched[0]), fetched[1])
				return True
		raise Fail("User not found")

class Map:
	def __init__(self, name):
		with open(name) as f:
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

	def formatStockList(self, stockList):
		retStr = "["
		for stock in stockList:
			retStr += "["
			retStr += str(stock.iSell)
			retStr += ","
			retStr += str(stock.iSellVal)
			retStr += ","
			retStr += str(stock.iBuy)
			retStr += ","
			retStr += str(stock.iBuyVal)
			retStr += ","
			if stock.sold:
				retStr += "false"
			else:
				retStr += "true"
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
			if stk.user == user:
				userstk.append(stk)
		return self.formatStockList(userstk)

	def find(self, user, iBuy):
		retstk = []
		for stk in self.stock:
			if stk.iSell == iBuy and stk.user != user and stk.sold is False:
				retstk.append(stk)
		for srv in self.server:
			sendMsg(json.dumps({"method": "findoffer", "item": iBuy}), srv.ip, srv.port)
			for stk in srv:
				if stk.iSell == iBuy and stk.user != user and stk.sold is False:
					retstk.append(stk)
		return self.formatStockList(retstk)

	def findInSelf(self, item):
		retstk = []
		for stk in self.stock:
			if stk.iSell == item and stk.sold is False:
				retstk.append(stk)
		return self.formatStockList(retstk)

	def fetchInSelf(self, usr, itID):
		for stk in self.stock:
			if stk.token == itID and stk.sold is True and stk.user == usr:
				return [stk.iBuy, stk.iBuyVal]
		raise Fail("item not found")

	def acceptInSelf(self, token):
		for stk in self.stock:
			if stk.token == token:
				self.stock.remove(stk)
				return True
		raise Fail("offer is not available")

	def cancel(self, token):
		for stk in self.stock:
			if stk.token == token:
				if stk.sold:
					raise Fail("item has been sold")
				else:
					self.stock.remove(stk)
					return True
		raise Fail("item not found")

	def accept(self, usr, itID):
		for stk in self.stock:
			if stk.token == itID and stk.user != usr and stk.sold is False:
				stk.sold = True
				return [stk.iBuy, stk.iBuyVal]
		# then if in self inventory is not found:
		for srv in self.server:
			for stk in srv:
				if stk.token == itID and stk.user != usr and stk.sold is False:
					return [stk.iBuy, stk.iBuyVal]
				sendMsg(json.dumps({"method": "accept", "offer_token": stk.token}), srv.ip, srv.port)
		raise Fail("item not found")


class XItem:
	def __init__(self, iSell, iBuy, iSellVal, iBuyVal, user):
		self.iBuy = iBuy
		self.iSell = iSell
		self.iBuyVal = iBuyVal
		self.iSellVal = iSellVal
		self.user = user
		self.sold = False
		self.token = '0'+hex(random.getrandbits(128))[2:-1]


class Server:
	def __init__(self, ip, port):
		self.ip = ip
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
	return str(inspect.currentframe().f_back.f_lineno)


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


def prepFailJSON(ex, no):
	print("an operation has failed at line " + no + " - " + ex.msg)
	jmsg = {
		'status': 'fail',
		'description': e.msg
	}
	return json.dumps(jmsg).encode('utf-8')


def srvTime():
	return calendar.timegm(time.gmtime())


def sendMsg(msg, ip, port):
	srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	srv.connect((ip, port))
	# m = json.dumps({"method": "join", "ip": TCP_IP, "port": TCP_PORT})
	srv.send(msg.encode('utf-8'))
	packet = json.loads(srv.recv(BUFFER_SIZE))
	if packet['status'] != 'ok':
		raise Fail(packet['description'])
	srv.close()
	return True


# Prep =============================================================================
if len(sys.argv) < 4:
	sys.exit('Usage: server.py self-ip port mapfile (optional)notrack\nAvailable mapfiles:\n  map1.json ')

if not os.path.exists(sys.argv[3]):
	sys.exit('ERROR: Map %s was not found!' % sys.argv[3])

TCP_IP = sys.argv[1]
TCP_PORT = int(sys.argv[2])

TRAC_IP = '167.205.32.46'
TRAC_PORT = 8000

MAP = Map(sys.argv[3])
UC = UserContainer()
X = Xchange()

BUFFER_SIZE = 4096

if len(sys.argv) < 3:
	print("Broadcasting self existence to Tracker...")
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TRAC_IP, TRAC_PORT))
	a = json.dumps({"method": "join", "ip": TCP_IP, "port": TCP_PORT})
	s.send(a.encode('utf-8'))
	packet = json.loads(s.recv(BUFFER_SIZE))
	OTHER_SERVERS = None
	if packet['status'] == 'ok':
		OTHER_SERVERS = packet['value']
	else:
		sys.exit("ERROR: " + packet['description'])
	s.close()

print("Binding port...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

MAIN_LOOP = True


# Main Loop =============================================================================

print("Server Init Completed. Listening...")
while MAIN_LOOP:
	conn, addr = s.accept()
	data = conn.recv(BUFFER_SIZE).decode('utf-8')
	print("== New LoliCON ==")
	if str(data) == "":
		print("PING")
	else:  # handleJSON
		# try:
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
						print("  user signed up: " + packet['username'])
					else:
						msg = {'status': 'error'}
						conn.send(json.dumps(msg).encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'login':
				try:
					usrv = UC.login(packet['username'], packet['password'])
					msg = {
						'status': 'ok',
						'token': usrv.token,
						'x': usrv.location[0],
						'y': usrv.location[1],
						'time': srvTime()
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  user logged in: " + packet['username'])
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'inventory':
				try:
					msg = {
						'status': 'ok',
						'inventory': UC.inv(packet['token'])
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  user token checked inventory: " + packet['token'])
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'mixitem':
				try:
					msg = {
						'status': 'ok',
						'item': UC.mix(packet['token'], packet['item1'], packet['item2'])
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  user token mixed item: " + packet['token'])
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'map':
				msg = {
					'status': 'ok',
					'name': MAP.name,
					'width': MAP.width,
					'height': MAP.height
				}
				conn.send(json.dumps(msg).encode('utf-8'))
				print("  map checked")
			elif packet['method'] == 'move':
				try:
					msg = {
						'status': 'ok',
						'time': UC.move(packet['token'], str(packet['x']) + str(packet['y']))
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  moving user token: " + packet['token'] + " to " + str(packet['x']) + str(packet['y']))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'field':
				try:
					msg = {
						'status': 'ok',
						'item': UC.collect(packet['token'])
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  user token harvested item:" + packet['token'])
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'offer':
				try:
					UC.offer(packet['token'], packet['offered_item'], packet['n1'], packet['demanded_item'], packet['n2'])
					msg = {
						'status': 'ok'
					}
					conn.send(json.dumps(msg).encode('utf-8'))
					print("  user token offered an item: " + packet['token'])
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'tradebox':
				try:
					userbox = UC.getuserbox(packet['token'])
					msg = '{"status": "ok", "offers": ' + userbox + '}'
					conn.send(msg.encode('utf-8'))
					print(X.stock)
					print(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'sendfind':
				try:
					box = UC.find(packet['token'], packet['item'])
					msg = '{"status": "ok", "offers": ' + box + '}'
					conn.send(msg.encode('utf-8'))
					print(X.stock)
					print(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'findoffer':  # server-server
				try:
					items = X.findInSelf(id2item(packet['item']))
					msg = '{"status": "ok", "offers": ' + items + '}'
					conn.send(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'sendaccept':  # TODO
				print("nop")
			elif packet['method'] == 'accept':  # server-server
				try:
					if X.acceptInSelf(packet['token']):
						msg = '{"status": "ok"}'
						conn.send(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'fetchitem':
				try:
					if UC.fetch(packet['token'], packet['offer_token']):
						msg = '{"status": "ok"}'
						conn.send(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'canceloffer':
				try:
					if UC.cancelOffer(packet['token'], packet['offer_token']):
						msg = '{"status": "ok"}'
						conn.send(msg.encode('utf-8'))
				except Fail as e:
					conn.send(prepFailJSON(e, lineno()))
			elif packet['method'] == 'killserver':
				if packet['magicString'] == 'q34tAq34tb3qy4IUaXa4t':
					print("Shutting down server...")
					MAIN_LOOP = False
				else:
					print("WARNING: intrusion attempt")
			else:
				print("unknown connection method.")
		# except Exception as ex:
		# 	print("ERROR: unknown exception in handling connection data.")
		# 	print(ex)

	# conn.shutdown('SHUT_RDWR')
	conn.close()
	UC.save()  # save aaaall the time. really safe for times when server suddenly crash for no reason whatsoever.

# Cleanup =============================================================================
UC.shutdown()
UC.save()