print("Welcome to the bill calculator!")
bill = float(input("What was the bill? $"))
tip = float(input("What was the tip percentage? 10, 12 or 15 "))
split = int(input("How many people to split the bill? "))

total = (bill * (tip / 100 + 1)) / split
print(f"Each person should pay: ${round(total, 2)}")