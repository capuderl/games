#Makes 4 images evenly distributed!
#This time I want to add a button

import matplotlib
import tkinter
from tkinter import *
from PIL import ImageTk, Image
from math import floor, ceil
import random
from random import choices
from os import listdir
import tkinter.messagebox
from functools import partial


#Who is playing?
#playerNames = ["Larry", "Kimi", "Brian", "Mom", "Cleo", "Elenor"]
#playerNames = ["Larry", "Kimi"]
playerNames = ["Larry", "Kimi", "Brian", "Mom"]

#If this is true, the game will distrubute die roll probabilities that I think is "funnest"
#If it's false, it'll give equal weight to all 3
fancyProbMode = True

projectPath = "C:/Users/capud/Documents/git/games/billionsOfBirds"

#How many points to play to?  
pointsRemainingInitial = 40 #150
pointsRemaining = pointsRemainingInitial

######################################## Initializing and odds and ends


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
takeHomeButtons = []
picName = []
numBirds = 4

whoseTurn = 0

# Create an instance of tkinter window
win = Tk()
win.title('Billions of Birds')

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

#What fraction of the height should image take up?  
#subtract a little buffer to make sure the button doesn't look weird
imHeight = floor(windowHeight*2/3) - 50;

#Set up the list of bird photos
#photoDir = projectPath + "/birdPhotos"
photoDir = projectPath + "/kimiBirb"
photoList = listdir(photoDir)
photoIndexOptions = list(range(len(photoList)))
#Turn on the names to the birds only when it's Kimi's set that named the birds nicely
addBirdName = "kimiBirb" in photoDir

#read in the stories
fStories=open(otherPath + "/stories.txt")
stories = fStories.readlines()
storyIndexOptions = list(range(len(stories)))

#read in the stories
fAdj=open(otherPath + "/adj.txt")
adj = fAdj.readlines()
adjIndexOptions = list(range(len(adj)))

#This is an empty virtual 1x1 pixel
#This is added to the botton so that height and width are in pixels
#default is "text units", which I find clunky
pixelVirtual = PhotoImage(width=1, height=1)

######################################## Take a bird home

#A list for each player
# Create an empty list
imagesPlayersTookHome = []
# Iterate over a sequence of numbers from 0 to 4
for i in range(len(playerNames)):
    # In each iteration, add an empty list to the main list
    imagesPlayersTookHome.append([])

def takeBirdHome(iPosition):

    #Figure out who is taking it home
    iPlayer = -1
    numChecked = 0;
    for iP in range(len(playerNames)):
        #print(playerNames[iP] + ": " + str(isChecked[iP]) + " ...or " + str(isChecked[iP].get()))
        if isChecked[iP].get(): 
            iPlayer = iP
            numChecked = numChecked + 1
    
    #This only works if EXACTLY one player is checked, they are the ones that take the bird home
    if numChecked != 1:
       tkinter.messagebox.showerror("No!", "You checked " + str(numChecked) + " players, but you need to check exactly 1 for this")
    else:
        #Add bird they took home
        #Just save the image name, I was tempted to add the formmated image, but it'll need to be resized later
        #debug with sand hill crane, it's weird dimensions
        #imageTk = prepareImageTk(photoDir + "/" + "sandhill crane.jpg", homeImageWidth, homeImageHeight)
        imagesPlayersTookHome[iPlayer].append(photoDir + "/" + picName[iPosition])
        makeTakeBirdHomeWindow(iPlayer)
        isChecked[iPlayer].set(0)


def addTakeHomeCaption():
    for iPosition in range(numBirds):
        #Kimi wants the caption to be at the bottom of the photo, that's what she gets!
        #Idea is to have it be right below the picture and same width 
        imPlaceInfo = labels[iPosition].place_info()
        xPos = int(imPlaceInfo["x"])
        #upper left corner of image plus image height + some buffer
        yPos = int(imPlaceInfo["y"]) + labels[iPosition].image.height() + 10

        if len(takeHomeButtons)<numBirds:
            #Make the button for the first time
            #I tried lambda for adding arguements to takeBirdHome, it always used iPostion of last one though
            takeBirdHome_with_arg = partial(takeBirdHome, iPosition)
            takeHomeButtons.append(
                Button(
                    text ="Take Me Home", 
                    command = takeBirdHome_with_arg,
                    image=pixelVirtual,
                    width = imWidth,
                    compound="c",
                    bg="#abf7b1"))
                    
        #reposition
        takeHomeButtons[iPosition].place( x=xPos , y=yPos)
        #rename only if it's kimi's data set
        if addBirdName:
            takeHomeButtons[iPosition].config(text="Take Me Home\n" + picName[iPosition].split('.')[0])

