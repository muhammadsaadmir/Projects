print("PyCalculator")
cal= int(input("Press 1 for Addition\nPress 2 for Subtraction\nPress 3 for Multiplication\nPress 4 for Division\n"))

def addition():
   a = int(input("Enter a number: "))
   b = int(input("Enter another number: "))
   sum = a + b
   print(sum)

def subtraction():
    a = int(input("Enter a number: "))
    b = int(input("Enter another number: "))
    sum = a - b
    print(sum)

def multiplication():
    a = int(input("Enter a number: "))
    b = int(input("Enter another number: "))
    sum = a * b
    print(sum)

def division():
    a = float(input("Enter a number: "))
    b = float(input("Enter another number: "))
    sum = a / b
    print(sum)

if cal == 1:
    addition()
elif cal == 2:
    subtraction()
elif cal == 3:
    multiplication()
elif cal == 4:
    division()
else:
    print("Invalid input")