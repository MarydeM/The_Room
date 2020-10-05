######################################################################
# Name:Mary deMarigny & Chloe Boudreaux
# Date:09/29/2020
# Description: Text Based Game_Updated: Python 3.8
######################################################################

#I added to my game the following features:
    #item descriptions change when grabbables are picked up
    #there is an extra room, items, and grababble
    #the extra room contains a dragon and a hidden item that is not revealed until the dragon is killed
    #once the dragon is found, a countdown starts before the player is killed, and is only stopped by killing the dragon
    #there is a shooting mechanism that only works once the gun is obtained
    #there is a chest that can only be open once the key is obtained
    #there is a secret room that is revealed when the book is placed on the bookshelf
    
#Used for the timer on the Dragon
from tkinter import *
from time import time

class Room():
    
    #the constructor 
    def __init__(self, name, image):
        self.name = name
        #Dictionaries
        self.image = image
        self.exits = {}
        self.items = {}
        self.grabbables = []
        
    #mutators and grabers
    @property
    def name(self):                   
        return self._name             
                                      
    @name.setter                      
    def name(self, value):            
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value
                                      
    @property                         
    def exits(self):                  
        return self._exits            
                                      
    @exits.setter                     
    def exits(self, value):           
        self._exits = value           
                                      
    @property                         
    def items(self):                  
        return self._items            
                                      
    @items.setter                     
    def items(self, value):           
        self._items = value           
                                      
    @property                         
    def grabbables(self):             
        return self._grabbables       
                                      
    @grabbables.setter                
    def grabbables(self, value):      
        self._grabbables = value      
        
    # Class functions
        
    def addExit(self, exit, room):
        self._exits[exit] = room

    def addItem(self, item, desc):
        self._items[item] = desc
        
    def addGrabbable(self, item):
        self._grabbables.append(item)
        
    def delGrabbable(self, item):
        self._grabbables.remove(item)

    def __str__(self):
        s = "You are in {}.\n".format(self.name)
        s += "You see: "
        for item in self.items.keys():
            s += item + " "
        s += "\n"
        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "
        return s
    
    #Exit Class
