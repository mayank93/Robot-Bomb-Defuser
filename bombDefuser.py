import random
import curses
from curses import initscr,curs_set,newwin,endwin,KEY_RIGHT,KEY_LEFT,KEY_UP,KEY_DOWN,beep,start_color,noecho;
from random import randrange;
scr=initscr()
noecho()
start_color()
#N=30 # heigt of field
#M=60 # width of field
N=scr.getmaxyx()[0]  # heigt of field
M=scr.getmaxyx()[1]  # width of field
count=0 # codes collected initally
d=4 # no. of codes initally
b=1 # no. of bomb initally
s=10 # score added when bomb is diffused
score=0 # inital score
level=0	# initalising level
flag=0
Life=3 # no. of chances 
e=0 # no. of enemies
L=5# no. of levels +1
sc=1 # score added when a code is collected
bomb=0 # no. of bomb diffused
space=5 # border width from edges in which the bomb and codes should not be placed
defaultkey=KEY_RIGHT # direction in which robo move initally
x=5
y=3
#-------------------------------------------------------------------------------------------------------------------------------------
#different robo bomb desis designs , same for codes 
import design
#-------------------------------------------------------------------------------------
class Keys:
	quit=[27,ord('q'),ord('Q')]
	up=[ord('w'),ord('W'),KEY_UP]
	down=[ord('s'),ord('S'),KEY_DOWN]
	left=[ord('a'),ord('A'),KEY_LEFT]
	right=[ord('d'),ord('D'),KEY_RIGHT]
	pause=[ord('p'),ord('P')]
	allkey=quit+up+down+right+left+pause
	choice=[ord('0'),ord('1'),ord('2'),ord('3'),ord('4'),ord('5'),ord('6'),ord('7'),ord('8'),ord('9')]
#-----------------------------------------------------------------------------------------
class Screen:
	def __init__(self):
		curs_set(0);
		self.height=N
		self.width=M
		self.win=newwin(N,M,0,0)
		self.win.border('|','|','~','~','+','+','+','+');
		self.win.keypad(1)
	def end(self):
		endwin()
	def clear(self):
		screen.win.clear()
		self.win.border('|','|','~','~','+','+','+','+');
	def window(self):
		return self.win
#-------------------------------------------------------------------------------------------------------------------------------------
screen=Screen()
#-------------------------------------------------------------------------------------------------------------------------------------
class Enemy:
	def __init__(self,choice,fieldpos,robopos):
		self.shape=design.roboshape(choice)
		self.pos=[]
		self.places=reduce(lambda x,y:x+y,robopos,[])
		self.fieldpos=reduce(lambda x,y:x+y,fieldpos,[])
		self.places.extend(self.fieldpos)
		self.enemycount=e
		self.enemypos=[]
		self.height=N
		self.width=M
		self.choice=choice
		self.check=[]
	def Enemyposdecider(self):
		self.enemypos=[]
		while (len(self.enemypos)!=self.enemycount):
			plac=[random.randrange(space,self.width-space),random.randrange(space,self.height-space)]
			if plac not in self.places and plac not in self.enemypos:
				if plac:
					self.enemypos.append(plac)
	def Enemtinit(self):
		ecount=0
		while (ecount!=self.enemycount):
			self.pos.append(design.roboposition(self.choice,x,y))
			ecount+=1
	def checkexistence(self,ecount):
			check1=reduce(lambda x,y:x+y,self.pos[ecount],[])
			check2=map(lambda xx:filter(lambda yy: xx==yy,check1),self.fieldpos)
			self.check=reduce(lambda x,y:x+y,check2,[])
	def move(self):
		ecount=0
		i=1
		while (ecount!=self.enemycount):
			plac=self.enemypos[ecount]
			self.enemypos[ecount]=[(plac[0]+2*i)%(M-space),(plac[1])%(N-space)]
			plac=self.enemypos[ecount]
			if plac not in self.fieldpos and plac[0]>=space and plac[1]>=space:
				self.checkexistence(ecount)
				if len(self.check)==0:
					map(lambda xx:map(lambda y:screen.win.addch(self.pos[ecount][xx][y][1],self.pos[ecount][xx][y][0],' '),range(0,len(self.pos[ecount][xx]))),range(0,len(self.pos[ecount])))
				x=plac[0]
				y=plac[1]
				self.pos[ecount]=design.roboposition(self.choice,x,y)
				self.checkexistence(ecount)
				if len(self.check)==0:
					map(lambda xx:map(lambda yy:screen.win.addch(self.pos[ecount][xx][yy][1],self.pos[ecount][xx][yy][0],self.shape[xx][yy],curses.A_BOLD),range(0,len(self.pos[ecount][xx]))),range(0,len(self.pos[ecount])))
			ecount+=1
	def getpos(self):
		return self.pos
	def whatatpos(self):
		return self.wap