def makeTakeBirdHomeWindow(iPlayer):
    numBirdsHome = len(imagesPlayersTookHome[iPlayer])

    #Don't make a window if there are no birds
    if numBirdsHome > 0:
        #Make a new window with all of that player's birds
        winHome = Toplevel(win)
        winHome.title(playerNames[iPlayer] + "'s birds")    
        
        #Place birds taken home on a grid
        #Height and width of photo depends on size of grid
        #Base it on size of main window
        #always have 3 rows
        numRows = 3
        homeImageHeight = floor(windowHeight/numRows)
        #number of columns changes based on number of birds
        numCol = ceil(numBirdsHome/numRows)
        homeImageWidth = floor(windowWidth/numCol)

        #populate a grid with all of the birds they took home
        labelsHome = []
        for i in range(len(imagesPlayersTookHome[iPlayer])):
            imageTk = prepareImageTk(imagesPlayersTookHome[iPlayer][i], homeImageWidth, homeImageHeight)
            labelsHome.append(Label(winHome, image=imageTk))
            labelsHome[i].image = imageTk
            #position the photo...let them auto do it
            labelsHome[i].grid(row=i%numRows, column=floor(i/numRows))
    else:
        tkinter.messagebox.askokcancel(title="Derp", message=playerNames[iPlayer]+" has no birds.")


######################################## Restting and initilizing images

def resetBirdPics():
    #populate bird pictures
    #loop over the picture in eac location
    
    global photoIndexOptions, probHome
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
        
        imageTk = prepareImageTk(photoDir + "/" + photoList[iImage], imWidth, imHeight)

        if len(labels)<numBirds:
            #This is the first printing
            labels.append(Label(win, image=imageTk))
            picName.append(photoList[iImage])
        else:
            #remove the old one
            labels[iPosition].destroy()
            picName[iPosition] = photoList[iImage]

        #position the photo
        labels[iPosition] = Label(win, image=imageTk)
        labels[iPosition].image = imageTk
        xPosition = buffer * (iPosition + 1) + imWidth * iPosition
        labels[iPosition].place(x=xPosition, y=ceil(windowHeight/3))
    addTakeHomeCaption()
    probHome = 0

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

#A lot of these ratios I picked for aesthetics
buttonHeightPixels = floor(windowHeight/5.5)
buttonWidthPixels = floor(windowWidth/12)
buttonBuffer = floor(buttonWidthPixels/5)
bottonColor = '#013220'
buttonFontColor = 'white'
distanceFromEdge = windowWidth-2*buttonWidthPixels
distanceFromTop = floor(buttonHeightPixels/5)

B2 = Button(
    text ="Pull up Adjective", 
    command = pullUpAdj,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg=bottonColor,
    fg=buttonFontColor)
#distanceFromEdge = distanceFromEdge - buttonBuffer - buttonWidthPixels
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
iDice = -1
def rollDice():
    global whoseTurn, probHome, iDice
    #We want to make sure the birds are reset BEFORE the roll because it affects the prob of the roll
    #Let the user do it manually if they want
    #iDice represents the last roll.  I'm using a magic number here, there's an assertion elsewhere that should catch if things change
    continueRolling = True
    if iDice==2 and probHome > 0:
        res=tkinter.messagebox.askquestion('Hey Buddy', 'Are you sure you want to reroll before resetting the birds?')
        if res == 'no' :
            continueRolling = False

    if continueRolling:
        probHome, pRoll = getDiceProbs(probHome, diceOptions)
        #see description of fancyProbMode at the top of the code
        if fancyProbMode:
            iDiceList = choices(range(len(diceOptions)), pRoll)
            iDice = iDiceList[0]
        else:
            iDice = random.randint(0, len(diceOptions)-1)
        diceButton.config(text="\n" + playerNames[whoseTurn] + "'s roll:\n\n" + diceOptions[iDice])
        diceButton.config(anchor="n")
        diceButton.config(bg=colorDice[iDice])
        #Keep track of whose turn it is
        if whoseTurn < len(playerNames)-1:
            whoseTurn = whoseTurn + 1
        else:
            whoseTurn = 0

def getDiceProbs(probHome, diceOptions):
    #First itteration gave equal weight to each die roll
    #But resetting twice in a row feels bad
    #Also the sotries are more fun than the adj
    #So have the p(Home) grow.  Give a story a higher weight than adj
    assert len(diceOptions)==3, "Sorry, I use magic numbers here and you'll need to adjust for that"
    iStory = 0
    iAdj = 1
    iHome = 2
    pRoll=len(diceOptions)*[0]
    pRoll[iHome] = probHome
    #Story should be a tiny bit more likely than adjective because it's more fun
    pRoll[iStory] = (1 - probHome) * 0.6
    pRoll[iAdj] = (1 - probHome) * 0.4
    #prob of taking a bird home grows every roll
    if probHome < 0.45:
        probHome = probHome + 0.15
    else:
        #we've been with these birds long enough, grow faster!
        probHome = probHome + 0.25
    return probHome, pRoll
    

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

B = Button(
    text ="Reset Birds", 
    command = resetBirdPics,
    image=pixelVirtual,
    height = buttonHeightPixels, 
    width = buttonWidthPixels,
    compound="c",
    bg=bottonColor,
    fg=buttonFontColor)
distanceFromEdge = distanceFromEdge - buttonBuffer - buttonWidthPixels
B.place( x=distanceFromEdge , y=distanceFromTop)
        
        

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
        makeTakeBirdHomeWindow(iP)
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

