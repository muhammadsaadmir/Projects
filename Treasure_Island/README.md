# Treasure Island Adventure Game

This is a text-based adventure game written in Python where the player goes on a journey to find a hidden treasure on a mysterious island. Along the way, the player must make decisions that determine whether they survive or lose the game.

The game uses user input and conditional logic to guide the player through different scenarios such as navigating through a forest, crossing a lake, avoiding sharks, and finally unlocking the treasure chest.

---

## Game Story

You start in a **dangerous forest** filled with traps and wild animals.
Your goal is to reach the **Treasure Island** and open the treasure chest.

However, many decisions stand between you and the treasure. One wrong move could end the game.

Even after finding the treasure, there is one final decision that determines if you truly win.

---

## Game Features

* Interactive text-based adventure
* Multiple decision points
* ASCII art introduction
* Different ways to lose the game
* A final moral decision that determines the true ending

---

## How the Game Works

Throughout the game, the player must press specific keys to continue:

| Action           | Key        |
| ---------------- | ---------- |
| Go Left          | `left`     |
| Go Straight      | `S`        |
| Search Bag       | `B`        |
| Use Boat         | `A`        |
| Shoot Sharks     | `F`        |
| Walk to Treasure | `W`        |
| Use Hammer       | `H`        |
| Final Choice     | `Y` or `N` |

Pressing the wrong key will usually result in **Game Over**.

---

## Example Gameplay

```
Welcome to the Treasure Island
Your mission is to find the treasure.

You are at a deserted forest.
Choose left or right?
left

Press S to head straight
S

Press B to search your bag
B

Press A to use the boat
A

Press F to fire at sharks
F
F
F

You reached the island and found the treasure!
```

The player must also make a final decision about the treasure.

---

## How to Run

1. Run the program:

```
python treasure_island.py
```

2. Follow the instructions displayed in the terminal.

---

## Concepts Used

This project demonstrates several Python fundamentals:

* user input with `input()`
* conditional logic (`if / elif / else`)
* string formatting
* ASCII art
* program termination with `sys.exit()`
* basic game flow control