#-------------------------------------------------------------------------------------------------------------------------------------
class Robot:
	def __init__(self,choice,i,j):
		self.shape=design.roboshape(choice)
		self.pos=design.roboposition(choice,i,j)
		self.x=i
		self.y=j
		self.choice=choice
		self.wap=[]
	def move(self,i,j):
		map(lambda x:map(lambda y:screen.win.addch(self.pos[x][y][1],self.pos[x][y][0],' '),range(0,len(self.pos[x]))),range(0,len(self.pos)))
		self.x+=i
		self.y+=j
		self.pos=design.roboposition(self.choice,self.x,self.y)
		self.wap=reduce(lambda xx,yy:xx+yy,map(lambda xx:map(lambda yy:screen.win.inch(self.pos[xx][yy][1],self.pos[xx][yy][0]) & 255,range(0,len(self.pos[xx]))),range(0,len(self.pos))),[])
		map(lambda xx:map(lambda yy:screen.win.addch(self.pos[xx][yy][1],self.pos[xx][yy][0],self.shape[xx][yy],curses.A_BOLD),range(0,len(self.pos[xx]))),range(0,len(self.pos)))
	def getpos(self):
		return self.pos
	def whatatpos(self):
		return self.wap
#------------------------------------------------------------------------------------------------------------------------------------
class Intro:
	Key=Keys()
	def __init__(self):
		self.flag=0
		self.choice=0
		self.choice=1
		self.EnemyRobochoice=5
		self.PoliceRobochoice=4
		self.bombchoice=6
		self.codechoice=5
	def firstscreen(self):
		N=scr.getmaxyx()[0]  # heigt of field
		M=scr.getmaxyx()[1]  # width of field
		screen.win.addstr((N/2)-4,M/2,'  1.Start Game  ',curses.A_REVERSE)
		screen.win.addstr((N/2)-2,M/2,'  2.Settings  ',curses.A_REVERSE)
		screen.win.addstr((N/2),M/2,'  3.Instructions  ',curses.A_REVERSE)
		screen.win.addstr((N/2)+2,M/2,'  4.About  ',curses.A_REVERSE)
		screen.win.addstr((N/2)+6,M/2,'  6.Credits  ',curses.A_REVERSE)
		screen.win.addstr((N/2)+4,M/2,'  5.Exit the game  ',curses.A_REVERSE)
		self.choice=screen.win.getch()
		screen.clear()
		if self.choice==ord('1'):
			i=0