class Game(Frame):

    def __init__(self, parent):
        #call the constructor
        self.parent = parent
        Frame.__init__(self, parent)

    def setupGUI(self):
        #Organize the GUI
        self.pack(fill = BOTH, expand = 1)
        #setup the player input at the bottom of the GUI
        #widget is a TKinter Entry
        Game.player_input = Entry(self, bg ='white')
        #function process in the class
        Game.player_input.bind('<Return>', self.process)
        #push it to the bottom of the GUI and let it fill horrizontally
        Game.player_input.pack(side = BOTTOM, fill = X)
        #give it focus so the player doesnt have to click it to type
        Game.player_input.focus()
        #set image to the left of the GUI
        img = None
        #the widget is a TKinter Label
        #don't let the image control the widget's size
        Game.image = Label(self, width=WIDTH // 2, image=img)
        Game.image_names.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)
        #setup the text to the right of the GUI
        #first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH // 2)
        #the widget is a TKinter Text
        #disable it by default
        #don't let the widget control the frame's size
        Game.text = Text(text_frame, bg='lightgrey', state=DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

    @property
    def parent(self):
        return self.parent

    def parent(self, parent):
        self.parent = parent

    def setRoomImage(self):
        if(Game.currentRoom == None):
            Game.img = PhotoImage(file = "Pictures\skull.gif")
        else:
            Game.img = PhotoImage(file = Game.currentRoom.image)
        Game.image.config(image=Game.img)
        Game.image.image = Game.img

    def setStatus(self, status):
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)
        if(Game.currentRoom == None):
            #If dead, let the player know
            Game.text.insert(END, "You are dead. The only thing you can do now is quit.\n")
        else:
            Game.text.insert(END, str(Game.currentRoom) +\
                             "\nYou are carrying: " + str(Game.inventory) +\
                             "\n\n" + status)
        Game.text.config(state = DISABLED)

    def process(self, event):
        #grabs the players input from the bottom of the GUI
        action = Game.player_input.get()
        #sets input to all lowercase
        action = action.lower()
        #set a default response
        response = ("I don't quite understand. Try verb noun. Valid verbs are go, look, and take")
        if(action == "quit" or action == "exit" or action == "bye"\
           or action == "salut" or action == "sionara"\
           or action == "au revoir"):
            exit(0)
        if(Game.currentRoom == None):
            #clears player's input
            Game.player_input.delete(0, End)
            return
        if(Game.currentRoom == r5):
            self.dragon()
        words = action.split()
        if(len(words) == 2):
            verb = words[0]
            noun = words[1]
            if(verb == "go"):
                response = ("Invalid exit.")
                if(noun in Game.currentRoom.exits):
                    Game.currentRoom = Game.currentRoom.exits[noun]
                    response = ("Room changed")
            elif(verb == "look"):
                response = "I don't see that item."
                if(noun in Game.currentRoom.items):
                    response = Game.currentRoom.items[noun]
            elif(verb == "take"):
                response = ("I don't see that item")
                for grabbable in Game.currentRoom.grabbables:
                    if(noun == grabbable):
                        Game.inventory.append(grabbable)
                        Game.currentRoom.delGrabbable(grabbable)
                        response = ("Item grabbed")
                        #no need to check anymore
                        break
                    
        #Changes room picture, states new status, and edits room if necessary
        self.roomEdit()
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)

    def Play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")

    def dragon(self): ##### This Prints a Dragon ##### I dont know how this will go and just wanted to have it
        global start                                 #here
        start = time() ##### Starts a timer #####
        Game.text.insert(END, " " * 14 + "_" * 14               
                         + " " * 8 + ",===:'.," + " " * 12 + "`-._\n"
                         + " " * 13 + "`:.`---.__" + " " * 9 + "`-._\n"
                         + " " * 15 + "`:.     `--.         `.\n"
                         + " " * 17 + "\.        `.         `.\n"
                         + " " * 9 + "(,,(,    \.         `.   ____,-`.,\n"
                         + " " * 6 + "(,'     `/   \.   ,--.___`.'\n"
                         + " " * 2 + ",  ,'  ,--.  `,   \.;'         `\n"
                         + " " * 3 + "`{D, {    \  :    \;\n"
                         + " " * 5 + "V,,'    /  /    //\n"
                         + " " * 5 + "j;;    /  ,' ,-//.    ,---.      ,\n"
                         + " " * 5 + "\;'   /  ,' /  _  \  /  _  \   ,'/\n" 
                         + " " * 11 + "\   `'  / \  `'  / \  `.' /\n"
                         + " " * 12 + "`.___,'   `.__,'   `.__,'\n")

    def createRooms(self):
        #names are made global so they can be used elsewhere
        global currentRoom
        global r1
        global r2
        global r3
        global r4
        global r5
        global r6
        #room names and images connected to the room
        r1 = Room("the livingroom", "Pictures/firstRoom.gif")
        r2 = Room("the bedroom", "Pictures/firstRoom.gif")
        r3 = Room("the office", "Pictures/firstRoom.gif")
        r4 = Room("the spare room", "Pictures/firstRoom.gif")
        r5 = Room("the Dungeon", "Pictures/firstRoom.gif")
        r6 = Room("the secret room", "Pictures/firstRoom.gif")
        #room 1
        r1.addExit("east", r2)
        r1.addExit("south", r3)
        r1.addGrabbable("key")
        r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
        r1.addItem("table", "It is made of oak. A golden key rests on it.")
        #room 2
        r2.addExit("west", r1)
        r2.addExit("south", r4)
        r2.addGrabbable("gun")
        r2.addItem("closet", "There's just a dirty, old coat with a gun in " \
                   "the pocket") 
        r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
        r2.addItem("fireplace", "It is full of ashes.")
        #room 3
        r3.addExit("north", r1)
        r3.addExit("east", r4)
        r3.addGrabbable("book")
        r3.addItem("bookshelves", "They are empty. Go figure.")
        r3.addItem("statue", "There is nothing special about it.")
        r3.addItem("desk", "The statue is resting on it. So is a book.")
        # room 4
        r4.addExit("north", r2)
        r4.addExit("west", r3)
        r4.addExit("south", r5) 
        r4.addGrabbable("6-pack")
        r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on " \
                   "the brew rig. A 6-pack is resting beside it.")
        #room 5
        r5.addExit("north", r4)
        r5.addItem("dragon!!!", "Does it matter what it looks like?! Kill it!")
        #room 6
        r6.addExit("east", r3)
        r6.addItem("safe", "It has a dial on it. I wonder what the code could be.")
        Game.currentRoom = r1
        Game.inventory = [] #initialize the player's inventory

    # edits the description of items once a grabable is in player's inventory
    def roomEdit(self):
        if Game.currentRoom == r1:
            if "key" in Game.inventory:
                r1.items["table"] = ("It is made of oak. Nothing is on it")
        if Game.currentRoom == r2:
            if "gun" in Game.inventory:
                r2.items["closet"] = ("There's just a dirty, old coat")
        if Game.currentRoom == r3:
            if "book" in Game.inventory:
                r3.items["desk"] = ("The statue is resting on it")
        if Game.currentRoom == r4:
            if "6-pack" in Game.inventory:
                r4.items["brew_rig"] = ("Gourd is brewing some sort of oatmeal " \
                                        "stout on the brew rig. Did you really " \
                                            "take his beer?")
        if Game.currentRoom == r5:
            if dragonDead == True:
                #changes the name of the dragon once killed
                del r5.items["dragon!!!"]
                r5.addItem("dead_dragon", "Yup, that's a dead dragon, alright")
                #reveals the previously hidden chest
                r5.addItem("chest", "It is very large and appears to be locked")

