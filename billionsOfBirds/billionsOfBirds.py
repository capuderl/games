#Makes 4 images evenly distributed!
#This time I want to add a button

import matplotlib
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from math import floor, ceil
import random
from os import listdir
import tkinter.messagebox

#Who is playing?
#TODO: get this as user input rather than hardcoding it
#or just accept that I have to change this every time we play...which is actually easy
playerNames = ["Larry", "Kimi", "Brian", "Mom", "Cleo", "Elenor"]

projectPath = "C:/Users/capud/Documents/git/games/billionsOfBirds"

#How many points to play to?  
pointsRemainingInitial = 150
pointsRemaining = pointsRemainingInitial

def prepareImageTk(picLoc, imWidth, imHeight):
    #picLoc = full path to the image
    #resize to imWidth x imHeight while maintaining aspect ratio

    img = Image.open(picLoc)
    imgSizeCurrent = img.size
    #This ratio will keep aspect ratio
    ratioResize = min(imWidth/imgSizeCurrent[0], imHeight/imgSizeCurrent[1])
    newSizeFloat = (ratioResize*imgSizeCurrent[0], ratioResize*imgSizeCurrent[1])
    newSizeInt = (floor(newSizeFloat[0]), floor(newSizeFloat[1]))
    img = img.resize(newSizeInt, Image.Resampling.LANCZOS)

    imgTk = ImageTk.PhotoImage(img)


    return imgTk


labels = []
numBirds = 4

# Create an instance of tkinter window
win = Tk()

# Define the geometry of the window
windowWidth = 1200
windowHeight = 550
win.geometry(str(windowWidth)+"x"+str(windowHeight))
#win.geometry("1600x600")

#I decided to add a background for flavor
otherPath = projectPath + "/suppFiles"
fileLocBackground = otherPath + "/lush-green-forest-neblzag5t76yolal.jpg"
#resizing a little wider to make sure it really fills the space
imageBackground = prepareImageTk(fileLocBackground, windowWidth*1.5, windowHeight*1.5)
#position the background to the upper left corner
lBack = Label(win, image=imageBackground)
lBack.image = imageBackground
lBack.place(x=1, y=1)      
       
       
#How much horizontal buffer should there be between photos
buffer = 60
    
#For 4 photos, there needs to be buffer on each side and between 
widthForPics = windowWidth - (numBirds+1)*buffer
imWidth = floor(widthForPics/numBirds);

#What fraction of the height should image take up?  Let's give it half for now
#In my experimenting, the width was the real limiting factor, so this doesn't really matter
imHeight = floor(windowHeight*2/3);

#Set up the list of bird photos
#photoDir = projectPath + "/birdPhotos"
photoDir = projectPath + "/kimiBirb"
photoList = listdir(photoDir)
photoIndexOptions = list(range(len(photoList)))

#read in the stories
fStories=open(otherPath + "/stories.txt")
stories = fStories.readlines()
storyIndexOptions = list(range(len(stories)))

#read in the stories
fAdj=open(otherPath + "/adj.txt")
adj = fAdj.readlines()
adjIndexOptions = list(range(len(adj)))

######################################## Restting and initilizing images

def resetBirdPics():
    #populate bird pictures
    #loop over the picture in eac location
    
    global photoIndexOptions
    for iPosition in range(numBirds):
    
        #Getting a random photo, but I never want to repeat
        #Select from remaining photoIndexOptions
        idx = random.randint(0, len(photoIndexOptions)-1)
        #iImage is the index into the list of image file paths
        iImage = photoIndexOptions[idx]
        #don't select this one in the future
        photoIndexOptions.remove(iImage)
        
        #If you run out of unique photos, reset it
        if len(photoIndexOptions) == 0:
            photoIndexOptions = list(range(len(photoList)))
            print("You've run out of photos, so I reset them")
        
        imageTrk = prepareImageTk(photoDir + "/" + photoList[iImage], imWidth, imHeight)
        
        if len(labels)<numBirds:
            #This is the first printing
            labels.append(Label(win, image=imageTrk))
        else:
            #remove the old one
            labels[iPosition].destroy()

        #position the photo
        labels[iPosition] = Label(win, image=imageTrk)
        labels[iPosition].image = imageTrk
        xPosition = buffer * (iPosition + 1) + imWidth * iPosition
        labels[iPosition].place(x=xPosition, y=ceil(windowHeight/3))

#Print birds for the first time
resetBirdPics()

######################################## Buttons

#Function for pulling up story from input CSV
def pullUpStory():
    global storyIndexOptions

    #Getting a random photo, but I never want to repeat
    #Select from remaining photoIndexOptions
    idx = random.randint(0, len(storyIndexOptions)-1)
    #iImage is the index into the list of image file paths
    iS = storyIndexOptions[idx]
    #don't select this one in the future
    storyIndexOptions.remove(iS)
    
    #If you run out of unique photos, reset it
    if len(photoIndexOptions) == 0:
        storyIndexOptions = list(range(len(stories)))
        print("You've run out of stories, so I reset them")
    
    #I'm using askokcancel because it doesn't make an annoying beep...I guess that's hard to turn off
    #tkinter.messagebox.showinfo("Story time",  stories[iS])
    tkinter.messagebox.askokcancel(title="Story time", message=stories[iS])
    
