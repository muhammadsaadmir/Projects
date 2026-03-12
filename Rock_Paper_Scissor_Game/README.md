# Rock Paper Scissors Game 

This is a simple command-line Rock Paper Scissors game written in Python.
The user plays against the computer by choosing **Rock, Paper, or Scissors**, and the computer randomly selects its move.

The program then compares both choices and determines the winner.

This project is useful for practicing **conditional logic, lists, user input, and the random module in Python**.

---

## How the Game Works

1. The player selects an option:

   * `0` for Rock
   * `2` for Scissors

2. The computer randomly chooses one of the three options.

3. The program displays both choices using ASCII art.

4. The winner is determined based on the classic game rules.

---

## Game Rules

| Player Choice | Computer Choice | Result       |
| ------------- | --------------- | ------------ |
| Rock          | Scissors        | Player Wins  |
| Rock          | Paper           | Player Loses |
| Paper         | Rock            | Player Wins  |
| Paper         | Scissors        | Player Loses |
| Scissors      | Paper           | Player Wins  |
| Scissors      | Rock            | Player Loses |
| Same Choice   | Same Choice     | Draw         |

---

## Example

```
Welcome to the Rock Paper Scissor Game
Press 0 for Rock, 1 for Paper, 2 for Scissor
1

Computer chose
0

You Win!
```

The game also displays visual ASCII art for each choice.

---

## How to Run

1. Run the program:

```
python rock_paper_scissors.py
```

2. Enter a number when prompted to make your move.

---

## Concepts Used

This project demonstrates several Python fundamentals:

* lists
* conditional statements (`if / elif / else`)
* random number generation (`random.randint`)
* user input handling
* ASCII art display
* program termination using `sys.exit()`