#			screen.win.addstr(N/2,M/2,'LOADING PLEASE WAIT.........',curses.A_BOLD)
			load="LOADING PLEASE WAIT........."
			for data in load:
				screen.win.addstr(N/2,M/2+i,data,curses.A_BOLD)
				screen.win.timeout(200)
				screen.win.getch()
				i+=1
			screen.clear()
		elif self.choice==ord('2'):
			screen.clear()
			self.secondscreen()
		elif self.choice==ord('3'):
			File=open("Instruction.txt",'r')
			i=0
			for data in File:
				screen.win.addstr(N/6+i,M/7,data,curses.A_BOLD)
				i+=1
			screen.win.border('|','|','~','~','+','+','+','+');
			
			choice2=screen.win.getch()
			screen.clear()
			self.firstscreen()
		elif self.choice==ord('4'):
			File=open("About.txt",'r')
			i=0
			for data in File:
				screen.win.addstr(N/3+i,6,data,curses.A_BOLD)
				i+=1
			screen.win.border('|','|','~','~','+','+','+','+');
			choice2=screen.win.getch()
			screen.clear()
			self.firstscreen()
		elif self.choice==ord('5'):
			self.flag=1
			screen.clear()
		elif self.choice==ord('6'):
			File=open("Credits.txt",'r')
			i=0
			for data in File:
				screen.win.addstr(N/4+i,M/6,data,curses.A_BOLD)
				i+=1
			screen.win.border('|','|','~','~','+','+','+','+');
			choice2=screen.win.getch()
			screen.clear()
			self.firstscreen()
		else:
			screen.clear()
			self.firstscreen()
	def secondscreen(self):
		N=scr.getmaxyx()[0]  # heigt of field
		M=scr.getmaxyx()[1]  # width of field
		screen.win.addstr((N/2)-4,M/2,'  1.Choose Your robot  ',curses.A_REVERSE)
		screen.win.addstr((N/2)-2,M/2,'  2.Choose Enemy robot  ',curses.A_REVERSE)
		screen.win.addstr((N/2),M/2,'  3.Choose Bomb  ',curses.A_REVERSE)
		screen.win.addstr((N/2)+2,M/2,'  4.Choose Diffudecode  ',curses.A_REVERSE)
		screen.win.addstr((N/2)+4,M/2,'  5.Back  ',curses.A_REVERSE)
		choice1=screen.win.getch()
		screen.clear()
		if choice1==ord('1'):
			self.selectrobo()
			self.PoliceRobochoice=self.choice
			screen.clear()
			self.secondscreen()
		elif choice1==ord('2'):
			self.selectrobo()
			self.EnemyRobotchoice=self.choice
			screen.clear()
			self.secondscreen()
		elif choice1==ord('3'):
			self.selectbomb()
			self.bombchoice=self.choice
			screen.clear()
			self.secondscreen()
		elif choice1==ord('4'):
			self.selectbomb()
			self.codechoice=self.choice
			screen.clear()
			self.secondscreen()
		elif choice1==ord('5'):
			screen.clear()
			self.firstscreen()
		else:
			screen.clear()
			self.secondscreen()
	def selectrobo(self):
			screen.win.addstr(18,4,'  Choose from option  ',curses.A_BOLD)
			xx=0
			yy=0
			for i in range(0,10):
				xx+=8
				if(xx==48):
					xx=8
					yy+=8
				robot=Robot(i,xx,6+yy)
				robot.move(0,0)
				screen.win.addstr(2+yy,xx,str(i),curses.A_BOLD)
			self.choice=screen.win.getch()
			if self.choice in Key.choice:
				self.choice=self.choice-ord('0')
			else:
				screen.clear()
				self.selectrobo()
	def selectbomb(self):
			screen.win.addstr(18,4,'  Choose from option  ',curses.A_BOLD)
			xx=0
			yy=0
			for i in range(0,10):
				xx+=8
				if(xx==48):
					xx=8
					yy+=8
				field=Field([],[],0)
				robot=field.display(i,xx,6+yy)
				screen.win.addstr(2+yy,xx,str(i),curses.A_BOLD)
			self.choice=screen.win.getch()
			if self.choice in Key.choice:
				self.choice=self.choice-ord('0')
			else:
				screen.clear()
				self.selectbomb()
