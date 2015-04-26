import pickle

class Test:
	testmeh = []

class BTest:
	def __init__(self, x, y):
		self.datax = x
		self.datay = y
	
tet = Test()
bte = BTest('ma',1234)
bte2 = BTest('me',4321)

tet.testmeh.append(bte)
tet.testmeh.append(bte2)

filehandler = open(b"yapokoknyagitu.obj","wb")
pickle.dump(tet, filehandler)

filehandler.close()

file = open("yapokoknyagitu.obj",'rb')
object_file = pickle.load(file)

a = object_file.testmeh[0].datax
b = object_file.testmeh[1].datax
c = object_file.testmeh[0].datay
d = object_file.testmeh[1].datay

print(a,b,c,d)

# print(tet.testmeh[0])

# file = open("my_pat.obj",'rb')
# object_file = pickle.load(file)

# print(object.testmeh[0])

# my_pat = pickle.load(file('my_pat.pickle'))
# print(object_file.data)
 
# my_puis = pickle.load(file('my_puis.pickle'))
# print my_puis.data