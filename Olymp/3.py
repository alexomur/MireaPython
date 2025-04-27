import re
from typing import List, Optional, Tuple


def normalize_rows(
    table: List[List[Optional[str]]]
) -> List[List[Optional[str]]]:
    max_cols = max((len(r) for r in table), default=0)
    return [row + [None] * (max_cols - len(row)) for row in table]


def remove_duplicate_columns(
    table: List[List[Optional[str]]]
) -> List[List[Optional[str]]]:
    if not table:
        return []
    seen: set = set()
    keep_idxs: List[int] = []
    for j in range(len(table[0])):
        col = tuple(row[j] for row in table)
        if col not in seen:
            seen.add(col)
            keep_idxs.append(j)
    return [[row[j] for j in keep_idxs] for row in table]


def remove_empty_rows(
    table: List[List[Optional[str]]]
) -> List[List[Optional[str]]]:
    return [row for row in table if any(cell is not None for cell in row)]


def remove_duplicate_rows(
    table: List[List[Optional[str]]]
) -> List[List[Optional[str]]]:
    seen: set = set()
    unique: List[List[Optional[str]]] = []
    for row in table:
        key: Tuple[Optional[str], ...] = tuple(row)
        if key not in seen:
            seen.add(key)
            unique.append(row)
    return unique


def transform_cell(cell: Optional[str]) -> str:
    if cell is None:
        return ''
    if re.fullmatch(r'\d{2}/\d{2}/\d{2}', cell):
        d, m, y = cell.split('/')
        return f'{y}.{m}.{d}'
    low = cell.lower()
    if low in ('да', 'нет'):
        return low
    if ',' in cell:
        return cell.split(',', 1)[0]
    if re.fullmatch(r'-?\d+(?:\.\d+)?', cell):
        return str(int(round(float(cell))))
    return cell


def transform_cells(
    table: List[List[Optional[str]]]
) -> List[List[str]]:
    return [
        [transform_cell(cell) for cell in row]
        for row in table
    ]


def transpose(table: List[List[str]]) -> List[List[str]]:
    return [list(col) for col in zip(*table)]


def main(table: List[List[Optional[str]]]) -> List[List[str]]:
    if not table:
        return []

    step1 = normalize_rows(table)
    step2 = remove_duplicate_columns(step1)
    step3 = remove_empty_rows(step2)
    step4 = remove_duplicate_rows(step3)
    step5 = transform_cells(step4)
    return transpose(step5)