#Function for pulling up story from input CSV
def pullUpAdj():
    global adjIndexOptions

    #Getting a random photo, but I never want to repeat
    #Select from remaining photoIndexOptions
    idx = random.randint(0, len(adjIndexOptions)-1)
    #iImage is the index into the list of image file paths
    iS = adjIndexOptions[idx]
    #don't select this one in the future
    adjIndexOptions.remove(iS)
    
    #If you run out of unique photos, reset it
    if len(photoIndexOptions) == 0:
        adjIndexOptions = list(range(len(adj)))
        print("You've run out of adjectives, so I reset them")
    
    #I'm using askokcancel because it doesn't make an annoying beep...I guess that's hard to turn off
    #tkinter.messagebox.showinfo("Story time",  stories[iS])
    tkinter.messagebox.askokcancel(title="This birb is...", message=adj[iS])


#This is an empty virtual 1x1 pixel
#This is added to the botton so that height and width are in pixels
#default is "text units", which I find clunky
pixelVirtual = PhotoImage(width=1, height=1)

#A lot of these ratios I picked for aesthetics
buttonHeightPixels = floor(windowHeight/5.5)
buttonWidthPixels = floor(windowWidth/12)
buttonBuffer = floor(buttonWidthPixels/5)
bottonColor = '#013220'
buttonFontColor = 'white'
B = Button(
    text ="Reset Birds", 
    command = resetBirdPics,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg=bottonColor,
    fg=buttonFontColor)
distanceFromEdge = windowWidth-2*buttonWidthPixels
distanceFromTop = floor(buttonHeightPixels/5)
B.place( x=distanceFromEdge , y=distanceFromTop)

B2 = Button(
    text ="Pull up Adjective", 
    command = pullUpAdj,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg=bottonColor,
    fg=buttonFontColor)
distanceFromEdge = distanceFromEdge - buttonBuffer - buttonWidthPixels
B2.place( x=distanceFromEdge , y=distanceFromTop)

B3 = Button(
    text ="Pull up Story", 
    command = pullUpStory,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg=bottonColor,
    fg=buttonFontColor)
distanceFromEdge = distanceFromEdge - buttonBuffer - buttonWidthPixels
B3.place( x=distanceFromEdge , y=distanceFromTop)

diceOptions = ["Story", "Adjective", "Take a birb home"]
colorDice = ["purple", "blue", "yellow"]
def rollDice():
    iDice = random.randint(0, len(diceOptions)-1)
    diceButton.config(text=diceOptions[iDice])
    diceButton.config(bg=colorDice[iDice])
    #iColor = random.randint(0, len(rainbow)-1)
    #diceButton.config(bg=rainbow[iColor])

diceButton = Button(
    text ="Action:\nRoll Dice", 
    command = rollDice,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg="white")
distanceFromEdge = distanceFromEdge - buttonBuffer - buttonWidthPixels
diceButton.place( x=distanceFromEdge , y=distanceFromTop)

######################################## Scoring

#Initialize scores
score = [0] * len(playerNames)

#Make checkboxes
checkBoxes = []
isChecked = []
rainbow = ["red", "orange", "yellow", "green", "blue", "purple"]
distanceFromTop = 0
distanceFromEdge = buffer #floor(buttonWidthPixels/5)
for iP in range(len(playerNames)):
    #use check boxes
    isChecked.append(IntVar())
    checkBoxes.append(
        Checkbutton(win, 
            text=playerNames[iP], 
            variable= isChecked[iP], #exec("isChecked%s" % playerNames[iP]), 
            onvalue=1, 
            offvalue=0, 
            bg=rainbow[iP%len(rainbow)]))
    #If there are enough players make 2 columns
    if (iP > 0) & (iP%4==0):
        distanceFromTop = 0
        distanceFromEdge = distanceFromEdge + floor(1.33*buffer)
    distanceFromTop = distanceFromTop + 30
    checkBoxes[iP].place( x=distanceFromEdge , y=distanceFromTop)
    
#Tally/display scores
def addScores():
    global pointsRemaining
    for iP in range(len(playerNames)):
        #print(playerNames[iP] + ": " + str(isChecked[iP]) + " ...or " + str(isChecked[iP].get()))
        if isChecked[iP].get(): 
            score[iP] = score[iP] + 1
            isChecked[iP].set(0)
            pointsRemaining = pointsRemaining - 1
    if pointsRemaining <= 0:
        finalScore()
    scoreButton.config(text="Score Points\nRemaining " + str(pointsRemaining))
    
#What to print when the game ends
def finalScore():
    global pointsRemaining
    finalOutput = ""
    for iP in range(len(playerNames)):
        finalOutput = finalOutput + playerNames[iP] + ": " + str(score[iP]) + "\n"
    tkinter.messagebox.askokcancel(title="Final Scores!", message=finalOutput)
    pointsRemaining = pointsRemainingInitial
    #Reset the max in case they want to keep playing...reset the counter though
    #This addScores call is just to reset the "remaining" display.  
    addScores()

scoreButton = Button(
    text ="Score Points\nRemaining " + str(pointsRemaining), 
    command = addScores,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg="white")
distanceFromTop = 30
distanceFromEdge = distanceFromEdge + floor(1.33*buffer)
scoreButton.place( x=distanceFromEdge , y=distanceFromTop)


win.mainloop()

