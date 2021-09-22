from tkinter import *
import requests
from bs4 import BeautifulSoup

class CurrencyConverter:
	def __init__(self):
		self.gui()

	def gui(self):
		root=Tk()
		root.title('Currency Converter')
		root.geometry('300x300')
		h=Label(root,text="Realtime Currency Converter")
		h.grid(row=0,column=0)
		l1=Label(root,text="Amount")
		l1.grid(row=1,column=0)
		self.amount=Entry(root)
		self.amount.grid(row=1,column=1)
		currencys=["INR","USD","EUR","GBP","AUD","CAD","SGD","CHF","SGD","CHF","MYR",
					"JPY","CNY","NSD"]
		self.from_amount=StringVar(root)
		self.to_amount=StringVar(root)
		self.from_amount.set('INR')
		self.to_amount.set("USD")
		Label(root,text="From").grid(row=3,column=0)
		fro=OptionMenu(root,self.from_amount,*currencys)
		fro.grid(row=3,column=1)
		Label(root,text="To").grid(row=4,column=0)
		to=OptionMenu(root,self.to_amount,*currencys)
		to.grid(row=4,column=1)
		b=Button(root,text="Convert",command=self.convert_amount)
		b.grid(row=5,column=1)
		self.result=Entry(root)
		self.result.grid(row=5,column=0)
		cl=Button(root,text="Clear",command=self.clear_all)
		cl.grid(row=7,column=0)
		root.mainloop()
	def clear_all(self,amount,result):
		self.amount.delete(0,END)
		self.result.delete(0,END)
	def convert_amount(self):
		amount=self.amount.get()
		if amount and amount.isnumeric():
			from_=self.from_amount.get()
			to_=self.to_amount.get()
			url=f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={from_}&To={to_}"
			r=requests.get(url)
			soup=BeautifulSoup(r.content,'html5lib')
			ans=soup.find("p",{"class":"result__BigRate-sc-1bsijpp-1 iGrAod"}).text
			ans=ans.split(' ')[0]
			self.result.delete(0,END)
			self.result.insert(0,ans)
		else:
			self.result.delete(0,END)
			self.result.insert(0,0)
CurrencyConverter()