#----------------------------------------------------------------------------------------------------------------------------------
class Field:
	def __init__(self,robopos,fieldpos,count):
		self.fieldpos=[]
		self.fieldpos.extend(fieldpos)
		self.places=reduce(lambda x,y:x+y,robopos,[])
		self.places.extend(fieldpos)
		self.count=count
		self.height=N
		self.width=M
		self.pos=[]
		self.shape=[]
		self.position=[]
		self.check=[]
	def checkexistence(self,ecount):
			check1=reduce(lambda x,y:x+y,self.pos,[])
			check2=map(lambda xx:filter(lambda yy: xx==yy,check1),self.places)
			self.check=reduce(lambda x,y:x+y,check2,[])
	def display(self,choice,x,y):
			self.pos=design.bombposition(choice,x,y)
			self.shape=design.bombshape(choice)
			map(lambda xx:map(lambda yy:screen.win.addch(self.pos[xx][yy][1],self.pos[xx][yy][0],self.shape[xx][yy],curses.A_BOLD),range(0,len(self.pos[xx]))),range(0,len(self.pos)))

	def plant(self,choice):
		temp=[]
		while (len(self.position)!=self.count):
			plac=[random.randrange(space,self.width-space),random.randrange(space,self.height-space)]
			x=plac[0]
			y=plac[1]
			self.pos=design.bombposition(choice,x,y)
			self.shape=design.bombshape(choice)
			self.checkexistence(1)
			tt=reduce(lambda x,y:x+y,self.pos,[])
			if len(self.check)==0:
				if plac:
					self.position.append(self.pos)
					temp.append(tt)
					map(lambda xx:map(lambda yy:screen.win.addch(self.pos[xx][yy][1],self.pos[xx][yy][0],self.shape[xx][yy],curses.A_BOLD),range(0,len(self.pos[xx]))),range(0,len(self.pos)))
		self.fieldpos.extend(temp)
	def getpos(self):
		return self.position
	def getfieldpos(self):
		return self.fieldpos
#-------------------------------------------------------------------------------------------------------------------------------
Key=Keys()
key=defaultkey
intro =Intro()
intro.firstscreen()
robot =Robot(intro.PoliceRobochoice,5,5)
flag=intro.flag
life=Life
N=scr.getmaxyx()[0]  # heigt of field
M=scr.getmaxyx()[1]  # width of field
def checkexistence(b,a):
	check1=reduce(lambda x,y:x+y,a,[])
	check2=map(lambda xx:filter(lambda yy: xx==yy,check1),b)
	return reduce(lambda x,y:x+y,check2,[])
#------------------------------------------------------------------------------------------------------------------------------
if __name__ == "__main__":
	while (level != L and life!=0 and flag!=1):
		flag=0
		aa=[]
		robot.x=5
		robot.y=5
		position=robot.getpos()
		Bomb=Field(position,[],b)
		Bomb.plant(intro.bombchoice)
		fpos=Bomb.getfieldpos()
		Code=Field(position,fpos,d)
		Code.plant(intro.codechoice)
		fieldpos=Code.getfieldpos()
		enemy=Enemy(intro.EnemyRobochoice,fieldpos,position)
		enemy.Enemyposdecider()
		enemy.Enemtinit()
		count=0
		bomb=0
		while key not in Key.quit:
			try:
				screen.win.border('|','|','~','~','+','+','+','+');
				screen.win.addstr(0,2,'CODE COLLECTED:'+str(count)+' REMAINING:'+str(d-count),curses.A_BOLD)
				screen.win.addstr(0,M/2,'SCORE:'+str(score),curses.A_BOLD)
				screen.win.addstr(N-1,M/2,'LEVEL:'+str(level),curses.A_BOLD)
				screen.win.addstr(0,M/2+20,'LIFE:'+str(life),curses.A_BOLD)
				screen.win.addstr(N-1,1,'BOMB:'+str(bomb)+':DIFFUSED REMAINING:'+str(b-bomb),curses.A_BOLD)
				enemy.move()
				screen.win.timeout(180-L*10)
				getkey=screen.win.getch()
				key=key if getkey not in Key.allkey else getkey
				if(key in Key.right or key in Key.left or key in Key.up or key in Key.down):
					i=(key in Key.right and 1 or key in Key.left and -1)
					j= (key in Key.up and -1 or key in Key.down and 1)
					robot.move(i,j)
					aa=robot.whatatpos()
				elif(key in Key.pause):
					screen.win.border('|','|','~','~','+','+','+','+');
					screen.win.addstr(N-1,5,"PRESS 'p' OR 'P' TO RESUME",curses.A_BOLD)
					while 1:
						getkey=screen.win.getch()
						if(getkey in Key.pause):
							key=0
							screen.win.border('|','|','~','~','+','+','+','+');
							break
				enemypos=enemy.getpos()
				enemypos=reduce(lambda x,y:x+y,reduce(lambda x,y:x+y,enemypos,[]),[])
				robopos=robot.getpos()
				robopos=reduce(lambda x,y:x+y,robopos,[])
				collision1=map(lambda xx:filter(lambda yy: xx==yy,robopos),enemypos)
				collision2=filter(lambda xx:xx[0]==0 or xx[0]==M-1 or xx[1]==0 or xx[1]==N-1,robopos)
				collision1=reduce(lambda x,y:x+y,collision1,[])
				collision=collision1+collision2
				if len(collision)!=0:
					flag=2
					break
				for i in range(0,b-bomb):
					if(len(checkexistence(robopos,Bomb.position[i]))!=0):
						bombpos=Bomb.position[i]
						map(lambda xx:map(lambda yy:screen.win.addch(bombpos[xx][yy][1],bombpos[xx][yy][0],' '),range(0,len(bombpos[xx]))),range(0,len(bombpos)))
						Bomb.position.remove(bombpos)
						if count==d:
							score+=s
							bomb+=1
							screen.win.addstr(N-1,1,'BOMB:'+str(bomb)+':DIFFUSED REMAINING:'+str(b-bomb),curses.A_BOLD)
							break
						else:
							screen.win.addstr(N-1,1,'BOMB EXPLODED',curses.A_BOLD)
							beep()
							beep()
							flag=2
							break
				for i in range(0,d-count):
					if(len(checkexistence(robopos,Code.position[i]))!=0):
