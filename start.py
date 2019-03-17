import os
import threading
import time
import tkinter.messagebox
from mutagen.mp3 import MP3
from tkinter.filedialog import askdirectory
import pygame
from mutagen.id3 import ID3
from tkinter import *

from random import shuffle

from tkinter import ttk
from ttkthemes import themed_tk as tk

root = Tk()
#root.get_themes()
#root.set_theme("plastix")
root.title("JET MUSIC PLAYER")
root.iconbitmap(r'ms.ico')
root.configure(bg='light blue')


root.minsize(610,500)


backgroundimg = PhotoImage(file="1.png")
#wall = PhotoImage(file="wal1.png")
img1 = PhotoImage(file="pause.png" )
img2 = PhotoImage(file="play.png")
img3 = PhotoImage(file="volumeup.png")
img4 = PhotoImage(file="volumedown.png")
img5 = PhotoImage(file="next.png")
img6 = PhotoImage(file="previous.png")
img7 = PhotoImage(file="mu1.png")


listofsongs = []

list = []

v = StringVar()
songlable = ttk.Label(root,textvariable=v,width=80,font='Times 12 bold')


index = 0

#lenghtlabel = Label(root,text="Total lenght-")
#lenghtlabel.place(x=400,y=300)

#currenttimelabel = Label(root,text="Current lenght-")
#currenttimelabel.place(x=100,y=300)

def setvol(val):
    volume = float(val)/100
    pygame.mixer.music.set_volume(volume)


def nextsong(event):
    global index
    index +=1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()


def prevsong(event):
    global index
    index -=1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

def pause(event):
    pygame.mixer.music.pause()


def play(event):
    pygame.mixer.music.unpause()

def shufflelist(event):
    x= [[i] for i in listofsongs]
    shuffle(x)



def startcount(t):
    global paused
    current_time = 0
    while current_time<=t and pygame.mixer.music.get_busy():
        if paused:
            continue
        else:
            mins,sec=divmod(current_time,60)
            mins=round(mins)
            sec=round(sec)
            timeformat='{:02d}:{:02d}'.format(mins,sec)
            currenttimelable="Current Time"+'-'+timeformat
            time.sleep(1)
            current_time+=1


#def incvol(event):
    #pygame.mixer.music.set_volume( pygame.mixer.music.get_volume()+0.1)


#def decvol(event):
 #   pygame.mixer.music.set_volume( pygame.mixer.music.get_volume()-0.1)


def updatelabel():
    global index
    global songname
    v.set(listofsongs[index])
    #return  songname

#listbox = Listbox(frame, yscrollcommand=scrollbar.set)



def directorychooser():
    directory = askdirectory()
    os.chdir(directory)

    for files in os.listdir(directory):
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)
            audio =ID3(realdir)


            listofsongs.append(files)
            list.append(files)


    pygame.mixer.init()
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()




directorychooser()


def getdetails():
    filedata = os.path.splitext(files)
    print(filedata)

    if filedata[1] == '.mp3':
        aud = MP3(files)
        lenghtlabel = aud.info.length

    else:
        aud= pygame.mixer.Sound()
        lenghtlabel = aud.get_length()

    mins, sec = divmod(lenghtlabel, 60)
    mins = round(mins)
    sec = round(sec)
    timeformat = '{:02d}:{:02d}'.format(mins, sec)
    lenghtlabel = "Total length" + '-' + timeformat
    t1 = threading.Thread(target=startcount, args=(lenghtlabel))
    t1.start()
    startcount(lenghtlabel)

label = ttk.Label(root,text='Jet Music player',font='Times 30 italic bold')
label.pack()
label.configure(background='light blue')

image = Label(root,image=img7)
image.place(x=0,y=380)
image.configure(background='light blue')

frame = Frame(root)
frame.pack()
frame.configure(background='light blue')
scrollbar = Scrollbar(frame)
scrollbar.pack(side = RIGHT, fill=Y)
scrollbar.configure(background='light blue')

listbox =Listbox(frame,width=90,yscrollcommand=scrollbar.set )
listbox.pack()
#listbox.configure(background='light blue')

scrollbar.config(command = listbox.yview)

listofsongs.reverse()

#frame1 = Frame(root)
#draw = Canvas(frame1,height=300,width=300)

#draw.create_image(300,400,anchor=NW,image=backgroundimg)
#draw.image=backgroundimg
#draw.place(x=300,y=400,width=100,height=100)
#frame1.place(x=300,y=400,width=100,height=100)

#draw.create_rectangle(25,25,130,60,fill='blue')


for items in listofsongs:
    listbox.insert(0,items)


listofsongs.reverse()
updatelabel()

middleframe = Frame(root)
middleframe.place(x=10,y=10)
middleframe.configure(background='light blue')

scale =ttk.Scale(root,from_=0,to=100,orient = HORIZONTAL,command=setvol)
scale.set(50)
scale.place(x=250,y=305)

label =ttk.Label(root,image=img3,background='light blue')
label.place(x=355,y=305)

label =ttk.Label(root,image=img4,background='light blue')
label.place(x=220,y=305)

shuff=ttk.Button(root,text='Shuffle')
shuff.place(x=500,y=500)

nextbutton =ttk.Button(root,image=img5)
nextbutton.place(x=340,y=250)

previousButton =ttk.Button(root,image=img6)
previousButton.place(x=220,y=250)

pauseButton = ttk.Button(root,image=img1)
pauseButton.place(x=260,y=250)

playButton = ttk.Button(root,image=img2)
playButton.place(x=300,y=250)

#volumehighButton =Button(root,image=img3)
#volumehighButton.place(x=700,y=250)

#volumelowButton =Button(root,image=img4)
#volumelowButton.place(x=700,y=320)


nextbutton.bind("<Button-1>",nextsong)
previousButton.bind("<Button-1>",prevsong)
pauseButton.bind("<Button-1>",pause)
playButton.bind("<Button-1>",play)
shuff.bind("<Button-1>",shufflelist)
#volumehighButton.bind("<Button-1>",incvol)
#volumelowButton.bind("<Button-1>",decvol)

songlable.place(x=30,y=220)
songlable.configure(background='light blue')

root.mainloop()