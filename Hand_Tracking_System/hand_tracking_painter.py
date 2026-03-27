import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector


# -----------------------------
# Config
# -----------------------------
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
BRUSH_THICKNESS = 12
ERASER_THICKNESS = 50

# Colors (BGR)
COLOR_BLUE = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

current_color = COLOR_BLUE
draw_color = current_color

# Toolbar button positions
# x1, y1, x2, y2
buttons = {
    "Blue": (20, 20, 170, 90),
    "Green": (190, 20, 340, 90),
    "Red": (360, 20, 510, 90),
    "Eraser": (530, 20, 700, 90),
    "Clear": (720, 20, 890, 90),
}

# -----------------------------
# Setup
# -----------------------------
cap = cv2.VideoCapture(0)
cap.set(3, CAMERA_WIDTH)
cap.set(4, CAMERA_HEIGHT)

detector = HandDetector(detectionCon=0.8, maxHands=1)

xp, yp = 0, 0
canvas = np.zeros((CAMERA_HEIGHT, CAMERA_WIDTH, 3), np.uint8)


# -----------------------------
# UI Helpers
# -----------------------------
def draw_toolbar(img, active_name=""):
    for name, (x1, y1, x2, y2) in buttons.items():
        if name == "Blue":
            color = COLOR_BLUE
        elif name == "Green":
            color = COLOR_GREEN
        elif name == "Red":
            color = COLOR_RED
        elif name == "Eraser":
            color = (60, 60, 60)
        else:
            color = (180, 180, 180)

        thickness = -1
        cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)

        if active_name == name:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 4)
        else:
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), 2)

        text_color = (255, 255, 255) if name != "Clear" else (0, 0, 0)
        cv2.putText(
            img,
            name,
            (x1 + 15, y1 + 45),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            text_color,
            2,
        )


def get_selected_button(x, y):
    for name, (x1, y1, x2, y2) in buttons.items():
        if x1 <= x <= x2 and y1 <= y <= y2:
            return name
    return None


def apply_tool(name):
    global current_color, draw_color, canvas
    if name == "Blue":
        current_color = COLOR_BLUE
        draw_color = current_color
    elif name == "Green":
        current_color = COLOR_GREEN
        draw_color = current_color
    elif name == "Red":
        current_color = COLOR_RED
        draw_color = current_color
    elif name == "Eraser":
        draw_color = COLOR_BLACK
    elif name == "Clear":
        canvas[:] = 0


# -----------------------------
# Main Loop
# -----------------------------
while True:
    success, img = cap.read()
    if not success:
        print("Failed to read from camera.")
        break

    img = cv2.flip(img, 1)

    hands, img = detector.findHands(img, flipType=False)

    active_button = ""

    if hands:
        hand = hands[0]
        lmList = hand["lmList"]

        x1, y1 = lmList[8][0], lmList[8][1]   # index fingertip
        x2, y2 = lmList[12][0], lmList[12][1] # middle fingertip

        fingers = detector.fingersUp(hand)

        # Selection Mode: index + middle fingers up
        if fingers[1] and fingers[2]:
            xp, yp = 0, 0

            cv2.rectangle(img, (x1, y1 - 20), (x2, y2 + 20), (255, 255, 255), cv2.FILLED)

            selected = get_selected_button(x1, y1)
            if selected:
                active_button = selected
                apply_tool(selected)

        # Draw Mode: only index finger up
        elif fingers[1] and not fingers[2]:
            cv2.circle(img, (x1, y1), 10, draw_color if draw_color != COLOR_BLACK else (255, 255, 255), cv2.FILLED)

            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            thickness = ERASER_THICKNESS if draw_color == COLOR_BLACK else BRUSH_THICKNESS

            cv2.line(img, (xp, yp), (x1, y1), draw_color, thickness)
            cv2.line(canvas, (xp, yp), (x1, y1), draw_color, thickness)

            xp, yp = x1, y1

        else:
            xp, yp = 0, 0

    else:
        xp, yp = 0, 0

    # Convert canvas to overlay properly
    gray_canvas = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, img_inv = cv2.threshold(gray_canvas, 20, 255, cv2.THRESH_BINARY_INV)
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

    img = cv2.bitwise_and(img, img_inv)
    img = cv2.bitwise_or(img, canvas)

    # Draw toolbar
    current_tool_name = ""
    if draw_color == COLOR_BLACK:
        current_tool_name = "Eraser"
    elif draw_color == COLOR_BLUE:
        current_tool_name = "Blue"
    elif draw_color == COLOR_GREEN:
        current_tool_name = "Green"
    elif draw_color == COLOR_RED:
        current_tool_name = "Red"

    draw_toolbar(img, active_button or current_tool_name)

    # Title
    cv2.putText(
        img,
        "Hand Tracking Painter",
        (930, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (255, 255, 255),
        2,
    )

    cv2.imshow("Hand Tracking Painter", img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break

cap.release()
cv2.destroyAllWindows()