#moved create rooms to Game class
           
#setting starting game variables 
shots = 0
dragonDead = False
characterDead = False

#enables dragon shooting abilities 
def shoot():
    global start
    global shots 
    global dragonDead
    global characterDead
    shots += 1
    end = time()
    elapsed = end - start ##### players have ten seconds to kill the dragon #####
    if shots < 2:
        if elapsed > 10:
            characterDead = True ##### Executes the Death function #####
        return "Got him! But he's still alive!!" 
    elif shots < 4:
        if elapsed > 10:
            characterDead = True ##### Executes the Death function #####
        return "He's getting closer to you!"
    elif shots < 6:
        if elapsed > 10:
            characterDead = True ##### Executes the Death function #####
        return "Almost there!"
    elif shots == 6:
        dragonDead = True ##### When this changes, the status of the character can be printed again.#####
        return "He's dead! Well that was exciting"
    elif shots > 6:
        return "He's already dead, you psychopath"              

#displays a jolly roger when the player dies
def death():
    print (" " * 17 + "u" * 7)
    print (" " * 13 + "u" * 2 + "$" * 11 + "u" * 2)
    print (" " * 10 + "u" * 2 + "$" * 17 + "u" * 2)
    print (" " * 9 + "u" + "$" * 21 + "u")
    print (" " * 8 + "u" + "$" * 23 + "u")
    print (" " * 7 + "u" + "$" * 25 + "u")
    print (" " * 7 + "u" + "$" * 25 + "u")
    print (" " * 7 + "u" + "$" * 6 + "\"" + " " * 3 + "\"" + "$" * 3 + "\"" + " " * 3 + "\"" + "$" * 6 + "u")
    print (" " * 7 + "\"" + "$" * 4 + "\"" + " " * 6 + "u$u" + " " * 7 + "$" * 4 + "\"")
    print (" " * 8 + "$" * 3 + "u" + " " * 7 + "u$u" + " " * 7 + "u" + "$" * 3)
    print (" " * 8 + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3 + "u" + " " * 6 + "u" + "$" * 3)
    print (" " * 9 + "\"" + "$" * 4 + "u" * 2 + "$" * 3 + " " * 3 + "$" * 3 + "u" * 2 + "$" * 4 + "\"")
    print (" " * 10 + "\"" + "$" * 7 + "\"" + " " * 3 + "\"" + "$" * 7 + "\"")
    print (" " * 12 + "u" + "$" * 7 + "u" + "$" * 7 + "u")
    print (" " * 13 + "u$\"$\"$\"$\"$\"$\"$u")
    print (" " * 2 + "u" * 3 + " " * 8 + "$" * 2 + "u$ $ $ $ $u" + "$" * 2 + " " * 7 + "u" * 3)
    print (" u" + "$" * 4 + " " * 8 + "$" * 5 + "u$u$u" + "$" * 3 + " " * 7 + "u" + "$" * 4)
    print (" " * 2 + "$" * 5 + "u" * 2 + " " * 6 + "\"" + "$" * 9 + "\"" + " " * 5 + "u" * 2 + "$" * 6)
    print ("u" + "$" * 11 + "u" * 2 + " " * 4 + "\"" * 5 + " " * 4 + "u" * 4 + "$" * 10)
    print ("$" * 4 + "\"" * 3 + "$" * 10 + "u" * 3 + " " * 3 + "u" * 2 + "$" * 9 + "\"" * 3 + "$" * 3 + "\"")
    print (" " + "\"" * 3 + " " * 6 + "\"" * 2 + "$" * 11 + "u" * 2 + " " + "\"" * 2 + "$" + "\"" * 3)
    print (" " * 11 + "u" * 4 + " \"\"" + "$" * 10 + "u" * 3)
    print (" " * 2 + "u" + "$" * 3 + "u" * 3 + "$" * 9 + "u" * 2 + " \"\"" + "$" * 11 + "u" * 3 + "$" * 3)
    print (" " * 2 + "$" * 10 + "\"" * 4 + " " * 11 + "\"\"" + "$" * 11 + "\"")
    print (" " * 3 + "\"" + "$" * 5 + "\"" + " " * 22 + "\"\"" + "$" * 4 + "\"\"")
    print (" " * 5 + "$" * 3 + "\"" + " " * 25 + "$" * 4 + "\"")

