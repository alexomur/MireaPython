OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}

def not_implemented(*args, **kwargs):
    raise RuntimeError('Not implemented!')

LIB = {
    '+': not_implemented,
    '-': not_implemented,
    '*': not_implemented,
    '/': not_implemented, # Целочисленный вариант деления
    '%': not_implemented,
    '&': not_implemented,
    '|': not_implemented,
    '^': not_implemented,
    '<': not_implemented,
    '>': not_implemented,
    '=': not_implemented,
    '<<': not_implemented,
    '>>': not_implemented,
    'if': not_implemented,
    'for': not_implemented,
    '.': not_implemented
}


# Список имен библиотечных операций в порядке добавления в словарь.
LIB_KEYS = list(LIB.keys())


def disasm(bytecode):
    lines = []

    entry = bytecode[0]
    lines.append("entry:")

    for cmd in bytecode[1:]:
        op_code = cmd & 0b111        # последние 3 бита
        arg = cmd >> 3               # старшие 29 бит

        op_name = OP_NAMES.get(op_code, f"UNKNOWN({op_code})")
        if op_name == 'op':
            if arg < len(LIB_KEYS):
                op_arg = f"'{LIB_KEYS[arg]}'"
            else:
                op_arg = f"UNKNOWN_OP({arg})"
            line = f"  {op_name} {op_arg}"
        else:
            line = f"  {op_name} {arg}"
        lines.append(line)

    return "\n".join(lines)


if __name__ == '__main__':
    #      disasm([0, 16,       16,       1,       121,        5])
    sample_code = [0, 0b10_000, 0b10_000, 0b0_001, 0b1111_001, 0b0_101]
    print(disasm(sample_code))
