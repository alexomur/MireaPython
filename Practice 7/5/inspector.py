import inspect
import importlib.util
import sys

def generate_api_doc(module_path: str) -> str:
    spec = importlib.util.spec_from_file_location("module", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    lines = []

    module_name = module.__name__
    lines.append(f"# Модуль {module_name}\n")
    if module.__doc__:
        lines.append(module.__doc__.strip() + "\n")

    for name, cls in inspect.getmembers(module, inspect.isclass):
        lines.append(f"## Класс {name}\n")
        if cls.__doc__:
            lines.append(cls.__doc__.strip() + "\n")

        for meth_name, meth in inspect.getmembers(cls, predicate=inspect.isfunction):
            sig = str(inspect.signature(meth))
            lines.append(f"* **Метод** `{meth_name}{sig}`\n")
            if meth.__doc__:
                lines.append(meth.__doc__.strip() + "\n")

    for name, func in inspect.getmembers(module, inspect.isfunction):
        lines.append(f"## Функция {name}\n")
        sig = str(inspect.signature(func))
        lines.append(f"Сигнатура: `{name}{sig}`\n")
        if func.__doc__:
            lines.append(func.__doc__.strip() + "\n")

    return "\n".join(lines)


if __name__ == '__main__':
    module_path = "main.py"
    documentation = generate_api_doc(module_path)
    print(documentation)
