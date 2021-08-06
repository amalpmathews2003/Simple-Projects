from tkinter import *
import time
def first():
	return [
	  [7,8,0,4,0,0,1,2,0],
	  [6,0,0,0,7,5,0,0,9],
	  [0,0,0,6,0,1,0,7,8],
	  [0,0,7,0,4,0,2,6,0],
	  [0,0,1,0,5,0,9,3,0],
	  [9,0,4,0,6,0,0,0,5],
	  [0,7,0,3,0,0,0,1,2],
	  [1,2,0,0,0,7,4,0,0],
	  [0,4,9,2,0,6,0,0,7]
	  ]
global board
board=first()
sample=first()
given_pos=[]

def gui():
	root=Tk()
	root.geometry('720x720')
	root.title('Sudoku Solver')
	root.iconbitmap('photos/sudoku.ico')
	photo=PhotoImage(file='photos/download.png')
	Label(image=photo).pack()
	#Label(root,text="Sudoku Solver",font=30).pack(padx=30,pady=30)
	global frm
	frm=Frame(root,width=400,height=400,bg="yellow")
	frm.pack()
	entries=[]
	for i in range(9):
		for j in range(9):
			e=Text(frm,width=4,height=2,font=("Helvetica", "16"))
			e.insert(END,"\n  ")
			e.grid(row=i+1,column=j+1,padx=2,pady=2)
			e.bind("<Tab>",focus_next)
			e.bind("<Shift-Tab>",focus_previous)
			e.bind("<Left>",focus_previous)
			e.bind("<Right>",focus_next)
			
			entries.append(e)
	entries[0].focus()

	Button(root,text="Solve",command=lambda:input_output(entries)).pack(side=BOTTOM)
	Button(root,text="Sample",command=lambda:input_sample(entries)).pack(side=BOTTOM,anchor=W)
	Button(root,text="Refresh",command=lambda:refresh(entries)).pack(side=BOTTOM,anchor=E)
	root.mainloop()

def refresh(entries):
	board=first
	sample=first
	for i in entries:
		i.delete("1.0",END)
		i.insert(END,"\n  ")
		i.configure(fg="black")



def focus_next(event):
	event.widget.tk_focusNext().focus()
	return ("break")

def focus_previous(event):
	event.widget.tk_focusPrev().focus()
	return ("break")

def input_sample(entries):
	k=0
	for i in range(9):
		for j in range(9):
			entries[k].delete("1.0",END)
			entries[k].insert(END,"\n  ")
			if(sample[i][j]!=0):
				entries[k].insert(END,sample[i][j])
			k+=1

def input_output(entries):
	global board,given_pos
	k=0
	for i in range(9):
		for j in range(9):
			try:
				board[i][j]=int(entries[k].get("1.0",END))
			except ValueError:
				board[i][j]=0

			if board[i][j]!=0:
				given_pos.append((i,j))
			entries[k].delete("1.0",END)
			k+=1
	solve()
	k=0
	for i in range(9):
		for j in range(9):
			entries[k].insert(END,"\n  ")
			if (i,j) in given_pos:
				entries[k].configure(fg="red")
			entries[k].insert(END,board[i][j])
			k+=1
	given_pos=[]
	board=first()
	sample=first()
	return

def print_board():
	for row in board:
		for ele in row:
			print(ele,end=" ")
		print()
def find_empty():
	for i in range(len(board)):
		for j in range(len(board[0])):
			if board[i][j] ==0:
				return (i,j) #row,col


def is_valid(num,pos):
	#check column
	for i in range(len(board[0])):
		if(board[pos[0]][i] == num and pos[1]!=i):
			return False

	#check row
	for i in range(len(board)):
		if board[i][pos[1]]==num and pos[0]!=i:
			return False
	
	#check box
	box_x =pos[1]//3
	box_y=pos[0]//3

	for i in range(box_y*3,box_y*3+3):
		for j in range(box_x*3,box_x*3+3):
			if board[i][j]==num and (i,j)!=pos:
				return False

	return True


def solve():
	find=find_empty()

	if not find:
		return True 
	else:
		row,col=find

		for i in range(1,10):
			if is_valid(i,(row,col)):
				board[row][col]=i

				if solve():
					return True
				else:
					board[row][col]=0
	return False
#def key_press(event):
#	print(event)


gui()

#print_board(board)
#solve(board)
#print()
#print_board(board)

#print(help(Tk.tk_focusNext))