#displays a dragon when it is encountered        
def dragon(): ##### This Prints a Dragon #####
    global start 
    start = time() ##### Starts a timer #####
    print (" " * 14 + "_" * 14               )
    print (" " * 8 + ",===:'.," + " " * 12 + "`-._"        )           
    print (" " * 13 + "`:.`---.__" + " " * 9 + "`-._"      )                 
    print (" " * 15 + "`:.     `--.         `."            )     
    print (" " * 17 + "\.        `.         `."            )  
    print (" " * 9 + "(,,(,    \.         `.   ____,-`.,"  )           
    print (" " * 6 + "(,'     `/   \.   ,--.___`.'"        )      
    print (" " * 2 + ",  ,'  ,--.  `,   \.;'         `"    )               
    print (" " * 3 + "`{D, {    \  :    \;"                )                    
    print (" " * 5 + "V,,'    /  /    //"                  )               
    print (" " * 5 + "j;;    /  ,' ,-//.    ,---.      ,"  )                 
    print (" " * 5 + "\;'   /  ,' /  _  \  /  _  \   ,'/"  )                 
    print (" " * 11 + "\   `'  / \  `'  / \  `.' /"          )    
    print (" " * 12 + "`.___,'   `.__,'   `.__,'")
    
#displays a chest when it is opened
def chest():##### This prints a chest when the game is won #####
    print ("*******************************************************************************")
    print ("          |                   |                  |                     |")
    print (" _________|________________.=\"\"_;=.______________|_____________________|_______")
    print ("|                   |  ,-\"_,=\"\"     `\"=.|                  |")
    print ("|___________________|__\"=._o`\"-._        `\"=.______________|___________________")
    print ("          |                `\"=._o`\"=._      _`\"=._                     |")
    print (" _________|_____________________:=._o \"=._.\"_.-=\"'\"=.__________________|_______")
    print ("|                   |    __.--\" , ; `\"=._o.\" ,-\"\"\"-._ \".   |")
    print ("|___________________|_._\"  ,. .` ` `` ,  `\"-._\"-._   \". '__|___________________")
    print ("          |           |o`\"=._` , \"` `; .\". ,  \"-._\"-._; ;              |")
    print (" _________|___________| ;`-.o`\"=._; .\" ` '`.\"\` . \"-._ /_______________|_______")
    print ("|                   | |o;    `\"-.o`\"=._``  '` \" ,__.--o;   |")
    print ("|___________________|_| ;     (#) `-.o `\"=.`_.--\"_o.-; ;___|___________________")
    print ("____/______/______/___|o;._    \"      `\".o|o_.--\"    ;o;____/______/______/____")
    print ("/______/______/______/_\"=._o--._        ; | ;        ; ;/______/______/______/_")
    print ("____/______/______/______/__\"=._o--._   ;o|o;     _._;o;____/______/______/____")
    print ("/______/______/______/______/____\"=._o._; | ;_.--\"o.--\"_/______/______/______/_")
    print ("____/______/______/______/______/_____\"=.o|o_.--\"\"___/______/______/______/____")
    print ("/______/______/______/______/______/______/______/______/______/______/_____/__")
    print ("*******************************************************************************")
    
