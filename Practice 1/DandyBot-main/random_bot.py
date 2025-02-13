import random
from AIArchive import *


def script(check, x, y):
    return v1(check, x, y)
    if check("gold", x, y):
        return "take"
    return random.choice(["pass", "left", "right", "up", "down"])
