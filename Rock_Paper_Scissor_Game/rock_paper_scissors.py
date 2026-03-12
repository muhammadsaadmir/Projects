import sys
import random

Rock = ("""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""")

Paper = ("""
    _______
---'   ____)
      (_____)
      (_____)
      (____)
---.__(___)
""")

Scissor = ("""
    _______
---'   ____)____
          ______)
       __________)
      (____)
---.__(___)
""")

print ("Welcome to the Rock Paper Scissor Game")
choices = [Rock, Paper, Scissor]
user = int(input("Press 0 for Rock, 1 for Paper, 2 for Scissor\n"))
if user >=0 and user <=2:
    print(choices[user])
computer = random.randint(0,2)
print("Computer chose")
print(choices[computer])
if user >=3 or user <0:
    print("Invalid input")
    sys.exit()
elif user == 0 and computer == 2:
    print("You Win!")
    sys.exit()
elif computer == 0 and user == 2:
    print("You Lose")
    sys.exit()
elif user<computer:
    print("You Lose")
    sys.exit()
elif computer<user:
    print("You Win")
    sys.exit()
elif computer == user:
    print("Draw")
    sys.exit()
else:
    print("You Typed an Invalid Number You Lose")
    sys.exit()