######################################################################
#                          START THE GAME!!!                         #
######################################################################
WIDTH, HEIGHT = 800, 600 #window resolution

#create the window
window = Tk()
window.geometry("{0}x{1}".format(WIDTH, HEIGHT))
window.title("Room Adventure")
#create the GUI and then play the game
my_canvas = Game(window)
my_canvas.Play()
#wait for the window to close
window.mainloop()


#I commented this out while we put the game together
###game introduction
##print ("Welcome! Have a look around, and you never know what you might find." \
##       " Access your available options at any time by typing \"options\"")
##
###displays character's status
##while (True):
##    #as long as the dragon is not being fought, so the room information is \
##    #not printed after every shot is fired at the dragon
##    if shots == 0 or dragonDead == True:
##        status = "{}\nYou are carrying: {}\n".format(currentRoom, inventory)
##        #ends the game once the gold is found
##        if game == "over":
##            print ("You are carrying: {}".format(inventory))
##            break #Exits the game
##        print ("=========================================================")
##        print (status)
##    
##    #gets player input on what to do
##    action = input("What to do? ")
##    #changes input to all lowercase for legibility
##    action = action.lower()
##    
##    #executes the death function when killed by dragon
##    if (characterDead == True):
##        death()
##        print ("You died")
##        break
##    
##    #default response
##    response = ("I don't understand. Try verb noun.")
##    
##    #allows player to exit the game
##    if (action == "quit" or action == "exit" or action == "bye" or \
##        action == "end"): 
##        response = "Quitting already? That's no fun. Goodbye"
##        print (response)
##        break
##    
##    #displays the options at the player's request
##    if (action == "options"):
##        response = ("Your verb options are go, look, take, open, place, and " \
##                    "shoot. \n Your noun options are {} {}".format(inventory, \
##                        currentRoom.items))
##    
##    #controlls all actions/ executes player input
##    #splits input into a list
##    words = action.split()
##    if (len(words) == 2):
##        verb = words[0]
##        noun = words[1]
##        
##        if (verb == "go"):
##            response = "Invalid exit."
##            if (noun in currentRoom.exits):
##                currentRoom = currentRoom.exits[noun]
##                response = "Room changed."
##                #starts the dragon attack
##                if currentRoom == r5 and dragonDead == False:
##                    response = "A dragon is atatcking you! Shoot him!"
##                    dragon()
##                
##        elif (verb == "look"):
##            response = "I don't see that item."
##            if (noun in currentRoom.items):
##                response = currentRoom.items[noun]
##                              
##        elif (verb == "take" or verb == "grab"):
##            response = "I don't see that item."
##            for grabbable in currentRoom.grabbables:
##                if (noun == grabbable):
##                    inventory.append(grabbable)
##                    currentRoom.delGrabbable(grabbable)
##                    response = "Item grabbed."
##                    #runs the function that changes the item descsriptions
##                    roomEdit()
##                
##        #opens the chest behind the dragon after it is revealed
##        elif (verb == "open" or verb == "unlock"):
##            response = "I can't open that."
##            if (currentRoom == r5) and (noun == "chest"):
##                if ("key" in inventory):
##                    inventory.append("infinite_wealth")
##                    #prints the chest
##                    chest()
##                    response = "So... much... GOLD!!! \n You're rich!!!"
##                    game = "over"
##        
##        #reveals secret room once book is placed on bookshelf
##        elif (verb == "place"):
##            response = "Place it where? The ground?!"
##            if (currentRoom == r3) and (noun == "book") and ("book" in inventory):
##                inventory.remove("book")
##                response = "The bookshelf swings back. A secret room appears!"
##                r3.addExit("west", r6)
##            if noun != "book":
##                response = "You should keep that for now."
##    
##    #allows the player to shoot the dragon with input "shoot"
##    elif (len(words) == 1):
##        verb = words[0]
##        
##        if (verb == "shoot"):
##            response = "Shoot with what? Finger guns?"
##            if "gun" in inventory:
##                response = "You put a hole in the wall. Why would you do that?"
##            if currentRoom == r5 and "gun" in inventory:
##                #deploys shoot function
##                response = shoot()
##            #reveals the chest once the dragon is dead
##            if dragonDead == True:
##                roomEdit()
##                           
##    print ("\n{}".format(response))
##
