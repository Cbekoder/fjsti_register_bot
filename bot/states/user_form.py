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
    phone = State()


class RequestForm(StatesGroup):
    to_service = State()
    description = State()
    file = State()
    confirmation = State()


class ProfileUpdate(StatesGroup):
    updatable = State()
    value = State()


class ScheduleState(StatesGroup):
    get_day = State()