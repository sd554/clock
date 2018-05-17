# Time Clock Version 3.0.0
# Written By Dylan Smith
# Managed By FRC Team 1540 The Flaming Chickens
# Last Updated January 23, 2018

from graphics import *
import os


# graphics is a graphics library
# oauth2client, gspread, and httplib2 are for uploading to the spreadsheet
# os is used for os.system, which runs shell script
# json is for reading and editing .json files
# time gets the time and date
# theading is for creating multiple threads
# urllib2 is for checking wifi
# smtplib is for sending emails

# user can change the width and height variable to whatever fits the screen best
width=1330 #window width
height=800 #window height
makeGraphicsWindow(width,height)
setWindowTitle("Time Clock")

# button class
class Button:
    def __init__(self,x,y,w,h,color,text,where,action,rounded=False,cap=1000):
        # x-position, in percentage of screen-width
        self.x=x
        # y-position, in percentage of screen-height
        self.y=y
        # width, in percentage of screen-width
        self.w=w
        # height, in percentage of screen-height
        self.h=h
        # button color
        self.color=color
        # displayed text
        self.text=text
        # what page the button is viewed on
        self.where=where
        # what happens when button is pressed
        self.action=action
        # are the edges of the button rounded (or square)
        self.rounded=rounded
        # the maximum font size
        # for the cases where you want the text to not touch the edge of the button
        self.cap=cap


################################################################
###################### Utility Functions #######################
################################################################

# text to speech
def say(string):
    if os.name=="posix": # macintosh
        os.system("say '"+string+"' -vSamantha")
    elif os.name=="nt": # windows
        # creates a file to read from, reads from it, then deletes the file
        open("tts.txt","w").write(string)
        os.system('cscript "C:\Program Files\Jampal\ptts.vbs" < tts.txt -voice "Microsoft Hazel Desktop"')
        os.remove("tts.txt")

# function that detects if point is inside of a box
def inbox(boxx,boxy,pointx,pointy,boxwidth=50,boxheight=50):
    if pointx>=boxx and pointx<=boxx+boxwidth:
        if pointy>=boxy and pointy<=boxy+boxheight:
            return True
        else:
            return False
    else:
        return False

# brings user back to home page
def reset():
    w=getWorld()
    if not w.name=="":
        w.msg = w.name + " clocked " + w.io
    w.name=""
    w.page="home"
    w.id=""
    w.io=None


################################################################
########################## Mouse Press #########################
################################################################

# x is x-position of mouse
# y is y-position of mouse
# b is the button pressed on the mouse (left-click is 1)
def mousePress(w,x,y,b):
    for u in w.buttons:
        # checks to see if user clicked on the button
        if b==1 and w.page==u.where and inbox(u.x*width,u.y*height,x,y,u.w*width,u.h*height):
            return u.action(u)

onMousePress(mousePress)

################################################################
######################## Button Actions ########################
################################################################

# all of the following functions take b, the button, as an argument for consistency
# these are run when buttons are pressed

#sends user to login screen
def IN(b):
    getWorld().page="login/logout"
    getWorld().io="in"

#sends user to logout screen
def OUT(b):
    getWorld().page="login/logout"
    getWorld().io="out"

#adds the button's display to the id
def KEY(b):
    if len(getWorld().id)<4:
        getWorld().id+=b.text

#backspace key
def DELETE(b):
    if len(getWorld().id)>0:
        getWorld().id=getWorld().id[:-1]

#return to home page
def PASS(b):
    reset()

#checks to see if ID is an actual ID. if so, signs you in/out
def OK(b):
    w=getWorld()
    reset()

################################################################
################################################################
################################################################

