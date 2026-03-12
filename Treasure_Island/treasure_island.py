import sys
print('''*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"""-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/]
*******************************************************************************''')
print("Welcome to the Treasure Island")
print("Your mission is to find the treasure.")
print("You are at a deserted forest, where do you want to go?")
choice = input("You want to go left or right? Be very careful the forest is full of traps and dangerous animals\nRemeber this if any wrong key pressed 'GameOver'\nChoose left or right?\n")
if choice == "left":
    print("You choose the correct path now head straight")
elif choice == "right":
    print("You choose the wrong path and got killed by the beast\nGameOver")
    sys.exit()
else:
    print("What did I tell you about pressing the wrong key!\nBe Gone!")
    sys.exit()

s = input("Press the S key to head straight but be careful!\n").upper()
if s == "S":
    print("Heading straight.....")
else:
    print("Invalid key pressed....How can you be this stupid\n Buzz off!")
    sys.exit()
print("You came across a lake. There is something there but I can't see it's too far.\nCheck your bag you might find an object to see!")
bag = input("Press B to search your bag\n").upper()
if bag == "B":
    print("Searching.....\n I have something, I got it.....\nLook it's Binoculars, this will help me see clearly.")
else:
    print("Oops you did it again got beaten up by this game now\nBe Gone!")
    sys.exit()
print("There is an Island it must be where the treasure is but how do I get there\nLooks around....\nThere is a boat we can use that or If you are feeling the adrenaline I can swim there too!")
choice_2 = input("Press A to use the boat or Press D to swim to the Island\n").upper()
if choice_2 == "A":
    print("Hopped onto the boat......Cruising to the Island")
elif choice_2 == "D":
    print("You were stupid enough to not take the boat and swim,\nWhat an idoit\nYou know what happened to you,\nYou got eaten by the shark!\n'GameOver")
    sys.exit()
else:
    print("You have press an Invalid key, You know what that means\nBe gone!!!!")
    sys.exit()
print("Something is hitting the boat....What Sharks!!!!")
import sys

fire = input("Hurry! Press F to use the gun to fire the sharks\n").upper()

if fire == "F":
    fire = input("Press one more time\n").upper()

    if fire == "F":
        fire = input("Only one left! Press F to kill the last one.\n").upper()

        if fire == "F":
            print("You killed the sharks!")
        else:
            print("You missed the last one!")
    else:
        print("You missed the second shot!")
else:
    print("You dumbass you did it again!\nBe gone!!!!")
    sys.exit()
print("You reached the Island....Look there's the treasure chest go to it")
walk = input("Press W to walk to it\n").upper()
if walk == "W":
    print("walking....The treasure chest it's so rusty\nLet's try opening it but there's a lock\nCheck your bag you may find something to break the lock.")
bag = input("Press B to search your bag\n").upper()
if bag == "B":
    print("A hammer I can use this to break the lock")
else:
        print("Wrong key again...It must be sad you come this far just gto exit\nBe gone!!!!")
        sys.exit()

hammer = input("Press H to use the hammer to break the lock\n").upper()
if hammer == "H":
    hammer = input("Hit it hard. You need to press one more time,\n").upper()
    if hammer == "H":
        print("You broke the lock")
    else:
        print("You needed only one more time to hit the lock")
else:
    print("I cannot even say no more....Just leave\nBe gone!!!!")
    sys.exit()
print("You found the treasure.\n I did not tell you the main choice is still yet remaining you did not win still\nOnly the player with the righteous heart will win.")
final_choice = input("Will you donate 50 percent of the treasure to the charity\n Press Y to say Yes or Press N to say No\n").upper()
if final_choice == "Y":
    print("See I told you the righteous heart will win\nCongrats YOU WON!!!!")
    sys.exit()
elif final_choice == "N":
    print("Not gonna give any funds to charity....You don't even deserve to win.....Be gone!!!! ")
    sys.exit()
else:
    print("Please Nooo....Who presses the wrong key at this moment....Be gone!!!! ")
    sys.exit()