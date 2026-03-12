# Python Password Generator 

This is a simple Python program that generates a random password based on user preferences.
The user can choose how many **letters**, **numbers**, and **symbols** they want in the password, and the program will generate a randomized password using those choices.

This project is a beginner-friendly way to practice working with **lists, loops, and the random module in Python**.

---

## Features

* Custom password length
* Choose number of letters, numbers, and symbols
* Randomized password order
* Simple command-line interaction

---

## How It Works

1. The program asks the user how many:

   * letters
   * numbers
   * symbols
     should be included in the password.

2. Random characters are selected from predefined lists.

3. All selected characters are stored in a list.

4. The list is shuffled to randomize the order.

5. The final password is created and displayed.

---

## Example

```
Welcome to Password Generator
How many letters would you like to generate? 5
How many numbers would you like to generate? 2
How many symbols would you like to generate? 2

Your generated password is: aB@7dT3!f
```

---

## How to Run

1. Run the program:

```
python password_generator.py
```

2. Follow the instructions in the terminal.

---

## Concepts Used

This project demonstrates several important Python concepts:

* `random.choice()` for selecting random characters
* `random.shuffle()` for randomizing order
* lists for storing characters
* loops (`for`)
* user input with `input()`
* string creation using concatenation
