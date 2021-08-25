from sympy import *
from tkinter import *
from tkinter import scrolledtext as st
import math
class Calculator():
	def __init__(self):
		root=Tk()
		root.geometry('350x500')
		root.title('Calculator')
		self.counter=1
		self.degree=True
		self.body(root)
		root.mainloop()
		
	def body(self,root):
		calc=Frame(root,width=350,height=500)
		calc.pack()
		self.e=st.ScrolledText(calc,width=30,height=4,font=10)
		self.e.place(x=10,y=10)

		def insert(x):
			self.e.insert(END,x)
		def degree_to_rad(x,b1,b2):
			self.degree=x
			print(self.degree)
			b1.configure(state=DISABLED)
			b2.configure(state=NORMAL)

		Button(calc,text="1",command=lambda:insert(1),height=2,width=4).place(x=50,y=120)
		Button(calc,text="2",command=lambda:insert(2),height=2,width=4).place(x=110,y=120)
		Button(calc,text="3",command=lambda:insert(3),height=2,width=4).place(x=170,y=120)
		Button(calc,text="4",command=lambda:insert(4),height=2,width=4).place(x=50,y=180)
		Button(calc,text="5",command=lambda:insert(5),height=2,width=4).place(x=110,y=180)
		Button(calc,text="6",command=lambda:insert(6),height=2,width=4).place(x=170,y=180)
		Button(calc,text="7",command=lambda:insert(7),height=2,width=4).place(x=50,y=240)
		Button(calc,text="8",command=lambda:insert(8),height=2,width=4).place(x=110,y=240)
		Button(calc,text="9",command=lambda:insert(9),height=2,width=4).place(x=170,y=240)
		Button(calc,text=".",command=lambda:insert("."),height=2,width=4).place(x=50,y=300)
		Button(calc,text="0",command=lambda:insert(0),height=2,width=4).place(x=110,y=300)
		Button(calc,text=",",command=lambda:insert(","),height=2,width=4).place(x=170,y=300)
		Button(calc,text="+",command=lambda:insert("+"),height=2,width=4).place(x=230,y=120)
		Button(calc,text="-",command=lambda:insert("-"),height=2,width=4).place(x=230,y=180)
		Button(calc,text="*",command=lambda:insert("*"),height=2,width=4).place(x=230,y=240)
		Button(calc,text="/",command=lambda:insert("/"),height=2,width=4).place(x=230,y=300)
		Button(calc,text="=",command=self.calculate,height=2,width=4).place(x=230,y=360)
		
		Button(calc,text="(",command=lambda:insert("("),height=2,width=4).place(x=50,y=360)
		Button(calc,text=")",command=lambda:insert(")"),height=2,width=4).place(x=110,y=360)


		Button(calc,text="sin",command=lambda:insert("sin("),height=2,width=4).place(x=50,y=440)
		Button(calc,text="cos",command=lambda:insert("cos("),height=2,width=4).place(x=110,y=440)
		Button(calc,text="tan",command=lambda:insert("tan("),height=2,width=4).place(x=170,y=440)
	
		b1=Button(calc,text="D",height=2,width=4,state=DISABLED)
		#b1.place(x=0,y=120)
		b2=Button(calc,text="R",height=2,width=4)
		#b2.place(x=0,y=180)
		b1.configure(command=lambda:degree_to_rad(True,b1,b2))
		b2.configure(command=lambda:degree_to_rad(False,b2,b1))


	def calculate(self):
		expr=self.e.get(f"{self.counter}.0",END)
		if expr:
			expr=self.convert(expr)
			ans=eval(expr)
			self.e.insert(END,f"\n{ans}\n")
			self.counter+=2
	def convert(self,expr):
		s=["sin","cos","tan"]
		for i in s:
			expr=expr.replace(i,f"math.{i}")
		print(expr)
		return expr



Calculator()
