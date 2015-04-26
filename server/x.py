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

# Classes ==========================================================================
class Inventory:
	id2item = {
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

	item2id = {
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
		return self.item2id[name]

	def mix(self, name1, name2):
		name1 = self.id2item[name1]
		name2 = self.id2item[name2]
		if name1[1] is name2[1]:
			if int(name1[2]) is int(name2[2])+1 or int(name1[2])+1 is int(name2[2]):
				if self.item[name1] >= 3 and self.item[name2] >= 3:
					self.item[name1] -= 3
					self.item[name2] -= 3
					resultantTier = int(name1[1]) + 1
					if int(name1[2] < name2[2]):
						self.item['R'+str(resultantTier)+name1[2]] += 1
						return self.item2id['R'+str(resultantTier)+name1[2]]
					else:
						self.item['R'+str(resultantTier)+name2[2]] += 1
						return self.item2id['R'+str(resultantTier)+name2[2]]
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

	def move(self, newLoc):
		if int(self.newLocation[0]) is int(self.location[0])+1 or int(self.newLocation[0]) is int(self.location[0])-1:
			if int(self.newLocation[1]) is int(self.location[1])+1 or int(self.newLocation[1]) is int(self.location[1])-1:
				self.newLocation = newLoc
				self.moveTime = random.randint(60,120)   # TODO: time, and what happens when time reaches zero? threads?
				return self.moveTime
			else:
				raise Fail("move location is too far")
		else:
			raise Fail("move location is too far")


class UserContainer:
	user = []

	#def __init__(self):
		#with open("users.json", 'r') as f:
			#self.user = json.load(f)

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
		with open("users.json", "w") as f:
			json.dump(self.user, f, default=lambda o: o.__dict__, indent=4)
			print(json.dump(self.user, f, default=lambda o: o.__dict__, indent=4))
			# i have NO IDEA how that ^ works, but whatever -_- just works.
			# indent optional.
		print("saved")

	def mix(self, token, name1, name2):
		for usr in self.user:
			if usr.token is token:
				return usr.inv.mix(name1, name2)
		raise Fail("User not found")

	def inv(self, token):
		for usr in self.user:
			if usr.token is token:
				return usr.getInventory()
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

class Map:
	def __init__(self):
		with open(sys.argv[2]) as f:
			mapdata = json.load(f)
		self.name = mapdata['name']
		self.width = mapdata['width']
		self.height = mapdata['height']
		self.items = mapdata['map']


# Exceptions =======================================================================
class Fail(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)


# Prep =============================================================================
UC = UserContainer()

UC.signup("dalva","passtemp")
UC.save()