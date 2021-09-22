import random

def generate():
	lower="abcdefghijklmnopqrstuvwxyz"
	upper="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
	digits="0123456789"
	symbols="!@#$%^&*()"

	password=""

	len=16

	for i in range(0,len):
		int=random.randint(0,100)
		if int%4==0:
			password=password+random.choice(lower)
		elif int%4==1:
			password=password+random.choice(upper)
		elif int%4==2:
			password=password+random.choice(digits)
		elif int%4==3:
			password=password+random.choice(symbols)

	print(password)

generate()