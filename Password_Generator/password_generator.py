import random

print("Welcome to Password Generator")
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ]
numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["@", "~", "!", "#", "$", "%", "^", "&", "*"]

nr_of_letters = int(input("How many letters would you like to generate? "))
nr_of_numbers = int(input("How many numbers would you like to generate? "))
nr_of_symbols = int(input("How many symbols would you like to generate? "))

password_list = []
for char in range(0, nr_of_letters):
    password_list.append(random.choice(letters))

for char in range(0, nr_of_numbers):
    password_list.append(random.choice(numbers))

for char in range(0, nr_of_symbols):
    password_list.append(random.choice(symbols))

random.shuffle(password_list)

password = ""
for char in password_list:
    password += char

print(f"Your generated password is: {password}")