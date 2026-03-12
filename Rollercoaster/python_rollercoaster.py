print("Welcome to Python Rollercoaster")
height = int(input("what is your height in cm: "))
if height >= 120:
    age = int(input("what is your age: "))
    if age <= 12:
       bill = 4
       print("Child ticket is $4")
    elif age <=18:
       bill = 8
       print("Youth ticket is $8")
    else:
        bill = 12
        print("Adult ticket is $12")
    photos = input("Do you want a photo taken? Y or N? " )
    if photos == "Y".upper():
        bill += 3

    print(f"Your total bill is {bill}")

else:
     print("You need to grow taller to ride this")