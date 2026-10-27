import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]:
    # Шаблон шукає числа з плаваючою крапкою, які відокремлені пробілами або межами рядка
    pattern = r'(?:^|\s)(\d+\.\d+)(?=$|\s)'
    for match in re.finditer(pattern, text):
        yield float(match.group(1))

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float:
    numbers_generator = func(text)
    return sum(numbers_generator)

text = """Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими 
надходженнями 27.45 і 324.00 доларів."""

total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")
