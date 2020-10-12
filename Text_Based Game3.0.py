######################################################################
# Name:Mary deMarigny & Chloe Boudreaux
# Date:10/12/2020
# Description: Text Based Game with a GUI attached: Python 3.8
######################################################################
   
#Used for the timer on the Dragon
from tkinter import *
import time

#Used to create room instances
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

    # Prints the status of the character
    def __str__(self):
        s = "You are in {}.\n".format(self.name)
        s += "You see: "
        #adds a ", " after each entry, except when the last entry
        for index, item in enumerate(self.items.keys()):
            s += item
            if index < len(self.items.keys()) - 1:
                s += ", "
        s += "."
        s += "\n"
        s += "Exits: "
        for index, exit in enumerate(self.exits.keys()):
            s += exit
            if index < len(self.exits.keys()) - 1:
                s += ", "
        s += "."
        return s
    
    #Exit Class

# actually plays the game
class Game(Frame):

    #constructor
    def __init__(self, parent):
        #call the parent constructor
        Frame.__init__(self, parent)
        
    #setting starting game variables 
    game = None
    shots = 0
    dragonDead, characterDead = False, False
    characterCuffed = True
    gameStarted = False
   
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
        #r7 is the starting room
        global r7
        
        #room names and images connected to the rooms
        r1 = Room("the foyer", "Pictures/secondRoom.gif")
        r2 = Room("the bedroom", "Pictures/forthRoom.gif")
        r3 = Room("the study", "Pictures/thirdRoom.gif")
        r4 = Room("the keg room", "Pictures/fifthRoom.gif")
        r5 = Room("the dungeon", "Pictures/firstRoom.gif")
        r6 = Room("a hidden office", "Pictures/secretRoom.gif")
        r7 = Room("a prison cell", "Pictures/firstRoom.gif")
        
        #room 1
        r1.addExit("east", r2)
        r1.addExit("south", r3)
        r1.addExit("north", r7)
        r1.addGrabbable("purple_key")
        r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
        r1.addItem("table", "It is made of oak. A purple_key rests upon it.")
        
        #room 2
        r2.addExit("west", r1)
        r2.addExit("south", r4)
        r2.addItem("closet", "There's a dirty, old coat in here, theres a \n" \
                   "paper_slip in the pocket. It has a 4-digit \n code on it.")
        r2.addGrabbable("paper_slip")
        r2.addItem("rug", "It is nice and Indian. It also needs to be \n" \
                   "vacuumed.")
        r2.addItem("fireplace", "It is full of ashes, there is a empty slot" \
                   " in the \n shape of a diamond above the opening.")
        
        #room 3
        r3.addExit("north", r1)
        r3.addExit("east", r4)
        r3.addGrabbable("book")
        r3.addItem("bookshelves", "A collection of book, looks like one is" \
                   " missing \n though.")
        r3.addItem("statue", "There is a large statue in the middle of the" \
                   " \n room. It looks like it's holding a purple_box.")
        r3.addItem("desk", "There is a book resting on the desk.")
        r3.addGrabbable("purple_box")
        
        # room 4
        r4.addExit("north", r2)
        r4.addExit("west", r3)
        r4.addExit("south", r5) 
        r4.addGrabbable("wine")
        r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout" \
                   " on \n the brew rig. Wine is resting beside it in a bottle.")
            
        #room 5
        r5.addExit("north", r4)
        r5.addItem("dragon", "Does it matter what it looks like?! Kill it!")
        
        #room 6
        r6.addExit("east", r3)
        r6.addItem("safe", "It has a dial on it. I wonder what the code" \
                   " could be.")
        r6.addGrabbable("gun")
        r6.addItem("gun", "Someone left their loaded pistol on the desk" \
                   "\n here.")
        
        #room 7
        r7.addExit("south", r1)
        r7.addGrabbable("small_key")
        r7.addItem("handcuffs", "I'm handcuffed to the wall, I can't move.")
        r7.addItem("upturned_bucket", "There is an upside down bucket here, " \
                   "underneath \n it is a small_key.")
        r7.addItem("slot", "There's a slot in the wall in the shape of a \n" \
                   "square.")
        r7.addItem("rags", "It's the closest thing to a bed in this cell.")
        
        #initialize the player's inventory after setting the starting room
        Game.currentRoom = r7
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
        #doesn't let the image control the widget's size
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
        #doesn't let the widget control the frame's size
        Game.text = Text(text_frame, bg = 'lightgrey', state = DISABLED)
        Game.text.pack(fill = Y, expand = 1)
        text_frame.pack(side = RIGHT, fill = Y)
        text_frame.pack_propagate(False)

    #set the current room image
    def setRoomImage(self):
        #sets skull image when character dies
        if (self.characterDead == True) or (Game.currentRoom == None):
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
        
        #If the game is in normal play; i.e. not over
        if (self.characterDead != True) or (Game.currentRoom != None) or \
            (self.game != "over"):
            Game.text.config(state = NORMAL)
            Game.text.delete("1.0", END)
            
        #Sets response at begining of the game to let player know that they \
        #are handcuffed
        if(self.gameStarted == False) and (Game.currentRoom != None):
            Game.text.insert(END, str(Game.currentRoom) +\
                             "\nYou are carrying: " + str(Game.inventory) +\
                             "\n\n" + status +\
                             "You wake up in a dark cell handcuffed to the \n" +\
                             "wall with no memory of how you got here.\n\n" +\
                             "Try verb noun to interact with the enviroment.")
            self.gameStarted = True
            return
        
        #If the game is over, let the player know
        if(self.game == "over"):
            Game.text.insert(END, "So...\nMuch...\nGold!!! \n\n You won!"\
                             "The only thing you can do now \n"\
                             "is quit.")
            Game.text.config(state = DISABLED)
        #If character dies
        elif(self.characterDead == True) or (Game.currentRoom == None):
            Game.text.insert(END, "You are dead. The only thing you can do" \
                             " now \n is quit.")
            self.setRoomImage()
            Game.text.config(state = DISABLED)
        else:
            Game.text.insert(END, str(Game.currentRoom) +\
                             "\nYou are carrying: " + str(Game.inventory) +\
                             "\n\n" + status)
        Game.text.config(state = DISABLED)

    #calls other functions so the game can be played
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
        response = ("I don't quite understand. Try verb noun. Valid \n" \
                    "verbs are go, look, take, open, place, and shoot.")
            
        #allows player to exit the game
        if (action == "quit" or action == "exit" or action == "bye"\
           or action == "salut" or action == "sionara"\
           or action == "au revoir"):
            #closes the window and the program
            window.destroy()
            
        #displays the options at the player's request
        if (action == "options"):
            response = ("Your verb options are go, look, take, unlock, \n" \
                        "place, open, and shoot.")
                
        #shoots the dragon
        if (action == "shoot"):
            response = ("Shoot with what? Finger guns?")
            if ("gun" in Game.inventory):
                response = ("You put a hole in the wall.\nWhy would you do that?")
            if (Game.currentRoom == r5) and ("gun" in Game.inventory):
                #deploys shoot function
                response = (self.shoot())
                
        #Ends the game when the character dies
        if (self.characterDead == True):
            #clears player's input
            Game.player_input.delete(0, END)
            return
        
        #for two word inputs (verb, noun)
        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]
            
            #to change rooms
            if (verb == "go"):
                response = ("Invalid exit.")
                #if character still cuffed at beginning
                if(self.characterCuffed == True):
                    response = ("I can't move, I'm handcuffed to the wall!")
                else:
                    if (noun in Game.currentRoom.exits):
                        Game.currentRoom = Game.currentRoom.exits[noun]
                        response = ("Room changed")
                        #starts the dragon attack
                        if Game.currentRoom == r5 and self.dragonDead == False\
                           and ("gun" in Game.inventory):
                            response = ("A dragon is atatcking you! Shoot him!")
                            self.dragon()
                        elif Game.currentRoom == r5 and self.dragonDead == False:
                            response = ("A dragon is atatcking you! Run!!")
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
                        
            #opens handcuffs, secret door, box, safe, and ending chest
            elif (verb == "open" or verb == "unlock" or verb == "use"):
                response = ("I can't open that.")
                
                #Safe
                if (Game.currentRoom == r6):
                    if (noun == "safe") or (noun == "paper_slip"):
                        response = ("I swing the safe open after inputting the" /
                                    "code.\n There's a small diamond in here.")
                        Game.inventory.remove("paper_slip")
                        Game.inventory.append("diamond")
                        
                #Purple box/key
                if (noun == "purple_box") or (noun == "purple_key"):
                    if ("purple_box" in Game.inventory) and ("purple_key" in Game.inventory):
                        Game.inventory.remove("purple_key")
                        Game.inventory.remove("purple_box")
                        response = ("The small box pops open, revealing a square red\n"
                                    "gemstone that fits in the palm of your hand.")
                        Game.inventory.append("red_gem")
                        
                #Character's handcuffs
                if (Game.currentRoom == r7) and (self.characterCuffed == True) \
                   and ("small_key" in Game.inventory):
                    if (noun == "handcuffs") or (noun == "small_key"):
                        response = ("I unlocked the handcuffs, I can stand up now!")
                        del r7.items["handcuffs"]
                        Game.characterCuffed = False
                        Game.inventory.remove("small_key")
                
                #Secret Door
                if ((Game.currentRoom == r3) and ("secret_door" in r3.items)) \
                    and ((noun == "secret_door") or (noun == "red_key")):
                        r3.addExit("west", r6)
                        Game.inventory.remove("red_key")
                        response = ("I unlocked the door to the hidden room!")
                        r3.items["secret_door"] = ("The door to the hidden" \
                                                   "room, it's unlocked now.")
                        
                #ends the game if chest is unlocked
                if (Game.currentRoom == r5) and (noun == "chest") and \
                    (self.dragonDead == True): 
                    if ("golden_key" in Game.inventory):
                        #ends the game
                        self.game = "over"
                        
            #place gems and book
            elif (verb == "place"):
                #basic response for the command is invalid
                response = ("You should keep that for now.")
                
                #gives player key to end game
                if (Game.currentRoom == r2) and ("diamond" in Game.inventory):
                    Game.inventory.remove("diamond")
                    response = ("Placing the diamond into the slot triggers \n" \
                                "a sound in the walls. There's a key on \n the" \
                                " mantel now.")
                    Game.inventory.append("golden_key")
                    
                #Gives player the key to secret room
                if (Game.currentRoom == r7) and ("red_gem" in Game.inventory) \
                    and (noun == "red_gem"):
                    Game.inventory.remove("red_gem")
                    response = ("You slide the gem into the slot, which reveals" \
                                " a hidden compartment with a red_key inside.")
                    Game.inventory.append("red_key")
                    
                #Reveals secret door in the office
                if (Game.currentRoom == r3) and (noun == "book") and \
                    ("book" in Game.inventory):
                    Game.inventory.remove("book")
                    r3.items["bookshelves"] = ("All books are here and " \
                                               "accounted for.")
                    response = ("The bookshelf swings back. There's a door here!")
                    r3.addItem("secret_door", "The locked door was hidden" \
                               " behind the shelves.\n The handle to the door" \
                                   " is painted red.")
                        
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
            #take the purple key in the foyer
            if "purple_key" in Game.inventory:
                r1.items["table"] = ("It is made of oak. Nothing is on it")
                
        if Game.currentRoom == r2:
            #grab the golden key
            if "golden_key" in Game.inventory:
                r2.items["fireplace"] = ("The fireplace now has a diamond \n" \
                                         "above the opening. Still full of" \
                                             " ash though.")
            #take the slip in the closet
            if "paper_slip" in Game.inventory:
                r2.items["closet"] = ("Just a dusty coat in here.")
                
        if Game.currentRoom == r6:
            #open the safe
            if "diamond" in Game.inventory:
                r6.items["safe"] = ("The safe is empty, I already took" \
                                    " everything")
            #pick up the gun in the office
            if "gun" in Game.inventory:
                if "gun" in r6.items:
                    del r6.items["gun"]
                    
        if Game.currentRoom == r3:
            #pick up book from desk
            if "book" in Game.inventory:
                r3.items["desk"] = ("It's just a empty desk now.")
            #pick up the box the statue is holding
            if "purple_box" in Game.inventory:
                r3.items["statue"] = ("It's just a tall statue in the middle" \
                                      "of the \n room.")
                    
        if Game.currentRoom == r4:
            #pick up wine in keg room
            if "wine" in Game.inventory:
                r4.items["brew_rig"] = ("Gourd is brewing some sort of oatmeal " \
                                        "stout on \n the brew rig. Did you" \
                                            " really just take his \n wine?")
                    
        if Game.currentRoom == r5:
            #changes the name of the dragon once killed
            if self.dragonDead == True and "dragon" in r5.items:
                del r5.items["dragon"]
                r5.addItem("dead_dragon", "Yup, that's a dead dragon, alright")
                #reveals the previously hidden chest
                r5.addItem("chest", "It is a very large wooden chest and" \
                           " appears \n to be locked.")
                
        if Game.currentRoom == r7:
            #changes slot description
            if "red_key" in Game.inventory:
                r7.items["slot"] = ("The slot in the wall has the gem I placed" \
                                    " in \n it still.")
            #changes bucket description
            if "small_key" in Game.inventory:
                r7.items["upturned_bucket"] = ("It's just an upside down" \
                                               " bucket, it's not \n that" \
                                                   "interesting.")

    #enables dragon shooting abilities 
    def shoot(self):
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
            # When this changes, the status of the character can be \
            #printed again
            self.dragonDead = True
            return "He's dead! Well that was exciting"
        elif self.shots > 6:
            return "He's already dead, you psychopath"           

######################################################################
#                          START THE GAME!!!                         #
######################################################################

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