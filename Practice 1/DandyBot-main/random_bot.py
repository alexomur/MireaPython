import random
from AIArchive import v1


def script(check, x, y):
    return v1.script(check, x, y)
    if check("gold", x, y):
        return "take"
    return random.choice(["pass", "left", "right", "up", "down"])
