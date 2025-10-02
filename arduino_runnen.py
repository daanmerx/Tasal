import serial
import time

# Initialiseer Arduino
arduino = serial.Serial('COM5', 9600, timeout=1)
arduino.flush()
time.sleep(2)  # Wacht tot Arduino klaar is

# Posities bijhouden
pos_x = 0
pos_y = 0

def move(cmd):
    """Verstuur een simpele beweging naar Arduino"""
    arduino.write(cmd.encode())
    time.sleep(0.01)

def move_to(x_target, y_target):
    """Beweeg naar absolute positie"""
    global pos_x, pos_y

    while pos_x < x_target:
        move('X')
        pos_x += 1
    while pos_y > y_target:
        move('y')
        pos_y -= 1
    while pos_x > x_target:
        move('x')
        pos_x -= 1
    while pos_y < y_target:
        move('Y')
        pos_y += 1

def move_wells(cmd, steps=1, after_move=None):
    """
    Beweeg een aantal stappen en voer na elke beweging een callback uit
    after_move: functie die wordt uitgevoerd na elke DONE van Arduino
    """
    global pos_x, pos_y
    for _ in range(steps):
        arduino.write(cmd.encode())
        while True:
            if arduino.in_waiting > 0:
                msg = arduino.readline().decode().strip()
                if msg == "DONE":
                    break
        # Posities bijhouden
        if cmd == 'X':
            pos_x += 1
        elif cmd == 'x':
            pos_x -= 1
        elif cmd == 'Y':
            pos_y += 1
        elif cmd == 'y':
            pos_y -= 1

        # Foto maken na elke move
    if after_move is not None:
        after_move()

    time.sleep(2)

def run_sequence(after_move=None):
    """Voer het volledige rondje uit"""
    # Voorbeeld: beweeg X 6 keer vooruit
    move_wells('X', 0, after_move=after_move)

    for _ in range(5):
        move_wells('x', 195, after_move=after_move)

    # Beweeg Y 1 keer vooruit
    move_wells('Y', 195, after_move=after_move)

    # Beweeg X 6 keer achteruit
    for _ in range(5):
        move_wells('X', 195, after_move=after_move)

    # Beweeg Y 1 keer achteruit
    move_wells('Y', 195, after_move=after_move)

    for _ in range(5):
        move_wells('x', 195, after_move=after_move)

    move_wells('Y', 195, after_move=after_move)

    for _ in range(5):
        move_wells('X', 195, after_move=after_move)
    # Terug naar start
    move_to(0, 0)

def close():
    arduino.close()