#						print "dd"
						codepos=Code.position[i]
						map(lambda xx:map(lambda yy:screen.win.addch(codepos[xx][yy][1],codepos[xx][yy][0],' '),range(0,len(codepos[xx]))),range(0,len(codepos)))
						Code.position.remove(codepos)
						count+=1
						score+=sc
						break
				if(bomb==b or flag!=0):
					break
			except curses.error:
				flag=2
				beep()
				break
			except KeyboardInterrupt:
				flag=1
				break
		screen.clear()
		if key in Key.quit:
			beep()
			break
		elif flag==0:
			d+=2
			b+=1
			s+=10
			sc+=1
			e+=1
			level+=1
			if life !=Life:
			  life+=1
		elif flag==2:
		 	life-=1
		key=defaultkey
		N=scr.getmaxyx()[0]  # heigt of field
		M=scr.getmaxyx()[1]  # width of field
	N=scr.getmaxyx()[0]  # heigt of field
	M=scr.getmaxyx()[1]  # width of field
	screen.win.addstr(N/2,M/8,"SCORE : "+ str(score),curses.A_BOLD)
	if(level==L and bomb==b-1):
		screen.win.addstr(N/2,(2*M)/5,"CONGRATULATIONS YOU WON",curses.A_BOLD)
		screen.win.addstr(N/2,(3*M)/4,"LEVEL : "+ str(level-1),curses.A_BOLD)
	else:
		screen.win.addstr(N/2,(2*M)/5,"GAME OVER",curses.A_BOLD)
		screen.win.addstr(N/2,(3*M)/4,"LEVEL : "+ str(level),curses.A_BOLD)
	screen.win.timeout(400)
	screen.win.getch()
	i=1
	for i in range(1,N/2-1):
		for j in range(1,M-1):
			screen.win.timeout(2)
			screen.win.getch()
			screen.win.addstr(i,j,"*",curses.A_BOLD)
			screen.win.addstr(N-1-i,M-1-j,"*",curses.A_BOLD)
	screen.win.timeout(2000)
	screen.win.getch()
#----------------------------------------------------------------------------------------------------------------------------------
	screen.end()
#--------------------------------------------------------------------------------------------------------------------------------
#if(level==L and bomb==b-1):
#	print "YOU WIN"
#	print "LEVEL :" +str(level-1)
#else:
#	print "GAME OVER"
#	print "LEVEL :" +str(level)
#print "SCORE :" +str(score)
#--------------------------------------------------------------------------------------------------------------------------------

