from aiogram.fsm.state import StatesGroup, State


class UserForm(StatesGroup):
    level = State()
    faculty = State()
    direction = State()
    course = State()
    group = State()
    first_name = State()
    last_name = State()
    middle_name = State()