# the start function runs when app is opened
def start(w):
    # what page you are on
    w.page = "home"
    # whether or not you are logging in or out
    # when in, w.io="in"
    # when out, w.io="out"
    w.io = None
    # the id presently being type
    w.id = ""
    # list of all IDs in same order as spreadsheet
    w.ids = []

    w.msg = ""
    w.name = ""

    w.buttons = [
    Button(0.07,0.3,0.4,0.4,(3,155,229),"Log In","home",IN,cap=75),
    Button(0.53,0.3,0.4,0.4,(255,171,64),"Log Out","home",OUT,cap=75),
    Button(0.24,0.19,0.15,0.15,(208,211,216),"1","login/logout",KEY,cap=50),
    Button(0.42,0.19,0.15,0.15,(208,211,216),"2","login/logout",KEY,cap=50),
    Button(0.60,0.19,0.15,0.15,(208,211,216),"3","login/logout",KEY,cap=50),
    Button(0.24,0.39,0.15,0.15,(208,211,216),"4","login/logout",KEY,cap=50),
    Button(0.42,0.39,0.15,0.15,(208,211,216),"5","login/logout",KEY,cap=50),
    Button(0.60,0.39,0.15,0.15,(208,211,216),"6","login/logout",KEY,cap=50),
    Button(0.24,0.59,0.15,0.15,(208,211,216),"7","login/logout",KEY,cap=50),
    Button(0.42,0.59,0.15,0.15,(208,211,216),"8","login/logout",KEY,cap=50),
    Button(0.60,0.59,0.15,0.15,(208,211,216),"9","login/logout",KEY,cap=50),
    Button(0.24,0.79,0.15,0.15,(98,178,85),"OK","login/logout",OK,cap=50),
    Button(0.42,0.79,0.15,0.15,(208,211,216),"0","login/logout",KEY,cap=50),
    Button(0.60,0.79,0.15,0.15,(237,99,92),"Del","login/logout",DELETE,cap=50),
    Button(0.8,0.05,0.15,0.15,(3,155,229),"Cancel","login/logout",PASS,cap=30)
    ]
    setDefaultFont("norwester")

def update(w):
    pass

# draw function for button
def button(x,y,w,h,color,text,rounded,cap):
    # draws a curved button by drawing to rectangles in a lowercase t shape
    # and then proceeds to draw arcs to fill up each corner
    if rounded:
        # center / t-shape
        fillRectangle(x*width+30,y*height,w*width-60,h*height,color=color)
        fillRectangle(x*width,y*height+30,w*width,h*height-60,color=color)
        # top-left
        fillCircle(30+x*width,30+y*height,30,color=color)
#        drawArcCircle(30+x*width,30+y*height,30,90,180)
        # top-right
        fillCircle((x+w)*width-30,30+y*height,30,color=color)
#        drawArcCircle((x+w)*width-30,30+y*height,30,0,90)
        # bottom-left
        fillCircle(30+x*width,30+(y+h)*height-60,30,color=color)
#        drawArcCircle(30+x*width,30+(y+h)*height-60,30,180,270)
        # bottom-right
        fillCircle((x+w)*width-30,30+(y+h)*height-60,30,color=color)
#        drawArcCircle((x+w)*width-30,30+(y+h)*height-60,30,270,360)
        # vertical-lines
#        drawLine(x*width,y*height+30,x*width,(y+h)*height-30)
#        drawLine((x+w)*width,y*height+30,(x+w)*width,(y+h)*height-30)
        # horizontal-lines
#        drawLine(x*width+30,y*height,(x+w)*width-30,y*height)
#        drawLine(x*width+30,(y+h)*height,(x+w)*width-30,(y+h)*height)
    else:
        # draws a rectangular button
        fillRectangle(x*width,y*height,w*width,h*height,color=color)
#        drawRectangle(x*width,y*height,w*width,h*height)
    if not text=="":
        # size represents the size that each character of the string is
        size = 1
        # currentStringSize is a tuple (width of string,height of string)
        currentStringSize = sizeString(text,size=size)
        # the following loop attempts to find a size for the text that will not exceed the size of the button
        while ((w*width)-currentStringSize[0]>20) and ((h*height)-currentStringSize[1]>20):
            currentStringSize = sizeString(text,size=size)
            # checks to see if font-size has reached the font-cap yet
            if size>=cap:
                break
            size+=1
        xpos = (x*width) + ((w*width)/2) - (currentStringSize[0]/2)
        ypos = (y*height) + ((h*height)/2) - (currentStringSize[1]/2)
        drawString(text,xpos,ypos,size=size,color="white")

# drawing all text/buttons
# this function clears the display before running
def draw(w):
    # draws each button
    for b in w.buttons:
        if b.where==w.page:
            text = b.text
            if b.text=="OK": # for the clarity of the login/logout screens
                text=w.io.capitalize()
            button(b.x,b.y,b.w,b.h,b.color,text,b.rounded,b.cap)
    # for the display on the login/logout page
    if w.page=="login/logout":
        s = sizeString(w.id,90)
        drawString(w.id,width/2-s[0]/2.0,height*.01,size=90)
    elif w.page=="home":
        s = sizeString(w.msg,30)
        drawString(w.msg,width/2-s[0]/2.0,height*.01,size=30)

# runs the start, update, and draw function
runGraphics(start,update,draw)
