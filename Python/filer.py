import csv
from typing import Dict, Generator, Iterable, List, Optional, Union, Tuple
import json
import re

def export_csv():
    pass

Diapazon = Tuple[int, int]

# берет определенные строки из файла
def multy_slice(data: Iterable, diapazons: Tuple[Diapazon]) -> Generator:
    index = 0
    ranges = [range(*d) for d in diapazons]
    while True:
        try:
            value = next(data)
            if any(((index in i) for i in ranges)):
                yield value
            index += 1
        except StopIteration:
            return

# это читает из файла без модуля csv
def pure_python_reader(file: str, delimiter: str = ',') -> Generator:
    with open(file, 'r') as f:
        for line in f:
            row = line.strip().split(delimiter)
            yield row

# это читает с модулем csv
def csv_reader(file: str, delimiter: str = ',') -> Generator:
    with open(file, 'r') as f:
        reader = csv.reader(f, delimiter=delimiter)
        yield from reader

# берет определенные колонки из файла
def slice_colums(data: Iterable, colum_numbers: List[int]) -> Generator:
    return ([v for i, v in enumerate(row) if i in colum_numbers] for row in data)

# фильтрует регекспом по определенным колонкам или по всем если не передать номер колонок
def filter_by_regex(data: Iterable, regex: str, colum: Optional[int] = None) -> Generator:
    def mathes_regex(row: List, regex: str, colum: Optional[int]):
        if colum:
            row = [row[colum]]
        return any((re.match(regex, d) for d in row))
    return (r for r in data if mathes_regex(r, regex, colum))


def cast_to_types(data: Iterable, colum_types: Dict) -> Generator:
    def cast_row_to_type(row: List, colum_types: Dict):
        return [colum_types.get(i, str)(v) for i, v in enumerate(row)]
    return (cast_row_to_type(r, colum_types) for r in data)


ff = 'test.csv'


# reader = csv_reader(ff)
reader = pure_python_reader(ff)

# берем определенные колонки
reader = slice_colums(reader, [1, 2])

# достаем заголовок
header = next(reader)


# берем определенные строки
reader = multy_slice(
    reader, 
    (
        (0,2), (4,6), (8, 12)
    )
)
# фильтруем регекспом
reader = filter_by_regex(reader, r'3\d*', 1)

# кастим колонки к типам
reader = cast_to_types(reader, {1: int})

# сортируем по колонке
data = sorted(list(reader), key=lambda o: o[1])

print(data)

data = [dict(zip(header, v)) for v in data]
with open('test.json', 'w') as f:
    f.writelines(json.dumps(data, indent=4))