from typing import List
import matplotlib.pyplot as plt


PAIRS = ("..LEXEGEZACEBISO"
         "USESARMAINDIREA."
         "ERATENBERALAVETI"
         "EDORQUANTEISRION")

SEED = (0x5A4A, 0x0248, 0xB753)


def strip_dots(name: str) -> str:
    return name.replace('.', '')


class Seed:
    def __init__(self, w0: int, w1: int, w2: int):
        self.w0 = w0 & 0xFFFF  # сохраняем размерность
        self.w1 = w1 & 0xFFFF  # 2 байта
        self.w2 = w2 & 0xFFFF

    def tweakseed(self):
        temp = (self.w0 + self.w1 + self.w2) & 0xFFFF
        self.w0, self.w1, self.w2 = self.w1, self.w2, temp

class GoatSoupSeed:
    def __init__(self, a = 0, b = 0, c = 0, d = 0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d

class PlanetarySystem:
    def __init__(self):
        self.x = 0
        self.y = 0  # byte unsigned
        self.economy = 0  # 0-7
        self.govtype = 0  # 0-7
        self.techlev = 0  # 0-16
        self.population = 0  # byte
        self.productivity = 0  # 2 byte
        self.radius = 0  # 2 byte, not used
        self.goatsoupseed: GoatSoupSeed = GoatSoupSeed()
        self.name = ""  # По хорошему 12 символов


def make_system(seed: Seed) -> PlanetarySystem:
    # TODO: PBI23154 Refactor Code to meet company coding practices
    system = PlanetarySystem()
    system.x = seed.w1 >> 8
    system.y = seed.w0 >> 8

    system.govtype = (seed.w1 >> 3) & 7
    system.economy = (seed.w0 >> 8) & 7

    if system.govtype <= 1:
        system.economy |= 2

    system.techlev = ((seed.w1 >> 8) & 3) + (system.economy ^ 7)
    system.techlev += (system.govtype >> 1)

    if (system.govtype & 1) == 1:  # <= 1
        system.techlev += 1

    system.population = 4 * system.techlev + system.economy + system.govtype + 1
    system.productivity = (((system.economy ^ 7) + 3) * (system.govtype + 4)) * system.population * 8
    system.radius = 256 * (((seed.w2 >> 8) & 15) + 11) + system.x

    system.goatsoupseed.a = seed.w1 & 0xFF  # 11111111
    system.goatsoupseed.b = seed.w1 >> 8  # 1000
    system.goatsoupseed.c = seed.w2 & 0xFF
    system.goatsoupseed.d = seed.w2 >> 8

    longnameflag = seed.w0 & 64  # 1000000

    name_chars = []
    for _ in range(3):
        pair_index = 2 * ((seed.w2 >> 8) & 31)
        seed.tweakseed()
        name_chars.append(PAIRS[pair_index:pair_index + 2])
    if longnameflag:
        pair_index = 2 * ((seed.w2 >> 8) & 31)
        seed.tweakseed()
        name_chars.append(PAIRS[pair_index:pair_index + 2])

    system.name = strip_dots(''.join(name_chars))
    return system


def generate_galaxy(seed: Seed, systems_count: int = 256) -> List:
    systems = []
    for _ in range(systems_count):
        system = make_system(seed)
        systems.append(system)
    return systems


def visualize_galaxy(systems: List):
    xs = [sys.x for sys in systems]
    ys = [sys.y for sys in systems]

    plt.figure(figsize=(32, 8))

    # Точки
    plt.scatter(xs, ys, c='white', edgecolors='black')
    # Имена
    for system in systems:
        plt.text(system.x, system.y - 2, system.name, fontsize=8, ha='center', va='top', color='#8888FF')

    plt.xlabel("X")
    plt.ylabel("Y")
    plt.gca().set_facecolor('black')
    plt.grid(True, color='gray', linestyle='--', alpha=0.5)
    plt.show()

def main():
    initial_seed = Seed(*SEED)

    galaxy = generate_galaxy(initial_seed, systems_count=256)

    for i, system in enumerate(galaxy[:5], start=1):
        print(f"[{i}] (x,y)=({system.x},{system.y}), name={system.name}, "
              f"TechLev={system.techlev}, Population={system.population}")

    visualize_galaxy(galaxy)

if __name__ == '__main__':
    main()
