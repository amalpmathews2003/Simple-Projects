#created bu Amal P Mathews
import turtle 
import random #to create random numbers
import time
class snake_game():
	score=0
	high_score=0
	delay=0.1
	def screen(self):
		'''
			Setting Up Window
			width=600
			height=600
			background colour=black
			no update shown in screen
		'''
		self.wn=turtle.Screen()
		self.wn.title("Snake Game by Amal")
		self.wn.bgcolor('black')
		self.wn.setup(width=600,height=600)
		self.wn.tracer(0) #turns off window updates ,window will update if we call
		return
	def snake_head(self):
		#snake head
		self.head=turtle.Turtle()
		self.head.speed(0)#to attain full speed
		self.head.shape("square")
		self.head.color('green')
		self.head.penup()
		self.head.goto(0,0)#start from center
		self.head.direction="stop"#dont move until we wants to move

		self.segments=[] #to increase size of snake
		return
	def food(self):
		#snake self.food
		self.food=turtle.Turtle()
		self.food.speed(0)#to attain full speed
		self.food.shape("circle")
		self.food.color('red')
		self.food.penup()# to not to show moment of food
		self.move_food()
		return
	def controls(self):
		'''
			keyboard bindings
			assigning aarow keys their functionalitis
			we can include (w,a,s,d) also like this
		'''
		self.wn.listen()
		self.wn.onkeypress(self.go_up,"Up") 
		self.wn.onkeypress(self.go_down,"Down")
		self.wn.onkeypress(self.go_right,"Right")
		self.wn.onkeypress(self.go_left,"Left")
		return
	def go_up(self):
		if self.head.direction!="down":
			self.head.direction="up"
		return
	def go_down(self):
		if self.head.direction!="up":
			self.head.direction="down"
		return
	def go_left(self):
		if self.head.direction!="right":
			self.head.direction="left"
		return
	def go_right(self):
		if self.head.direction!="left":
			self.head.direction="right"
		return
	def display_score(self):
		self.score_display=turtle.Turtle()
		self.score_display.speed(0)
		self.score_display.shape("square")
		self.score_display.color("white")
		self.score_display.penup()
		self.score_display.hideturtle()
		self.score_display.goto(0,260)
		self.score_display.write("Score: 0  High Score : 0 ",align="center",font=("courier",24,"normal"))
		return
	def game_over(self):
		self.segments.clear()
		delay=0.1
		t=turtle.Turtle()
		t.penup()
		t.hideturtle()
		t.color("red")
		self.wn.bgcolor("black")
		t.write("Game Over",move=True,align="center",font=("manjari",80,"bold"))
		time.sleep(0.5)
		self.wn.bye()
		return
	def move_food(self):
		'''
			since width of our screen is 600 making cordinate axis
			max(x)=300 and min(x)=-300
			for the food to be in the scrren we want x cordinate of the 
			food to be less than 300 and greater than -300 
			( i put 290 to not to got food parts out of screen ,similarly for y coordinate)
		'''
		#move the food random spot
		x=random.randint(-290,290)
		y=random.randint(-290,290)
		self.food.goto(x,y)
		return
	def is_food_eaten(self):
		#20 is the size of a turtle
		return self.head.distance(self.food)<20
	def add_segment(self):
		'''
			to increase snake size by adding to turlte to list segment
		'''
		new_segment=turtle.Turtle()
		new_segment.speed(0)
		new_segment.shape("square")
		new_segment.color("grey")
		new_segment.penup()
		self.segments.append(new_segment)
		self.delay-=0.001#increasing the speed
		return
	def move_segments(self):
		''' 
			to move snake segments along with head'
		'''
		#move the end segments first n reverse
		for index in range(len(self.segments)-1,0,-1):
			x=self.segments[index-1].xcor()
			y=self.segments[index-1].ycor()
			self.segments[index].goto(x,y)

		#move segment[0]
		if len(self.segments)>0:
			x=self.head.xcor()
			y=self.head.ycor()	
			self.segments[0].goto(x,y)
		return
	def is_colliding_with_border(self):
		#check for collision with border
		if(self.head.xcor()>300 or self.head.xcor()<-300 or self.head.ycor()<-300 or self.head.ycor()>300 ):
			time.sleep(0.6)
			self.score=0
			self.game_over()	
		return
	def is_colliding_with_body(self):
		#check for head collisions with body
		for i in range(len(self.segments)-1):
			if self.segments[i+1].distance(self.head)<10 : 
				self.score=0
				time.sleep(0.5)
				self.game_over()
		return
	def move_head(self):
		if self.is_colliding_with_border():
			return
		if self.head.direction=="up":
			y=self.head.ycor()
			self.head.sety(y+20)
	
		if self.head.direction=="down":
			y=self.head.ycor()
			self.head.sety(y-20)
		

		if self.head.direction=="left":
			x=self.head.xcor()
			self.head.setx(x-20)

		if self.head.direction=="right":
			x=self.head.xcor()
			self.head.setx(x+20)
		return
	def main_game(self):
		self.screen()#making screen
		self.snake_head() #making snake head
		self.food()#making foog
		self.controls()#key bindings
		self.display_score()#display score
		#infinite loop 
		while True:
			self.wn.update()#update screen
			if self.is_colliding_with_border():
				return
			if self.is_food_eaten():
				self.add_segment()
				self.move_food()
				self.score+=10
				if self.score>self.high_score:
					self.high_score=self.score
				self.score_display.clear()
				self.score_display.write("Score: {}  High Score : {} ".format(self.score,self.high_score),align="center",font=("courier",24,"normal"))
			self.move_segments()
			self.move_head()
			if self.is_colliding_with_body():
				return
			time.sleep(self.delay)



s=snake_game()
s.main_game()
