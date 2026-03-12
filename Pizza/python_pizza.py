import sys
print("Welcome to Python Pizza")

pizza_size = input("What size pizza do you want? Small, Medium or Large? ").upper()

if pizza_size not in ["SMALL", "MEDIUM", "LARGE"]:
    print("Invalid pizza size")
    sys.exit()

pepperoni = input("Do you want pepperoni? Y/N ").upper()

if pepperoni not in ("Y", "N"):
    print("Invalid selection")
    sys.exit()

cheese = input("Do you want cheese? Y/N ").upper()
if cheese not in ("Y", "N"):
    print("Invalid selection")
    sys.exit()
if pizza_size == "SMALL":
    bill = 15
    if pepperoni == "Y":
        bill += 2
    if cheese == "Y":
       bill += 1
    print("Your bill is " + str(bill))
elif pizza_size == "MEDIUM":
    bill = 20
    if pepperoni == "Y":
        bill += 3
    if cheese == "Y":
            bill += 1
    print("Your bill is " + str(bill))
elif pizza_size == "LAEGE":
    bill = 25
    if pepperoni == "Y":
        bill += 3
    if cheese == "Y":
        bill += 1
    print(f"Your bill is {bill}" )
else:
    print("Sorry, I don't know what you are doing")
