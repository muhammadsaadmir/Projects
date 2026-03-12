import random
friend = ["Chelsey💍", "Umer", "Rishi", "Deven", "Chirag"]
print(random.choice(friend))

fruits = ["Strawberries", "Nectarines", "Apples", "Grapes", "Peaches", "Cherries", "Pears"]
print(fruits[-5])

random_number = random.randint(1,10)
user_guess = input("Pick a number")

guess = 0
while guess != random_number: