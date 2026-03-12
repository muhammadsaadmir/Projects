# Python Rollercoaster 

This is a simple Python program that simulates buying a ticket for a rollercoaster ride.
The program checks if the user is tall enough to ride, determines the ticket price based on age, and allows the user to add an optional photo.

This project is useful for practicing **nested conditional statements, user input, and simple price calculations in Python**.

---

## How It Works

1. The program asks the user for their **height**.
2. If the user is **120 cm or taller**, they are allowed to ride.
3. The ticket price is then determined based on the user's **age**.
4. The user can choose to add a **ride photo** for an additional cost.
5. The program calculates and displays the **final bill**.

---

## Ticket Prices

| Age Group           | Price |
| ------------------- | ----- |
| 12 years or younger | $4    |
| 13–18 years         | $8    |
| 19+ years           | $12   |

### Optional Add-on

| Add-on     | Price |
| ---------- | ----- |
| Ride Photo | +$3   |

---

## Example

```
Welcome to Py's Rollercoaster
what is your height in cm: 150
what is your age: 20
Adult ticket is $12
Do you want a photo taken? Y or N? Y
Your total bill is 15
```

If the user is not tall enough:

```
Welcome to Py's Rollercoaster
what is your height in cm: 100
You need to grow taller to ride this
```

---

## How to Run

1. Run the program:

```
python_rollercoaster.py
```

2. Follow the instructions shown in the terminal.
