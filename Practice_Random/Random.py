import random
from Practice_Random import my_module

random_integer = random.randint(1,100)
print(random_integer)
print(my_module.my_name)
random_number = random.random() * 100
print(random_number)
random_floating = random.uniform(1,100)
print(random_floating)

random_game = random.randint(0,1)
if random_game == 0:
    print("Heads")
else:
    print("Tails")