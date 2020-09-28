######################################################################
# Name:Mary deMarigny
# Date:07/20/2020
# Description: Text Based Game: Python 3.8
######################################################################
######################################################################

#I added to my game the following features:
    #item descriptions change when grabbables are picked up
    #there is an extra room, items, and grababble
    #the extra room contains a dragon and a hidden item that is not revealed until the dragon is killed
    #once the dragon is found, a countdown starts before the player is killed, and is only stopped by killing the dragon
    #there is a shooting mechanism that only works once the gun is obtained
    #there is a chest that can only be open once the key is obtained
    #there is a secret room that is revealed when the book is placed on the bookshelf
    

##### My additions are denoted with 5 pound signs at the beginning and end of the line #####

from time import time ##### imported so a timer can be set #####

class Room(object):
    
    def __init__(self, name): #the constructor 
        self.name = name
        self.exits = [] #Lists that are connected somehow are called "parallel lists"
        self.exitLocations = [] #The correlating indecies are connected in parallel lists.
        self.items = [] #Parallel Lists v
        self.itemDescriptions = [] #    ^
        self.grabbables = []
        
        
    @property                         #mutators and grabers
    def name(self):                   # |
        return self._name             # |
                                      # |
    @name.setter                      # |
    def name(self, value):            # |
        self._name = value            # |
                                      # |
    @property                         # |
    def exits(self):                  # |
        return self._exits            # |
                                      # |
    @exits.setter                     # |
    def exits(self, value):           # |
        self._exits = value           # |
                                      # |
    @property                         # |
    def exitLocations(self):          # |
        return self._exitLocations    # |
                                      # |
    @exitLocations.setter             # |
    def exitLocations(self, value):   # |
        self._exitLocations = value   # |
                                      # |
    @property                         # |
    def items(self):                  # |
        return self._items            # |
                                      # |
    @items.setter                     # |
    def items(self, value):           # |
        self._items = value           # |
                                      # |
    @property                         # |
    def itemDescriptions(self):       # |
        return self._itemDescriptions # |
                                      # |
    @itemDescriptions.setter          # |
    def itemDescriptions(self, value):# |
        self._itemDescriptions = value# |
                                      # |
    @property                         # |
    def grabbables(self):             # |
        return self._grabbables       # |
                                      # |
    @grabbables.setter                # |
    def grabbables(self, value):      # V
        self._grabbables = value      #___
        
#-------------------------------------------------------------------
        
    def addExit(self, exit, room): #Formal Parameters
        self._exits.append(exit)
        self._exitLocations.append(room)

    def addItem(self, item, desc):
        self._items.append(item)
        self._itemDescriptions.append(desc)
        
    def addGrabbable(self, item):
        self._grabbables.append(item)
        
    def delGrabbable(self, item):
        self._grabbables.remove(item)

    def __str__(self):
        s = "You are in {}.\n".format(self.name)
        s += "You see: "
        for item in self.items:
            s += item + " "
        s += "\n"
        s += "Exits: "
        for exit in self.exits:
            s += exit + " "
        return s
    
    #Exit Class

def createRooms():
    global currentRoom
    global r1 #### I made the room names global so I can use them in a different function. #####
    global r2
    global r3
    global r4
    global r5
    global r6

    r1 = Room("the livingroom") ##### I changed the name of the rooms just for fun #####
    r2 = Room("the bedroom")
    r3 = Room("the office")
    r4 = Room("the spare room")
    r5 = Room("the Dungeon") ##### I added a basement #####
    r6 = Room("the secret room") ##### A secret room behind the bookshelf #####
#---------------------------------
    r1.addExit("east", r2) # -> to the east of room 1 is room 2
    r1.addExit("south", r3) #<- Actual Parameters assigned to the Formal Parameters
    r1.addGrabbable("key")
    r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
    r1.addItem("table", "It is made of oak. A golden key rests on it.")
#---------------------------------
    r2.addExit("west", r1)
    r2.addExit("south", r4)
    r2.addGrabbable("gun")
    r2.addItem("closet", "There's just a dirty, old coat with a gun in the pocket") 
    r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
    r2.addItem("fireplace", "It is full of ashes.")
#---------------------------------
    r3.addExit("north", r1)
    r3.addExit("east", r4)
    r3.addGrabbable("book")
    r3.addItem("bookshelves", "They are empty. Go figure.")
    r3.addItem("statue", "There is nothing special about it.")
    r3.addItem("desk", "The statue is resting on it. So is a book.")
#---------------------------------
    r4.addExit("north", r2)
    r4.addExit("west", r3)
    r4.addExit("south", r5) 
    r4.addGrabbable("6-pack")
    r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. A 6-pack is resting beside it.")
#---------------------------------
    r5.addExit("north", r4)
    r5.addItem("dragon!!!", "Does it matter what it looks like?! Kill it!") ##### I added a dragon to the basement #####
#---------------------------------
    r6.addExit("east", r3)
    r6.addItem("safe", "It has a dial on it. I wonder what the code could be.") ##### I added a dragon to the basement #####
#---------------------------------
    currentRoom = r1


