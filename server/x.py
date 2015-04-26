class XItem:
	def __init__(self, iSell, iBuy):
		self.iBuy = iBuy
		self.iSell = iSell


class XHandler:
	def __init__(self):
		self.item = [XItem(5,1),XItem(5,2)]

	def format(self):
		for itm in self.item:
			print(itm.iBuy)


x = XHandler()
x.format()


