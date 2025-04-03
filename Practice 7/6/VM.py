from typing import List


OP_NAMES = {0: 'push', 1: 'op', 2: 'call', 3: 'is', 4: 'to', 5: 'exit'}


def not_implemented(*args, **kwargs):
    raise RuntimeError('Not implemented!')

def op_add(vm):
    b = vm.stack.pop()
    a = vm.stack.pop()
    vm.stack.append(a + b)

def op_print(vm):
    value = vm.stack.pop()
    print(value)

LIB = {
    '+': op_add,
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
    '.': op_print
}

LIB_KEYS = list(LIB.keys())

class VM:
    def __init__(self, source_code: str):
        self.stack = []
        self.source_code: List[str] = source_code.split()
        self.byte_code: List[bin] = self.to_byte_code()

    def to_byte_code(self, source_code = None) -> List:
        source_code = source_code or self.source_code

        byte_code = [0]
        for command in source_code:
            # push
            if command.isdecimal():
                byte_code.append(int(command) << 3)
                continue

            # op
            try:
                arg = LIB_KEYS.index(command)
                byte_code.append(arg << 3 | 0b001)
                continue
            except Exception as e:
                print(e)

            raise AttributeError(f"Unknown symbol: {command}")

        # exit
        byte_code.append(5)

        return byte_code

    def run(self, byte_code = None) -> int:
        byte_code = byte_code or self.byte_code

        for command in byte_code:
            op = command & 0b111
            arg = command >> 3

            # exit
            if op == 5:
                if len(self.stack) > 0:
                    return self.stack.pop()
                return 0

            # push
            if op == 0:
                self.stack.append(arg)
                continue

            # op
            if op == 1:
                func_op = LIB[LIB_KEYS[arg]]
                func_op(self)
                continue

            raise AttributeError(f"Unknown command: {arg} : {op}")

        raise AttributeError("No exit code in byte code")


if __name__ == '__main__':
    vm = VM("2 2 + .") # Компиляция
    print(vm.source_code)
    print(vm.byte_code)

    vm.run() # Запуск