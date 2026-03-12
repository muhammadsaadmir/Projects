import sys
print("Welcome to Python Cinema")
ticket = 0
movie = input("Which movie do you want to watch\nSpiderman 4\nDragonball Super\nInception\n").upper()
if movie not in ("SPIDERMAN 4","DRAGONBALL SUPER", "INCEPTION"):
    print("Invalid selection")
    sys.exit()
if movie == "SPIDERMAN 4":
    ticket = 16
    age = int(input("What is your age? "))
    if 18<= age <=24:
        print(f"The ticket is {ticket}")
    else:
        print("Sorry, you must be between 18 and 24 years old to watch this movie.")
        sys.exit()

elif movie == "DRAGONBALL SUPER":
    ticket = 18
    print(f"The ticket is {ticket}")

elif movie == "INCEPTION":
     ticket = 16
     age = int(input("What is your age? "))
     if age >=18:
         print(f"The ticket is {ticket}")
     else:
         print("You are too young")
         sys.exit()
else:
    print("Invalid selection")

popcorn = input("Do you want popcorn? Y/N ").upper()
if popcorn == "Y":
       ticket +=3

drink = input("Do you want drink? Y/N ").upper()
if drink == "Y":
    ticket +=1

print(f"Your total bill is {ticket} ")
