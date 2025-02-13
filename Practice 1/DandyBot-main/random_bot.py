import random
import user_bot


def script(check, x, y):
    return user_bot.script(check, x, y)
    if check("gold", x, y):
        return "take"
    return random.choice(["pass", "left", "right", "up", "down"])
