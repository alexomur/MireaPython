def draw_graph(check, x, y) -> None:
    pass

def level1(check, x, y):
    if check("wall", x+2, y):
        return "down"
    return "right"

def level2(check, x, y):
    if check("wall", x, y-1):
        return "right"
    if (check("wall", x+2, y) or check("wall", x+1, y)) or check("wall", x, y-2):
        return "up"
    else:
        return "right"

def script(check, x, y):
    if check("gold", x, y):
        return "take"

    if check("level") == 1:
        return level1(check, x, y)
    if check("level") == 2:
        return level2(check, x, y)
    return "pass"
