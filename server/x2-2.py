# from x3 import UserContainer
import pickle

class Test:
	testmeh = []

class BTest:
	def __init__(self, x, y):
		self.datax = x
		self.datay = y

file = open("yapokoknyagitu.obj",'rb')
object_file = pickle.load(file)

a = object_file.testmeh[0].datax
b = object_file.testmeh[1].datax
c = object_file.testmeh[0].datay
d = object_file.testmeh[1].datay

print(a,b,c,d)

# file = open("savefile.obj",'rb')
# object_file = pickle.load(file)

# print(object_file[0].pw)