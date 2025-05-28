import json
import pandas as pd
from datetime import datetime
from pathlib import Path

from main.models import Student
from tuzilma.models import Group, Direction
from .scenario import get_text
from loader import orm_async

BASE_DIR = Path(__file__).resolve().parent
folder_path = BASE_DIR.parent.parent / "files/schedules"

def data_cleaner(val):
    return "❗️" if str(val).lower() == "nan" else val

def format_schedule(schedule_data):

    lesson_times = {
        1: "08:30 – 09:50",
        2: "10:00 – 11:20",
        3: "11:30 – 12:50",
        4: "13:30 – 14:50",
        5: "15:00 – 16:20",
        6: "16:30 – 17:50",
    }

    formatted_lessons = []

    for lesson in schedule_data:
        hour = int(lesson.get("Lesson Hour", 0))
        time = lesson_times.get(hour, "Vaqt noma'lum")
        subject = data_cleaner(lesson.get("Subject"))
        lesson_type = data_cleaner(lesson.get("Lesson Type"))
        teacher = data_cleaner(lesson.get("Teacher"))
        room = data_cleaner(lesson.get("Room"))

        formatted = (
            f"⏱️ {time}️\n"
            f"📚 {subject}\n"
            f"🧪 {lesson_type}\n"
            f"📍: {room}\n"
            f"👨‍🏫: {teacher}"
        )

        formatted_lessons.append(formatted)

    return "\n\n".join(formatted_lessons)

async def get_schedule(user_id, weekday_number):
    student = await orm_async(Student.objects.get, telegram_id=user_id)
    lang = student.language
    group_exists = await orm_async(Group.objects.filter(id=student.group).exists)
    if group_exists:
        group = await orm_async(Group.objects.filter(name=student.group).last)
        direction = await orm_async(Direction.objects.get, pk=group.direction_id)
        file_path = folder_path / f"{direction.name}_{group.course}_jadval.xlsx"
    else:
        file_path = folder_path / f"{student.direction}_{student.course}_jadval.xlsx"
    day = get_text('uz', 'weekdays')[weekday_number]
    try:
        df = pd.read_excel(file_path)

        groups = {}
        for col in range(2, len(df.columns), 4):
            group_name = df.iloc[1, col]
            if pd.isna(group_name):
                break
            groups[group_name] = [col, col + 1, col + 2, col + 3]

        if group not in groups:
            result = get_text(lang, "schedule-not-found")
        else:
            ustunlar = groups[group]

            days = {
                "Dushanba": range(4, 10),
                "Seshanba": range(10, 16),
                "Chorshanba": range(16, 22),
                "Payshanba": range(22, 28),
                "Juma": range(28, 34),
                "Shanba": range(34, 40)
            }

            qatorlar = days[day]

            jadval = df.iloc[qatorlar, [0, 1] + ustunlar].copy()
            jadval.columns = ["Day", "Lesson Hour", "Subject", "Lesson Type", "Teacher", "Room"]

            jadval = jadval.dropna(subset=["Subject"])

            jadval = jadval.sort_values(by="Lesson Hour")

            if jadval.empty:
                result = get_text(lang, "schedule-not-found")
            else:
                jadval = jadval.drop(columns=["Day"])
                jadval_dict = jadval.to_dict(orient="records")
                result = (f"👥 {group}\n"
                          f"📆 {datetime.today().strftime('%d.%m.%Y')} | {get_text(lang, 'weekdays')[weekday_number]}\n\n"
                          f"{format_schedule(schedule_data=jadval_dict)}")

                return result

    except Exception as e:
        result = get_text(lang, "error-occured")

    return result

