from __future__ import annotations

from datetime import datetime, date, timedelta
import random
import re
from typing import List, Dict, Any


def get_days_from_today(date_str: str) -> int:
    """
    Рахує різницю у днях між заданою датою (YYYY-MM-DD) та сьогоднішньою датою.
    Повертає ціле число: (today - given_date).days
    Якщо дата у майбутньому — результат від'ємний.
    Якщо формат некоректний — повертає 0.
    """
    try:
        given_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return 0

    today = datetime.today().date()
    return (today - given_date).days


def get_numbers_ticket(min: int, max: int, quantity: int) -> List[int]:
    """
    Генерує відсортований список унікальних випадкових чисел.
    Обмеження:
      - min >= 1
      - max <= 1000
      - min < max
      - quantity має бути в межах [1, max-min+1]
    Якщо параметри некоректні — повертає [].
    """
    if (
        not isinstance(min, int)
        or not isinstance(max, int)
        or not isinstance(quantity, int)
        or min < 1
        or max > 1000
        or min >= max
        or quantity < 1
        or quantity > (max - min + 1)
    ):
        return []

    numbers = random.sample(range(min, max + 1), quantity)
    return sorted(numbers)


def normalize_phone(phone_number: str) -> str:
    """
    Нормалізує телефон до формату:
      - тільки цифри та '+' на початку
      - якщо немає міжнародного коду:
          * якщо починається з 380... -> додаємо лише '+'
          * інакше -> додаємо '+38'
    """
    if phone_number is None:
        return "+38"

    raw = str(phone_number).strip()
    digits = re.sub(r"\D", "", raw)

    if raw.startswith("+"):
        return f"+{digits}"

    if digits.startswith("380"):
        return f"+{digits}"

    return f"+38{digits}"


def get_upcoming_birthdays(users: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Повертає список привітань на найближчі 7 днів включно з поточним днем.
    Вхід:
      users = [{"name": "...", "birthday": "YYYY.MM.DD"}, ...]
    Вихід:
      [{"name": "...", "congratulation_date": "YYYY.MM.DD"}, ...]
    Якщо день народження на вихідних — переносимо привітання на понеділок.
    """
    today = datetime.today().date()
    result: List[Dict[str, str]] = []

    for user in users:
        name = user.get("name")
        bday_str = user.get("birthday")

        if not name or not bday_str:
            continue

        try:
            bday = datetime.strptime(bday_str, "%Y.%m.%d").date()
        except ValueError:
            continue

        bday_this_year = date(today.year, bday.month, bday.day)
        if bday_this_year < today:
            bday_this_year = date(today.year + 1, bday.month, bday.day)

        delta_days = (bday_this_year - today).days

        if 0 <= delta_days <= 7:
            congrat_date = bday_this_year

            weekday = congrat_date.weekday()  
            if weekday == 5:  
                congrat_date += timedelta(days=2)
            elif weekday == 6:  
                congrat_date += timedelta(days=1)

            result.append(
                {
                    "name": name,
                    "congratulation_date": congrat_date.strftime("%Y.%m.%d"),
                }
            )

    result.sort(key=lambda x: x["congratulation_date"])
    return result










