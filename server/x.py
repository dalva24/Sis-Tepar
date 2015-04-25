# Imports ==========================================================================
import socket
import json
import sys
import os
import hashlib
import datetime
import random


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
		with open("users.json", 'r') as f:
			self.user = json.load(f)

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

	def save(self):
		with open("users.json", "w") as f:
			json.dump(self.user, f, default=lambda o: o.__dict__, indent=4)

uc = UserContainer()
#uc.add(User("dalva","pass"))
#uc.add(User("taiga","pass2"))
print(uc.user)
uc.save()