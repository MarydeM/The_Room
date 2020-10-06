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
import time

class Room():
    
    #the constructor 
    def __init__(self, name, image):
        self.name = name
        #Dictionaries
        self.image = image
        self.exits = {}
        self.items = {}
        #inventory
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

    #constructor
    def __init__(self, parent):
        #call the constructor
        Frame.__init__(self, parent)
        
    #setting starting game variables 
    game = None
    shots = 0
    dragonDead = False
    characterDead = False
   
    #creates the rooms
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
        r2 = Room("the bedroom", "Pictures/secondRoom.gif")
        r3 = Room("the office", "Pictures/thirdRoom.gif")
        r4 = Room("the spare room", "Pictures/forthRoom.gif")
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
        #initialize the player's inventory 
        Game.currentRoom = r1
        Game.inventory = [] 

    #sets up the GUI
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
        Game.image = Label(self, width = WIDTH // 2, image=img)
        Game.image = Label(self, width = WIDTH // 2, image = img)
        Game.image_names.image = img
        Game.image.pack(side = LEFT, fill = Y)
        Game.image.pack_propagate(False)
        #setup the text to the right of the GUI
        #first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH // 2)
        #the widget is a TKinter Text
        #disable it by default
        #don't let the widget control the frame's size
        Game.text = Text(text_frame, bg = 'lightgrey', state = DISABLED)
        Game.text.pack(fill = Y, expand = 1)
        text_frame.pack(side = RIGHT, fill = Y)
        text_frame.pack_propagate(False)

    #set the current room image
    def setRoomImage(self):
        #sets skull image when character dies
        if(self.characterDead == True):
            Game.img = PhotoImage(file = "Pictures\skull.gif")
        #sets chest image when character wins
        elif(self.game == "over"):
            Game.img = PhotoImage(file = "Pictures\chest.gif")
        else:
            Game.img = PhotoImage(file = Game.currentRoom.image)
        Game.image.config(image = Game.img)
        Game.image.image = Game.img

    #sets the status displayed on the right of the GUI
    def setStatus(self, status):
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)
        #If dead, let the player know
        if(self.characterDead == True):
            Game.text.insert(END, "You are dead. The only thing you can do now"\
                             " is quit.\n")
        else:
            Game.text.insert(END, str(Game.currentRoom) +\
                             "\nYou are carrying: " + str(Game.inventory) +\
                             "\n\n" + status)
        Game.text.config(state = DISABLED)

    #play the game
    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")

    #processes the player's input
    def process(self, event):
        #grabs the players input from the bottom of the GUI
        action = Game.player_input.get()
        #sets input to all lowercase
        action = action.lower()
        #set a default response
        response = ("I don't quite understand. Try verb noun. Valid verbs are" \
                    " go, look, take, open, place, and shoot.")
        #allows player to exit the game
        if (action == "quit" or action == "exit" or action == "bye"\
           or action == "salut" or action == "sionara"\
           or action == "au revoir"):
            #closes the window and the program
            window.destroy()
        #displays the options at the player's request
        if (action == "options"):
            response = ("Your verb options are go, look, take, open, place," \
                        "and shoot.")
        #shoots the dragon
        if (action == "shoot"):
            response = ("Shoot with what? Finger guns?")
            if ("gun" in Game.inventory):
                response = ("You put a hole in the wall. Why would you do that?")
            if (Game.currentRoom == r5) and ("gun" in Game.inventory):
                #deploys shoot function
                response = (self.shoot())
        #Ends the game 
        if (self.characterDead == True):
            #clears player's input
            Game.player_input.delete(0, "end")  #This doesn't work for some reason
            return
        #for two word inputs (verb, noun)
        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]
            #to change rooms
            if (verb == "go"):
                response = ("Invalid exit.")
                if (noun in Game.currentRoom.exits):
                    Game.currentRoom = Game.currentRoom.exits[noun]
                    response = ("Room changed")
                    #starts the dragon attack
                    if Game.currentRoom == r5 and self.dragonDead == False:
                        response = ("A dragon is atatcking you! Shoot him!")
                        self.dragon()
            #to look at items
            elif (verb == "look"):
                response = ("I don't see that item.")
                if (noun in Game.currentRoom.items):
                    response = Game.currentRoom.items[noun]
            #to add grabbables
            elif (verb == "take"):
                response = ("I don't see that item")
                for grabbable in Game.currentRoom.grabbables:
                    if (noun == grabbable):
                        Game.inventory.append(grabbable)
                        Game.currentRoom.delGrabbable(grabbable)
                        response = ("Item grabbed")
            #opens the chest behind the dragon after it is revealed
            elif (verb == "open" or verb == "unlock"):
                response = ("I can't open that.")
                if (Game.currentRoom == r5) and (noun == "chest") and (self.dragonDead == True):
                    if ("key" in Game.inventory):
                        #adds wealth to the player's inventory
                        Game.inventory.append("infinite_wealth")
                        response = ("So... much... GOLD!!! \n You're rich!!!")
                        #ends the game
                        self.game = "over"
            #reveals secret room once book is placed on bookshelf
            elif (verb == "place"):
                response = ("Place it where? The ground?!")
                if (Game.currentRoom == r3) and (noun == "book") and \
                    ("book" in Game.inventory):
                    Game.inventory.remove("book")
                    response = ("The bookshelf swings back. A secret room appears!")
                    r3.addExit("west", r6)
                if noun != "book":
                    response = ("You should keep that for now.")
                    
        #Changes room picture, states new status, and edits room if necessary
        self.roomEdit()
        self.setStatus(response)
        self.setRoomImage()
        Game.player_input.delete(0, END)

    #starts the Boss fight
    def dragon(self):
        #Starts a timer for the player to kill the dragon
        global start
        start = time.time()
    
    #edits the description of items once a grabable is in player's inventory
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
            if self.dragonDead == True and "dragon!!!" in r5.items:
                #changes the name of the dragon once killed
                del r5.items["dragon!!!"]
                r5.addItem("dead_dragon", "Yup, that's a dead dragon, alright")
                #reveals the previously hidden chest
                r5.addItem("chest", "It is very large and appears to be locked")

    #enables dragon shooting abilities 
    def shoot(self):
        global start 
        self.dragonDead
        self.characterDead
        self.shots += 1
        #players have ten seconds to kill the dragon
        end = time.time()
        elapsed = end - start
        #varied responses
        if self.shots < 2:
            if elapsed > 10:
                # Executes the Death function
                self.characterDead = True
            return "Got him! But he's still alive!!" 
        elif self.shots < 4:
            if elapsed > 10:
                self.characterDead = True
            return "He's getting closer to you!"
        elif self.shots < 6:
            if elapsed > 10:
                self.characterDead = True
            return "Almost there!"
        elif self.shots == 6:
            # When this changes, the status of the character can be printed again
            self.dragonDead = True
            return "He's dead! Well that was exciting"
        elif self.shots > 6:
            return "He's already dead, you psychopath"           

