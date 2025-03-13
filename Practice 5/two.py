import module
from module import GLOBAL_VAR
from one import one


def two():
    print(f"File 2.py | one()")
    print(f"{GLOBAL_VAR = }")
    print(f"{module.GLOBAL_VAR = }")

print(f"\n1")
one()
print(f"---")
two()
print(f"\n2")
GLOBAL_VAR = 30
one()
print(f"---")
two()
print(f"\n3")
module.GLOBAL_VAR = 55
one()
print(f"---")
two()
