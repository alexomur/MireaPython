import random


def script(check, x, y):
    return "pass"
    if check("gold", x, y):
        return "take"
    return random.choice(["pass", "left", "right", "up", "down"])