def death():
    pass
######################################################################
#                          START THE GAME!!!                         #
######################################################################


#Game Intro
# print ("Welcome! Have a look around, and you never know what you might find." \
      # " Access your available options at any time by typing \"options\"")

#window resolution
WIDTH, HEIGHT = 800, 600

#create the window
window = Tk()
window.title("Room Adventure")
#create the GUI
my_canvas = Game(window)
#play the game
my_canvas.play()
#wait for the window to close
window.mainloop()


#I commented this out while we put the game together
###game introduction
# print ("Welcome! Have a look around, and you never know what you might find." \
#       " Access your available options at any time by typing \"options\"")
##
###displays character's status
##while (True):
##    #as long as the dragon is not being fought, so the room information is \
##    #not printed after every shot is fired at the dragon
##    if shots == 0 or dragonDead == True:
##        status = "{}\nYou are carrying: {}\n".format(currentRoom, inventory)
##        #ends the game once the gold is found
##    
#    #executes the death function when killed by dragon
#    if (characterDead == True):
#        death()
#        print ("You died")
#        break
#
##           
# #opens the chest behind the dragon after it is revealed
# elif (verb == "open" or verb == "unlock"):
#     response = "I can't open that."
#     if (currentRoom == r5) and (noun == "chest"):
#         if ("key" in inventory):
#             inventory.append("infinite_wealth")
#             #prints the chest
#             chest()
#             response = "So... much... GOLD!!! \n You're rich!!!"
#             game = "over"
##        
# #reveals secret room once book is placed on bookshelf
# elif (verb == "place"):
#     response = "Place it where? The ground?!"
#     if (currentRoom == r3) and (noun == "book") and ("book" in inventory):
#         inventory.remove("book")
#         response = "The bookshelf swings back. A secret room appears!"
#         r3.addExit("west", r6)
#     if noun != "book":
#         response = "You should keep that for now."
##    
##    #allows the player to shoot the dragon with input "shoot"
##    elif (len(words) == 1):
##        verb = words[0]
##        
# if (verb == "shoot"):
#     response = "Shoot with what? Finger guns?"
#     if "gun" in inventory:
#         response = "You put a hole in the wall. Why would you do that?"
#     if currentRoom == r5 and "gun" in inventory:
#         #deploys shoot function
#         response = shoot()
#     #reveals the chest once the dragon is dead
#     if dragonDead == True:
#         roomEdit()
##                           
##    print ("\n{}".format(response))
##
