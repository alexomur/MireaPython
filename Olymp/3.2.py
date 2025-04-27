import json
import re
from typing import List, Optional


def main(table: List[List[Optional[str]]]) -> List[List[str]]:
    if not table:
        return []
    s = json.dumps(table, ensure_ascii=False).replace('null', '""')
    s = re.sub(
        r'"(\d{2})/(\d{2})/(\d{2})"',
        lambda m: f'"{m.group(3)}.{m.group(2)}.{m.group(1)}"',
        s
    )
    s = s.replace('"Да"', '"да"').replace('"Нет"', '"нет"')
    s = re.sub(r'"(\w+),[^"]+"', r'"\1"', s)
    s = re.sub(
        r'"(-?\d+\.\d+)"',
        lambda m: f'"{int(round(float(m.group(1))))}"',
        s
    )
    loaded = json.loads(s)
    rows = list(dict.fromkeys(
        tuple(r) for r in loaded if any(r)
    ))
    cols = list(dict.fromkeys(zip(*rows)))
    return [list(c) for c in cols]
