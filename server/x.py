class A:
	def __init__(self):
		self.x = 1

	def geet(self):
		retval = self.x
		return self.x


test = A()
val = test.geet()
val += 1
print (val)
print (test.x)