# ____Room Editor___________________
def roomEdit(): ##### This edits the description of items once a grabable is picked up #####
    if currentRoom == r1:
        if "key" in inventory:
            i = r1.itemDescriptions.index("It is made of oak. A golden key rests on it.")
            r1.itemDescriptions [i] = ("It is made of oak. Nothing is on it")
            
    if currentRoom == r2:
        if "gun" in inventory:
            i = r2.itemDescriptions.index("There's just a dirty, old coat with a gun in the pocket")
            r2.itemDescriptions [i] = ("There's just a dirty, old coat")
    
    if currentRoom == r3:
        if "book" in inventory:
            i = r3.itemDescriptions.index("The statue is resting on it. So is a book.")
            r3.itemDescriptions [i] = ("The statue is resting on it")
            
    if currentRoom == r4:
        if "6-pack" in inventory:
            i = r4.itemDescriptions.index( "Gourd is brewing some sort of oatmeal stout on the brew rig. A 6-pack is resting beside it.")
            r4.itemDescriptions [i] = ("Gourd is brewing some sort of oatmeal stout on the brew rig. Did you really take his beer?")

    if currentRoom == r5:
        if dragonDead == True:
            i = r5.itemDescriptions.index("Does it matter what it looks like?! Kill it!")
            r5.itemDescriptions [i] = ("Yup, that's a dead dragon, alright")
            r5.items [i] = "dead_dragon" ##### changes the name of the dragon once killed #####
            r5.addItem("chest", "It is very large and appears to be locked") ##### reveals a previously hidden item #####
            
        
#_____Shoot Enabler____________________
##### This makes it so we can shoot the dragon and get a response #####       
shots = 0  ##### Setting starting game variables #####
dragonDead = False
characterDead = False
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

    
# ____Death_Function___________________
    
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

# ____Dragon_Function___________________
        
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
    
# ____Chest_Function___________________
    
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
# START THE GAME!!!
######################################################################
        
inventory = [] 
createRooms()
game = "playing"

##### Intro #####
print ("Welcome! Have a look around, and you never know what you might find. Access your available options at any time by typing \"options\"")

while (True):
    if shots == 0 or dragonDead == True: ##### Adding this makes it so the room information is not printed after every shot is fired at the dragon #####
        status = "{}\nYou are carrying: {}\n".format(currentRoom, inventory)
        if game == "over": ##### Ends the game once the gold is found #####
            print ("You are carrying: {}".format(inventory))
            break #Exits the game
        print ("=========================================================")
        print (status)
    
    action = input("What to do? ")
    action = action.lower()
     
    if (characterDead == True): ##### Executed the death function when killed by dragon #####
        death()
        print ("You died")
        break
    
    response = ("I don't understand. Try verb noun.")
    
    if (action == "quit" or action == "exit" or action == "bye" or action == "end"): 
        response = "Quitting already? That's no fun. Goodbye" #### I added a string to display upon quitting. ####
        print (response)
        break
    
    if (action == "options"): ##### Allows the player to look at options at any time #####
        response = ("Your verb options are go, look, take, open, place, and shoot. \n Your noun options are {} {}".format(inventory, currentRoom.items))
    
    
    words = action.split()
    if (len(words) == 2):
        verb = words[0]
        noun = words[1]
        
        if (verb == "go"):
            response = "Invalid exit."
            for i in range(len(currentRoom.exits)):
                if (noun == currentRoom.exits[i]):
                    currentRoom = currentRoom.exitLocations[i]
                    response = "Room changed."
                    if currentRoom == r5 and dragonDead == False: ##### Prints the dragon #####
                        response = "A dragon is atatcking you! Shoot him!"
                        dragon()
                    break
                
        elif (verb == "look"):
            response = "I don't see that item."
            for i in range(len(currentRoom.items)):
                if (noun == currentRoom.items[i]):
                    response = currentRoom.itemDescriptions[i]
                    break
                
        elif (verb == "take" or verb == "grab"): ##### I added "grab" as a verb because that is what I naturally kept typing #####
            response = "I don't see that item."
            for grabbable in currentRoom.grabbables:
                if (noun == grabbable):
                    inventory.append(grabbable)
                    currentRoom.delGrabbable(grabbable)
                    response = "Item grabbed."
                    roomEdit() ##### Runs the function that changes the item descsriptions #####
                    break
                
        elif (verb == "open" or verb == "unlock"): ##### Opens the chest behind the dragon #####
            response = "I can't open that."
            if (currentRoom == r5) and (noun == "chest"):
                if ("key" in inventory):
                    inventory.append("infinite_wealth")
                    chest() ##### Prints the chest #####
                    response = "So... much... GOLD!!! \n You're rich!!!"
                    game = "over"
                    
        elif (verb == "place"): ##### A secret room is revealed when the book is placed on the bookshelf #####
            response = "Place it where? The ground?!"
            if (currentRoom == r3) and (noun == "book") and ("book" in inventory):
                inventory.remove("book")
                response = "The bookshelf swings back. A secret room appears!"
                r3.addExit("west", r6)
            if noun != "book":
                response = "You should keep that for now."
        
    elif (len(words) == 1): ##### This is so the player only has to type "shoot" and not "shoot gun". #####
        verb = words[0]
        
        if (verb == "shoot"):
            response = "Shoot with what? Finger guns?"
            if "gun" in inventory:
                response = "You put a hole in the wall. Why would you do that?"
            if currentRoom == r5 and "gun" in inventory:
                response = shoot()
            if dragonDead == True:
                roomEdit()
                           
    print ("\n{}".format(response))