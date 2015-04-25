import datetime
import hashlib

tel = {'R11': 1, 'R12': 2, 'R13': 3}
print (list(tel.values()))
a = datetime.datetime.now()
b = "a"
print (hashlib.md5(b.encode()+str(a).encode()).hexdigest())