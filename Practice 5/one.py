import module
from module import GLOBAL_VAR
import numpy

import ObjectParser

def one():
    print(f"File 1.py | one()")
    print(f"{GLOBAL_VAR = }")
    print(f"{module.GLOBAL_VAR = }")

ObjectParser.parser.Parser.save(numpy.zeros, "numpy.zeros.yml")