import re
import difflib

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from django.core.cache import cache

from django.db.models import Q
from keyboards.inline.user_form import faculty_buttons, direction_buttons, course_buttons, group_buttons, level_buttons
from keyboards.default.menu_keyboard import menu_buttons, settings_buttons
from keyboards.default.common_buttons import phone_request_keyboard
from keyboards.inline.user_form import profile_buttons
from states.user_form import UserForm, ProfileUpdate
from data.scenario import get_text
from loader import dp, redis_cl, orm_async

from main.models import Student
from tuzilma.models import Group


@dp.callback_query(UserForm.level, F.data.startswith("level"))
async def process_level(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    level_key = callback_query.data.split("_")[1]
    await state.update_data(level=level_key)
    await callback_query.answer(f"You selected {level_key} level.")
    if level_key == 'bachelor':
        await callback_query.message.edit_text(get_text(lang, "enter-faculty"), reply_markup=faculty_buttons(lang))
        await state.set_state(UserForm.faculty)
    elif level_key == 'master':
        direction_list = [
            "obstetrics", "endocrinology", "hygiene",
            "cardiology", "morphology", "pathological-anatomy", "pediatrics_m",
            "radiology-technology", "healthcare-management",
            "therapy", "medical-biological-equipment",
            "general-oncology", "surgery"
        ]
        await callback_query.message.edit_text(get_text(lang, "enter-specialty"),
                                               reply_markup=direction_buttons(lang, direction_list))
        await state.update_data(faculty='master')
        await state.set_state(UserForm.direction)
    elif level_key == 'ordinatura':
        direction_list = [
            "obstetrics-gynecology", "allergy-clinical-immunology",
            "anesthesiology-reanimation", "pediatric-anesthesiology-reanimation",
            "pediatric-cardiorheumatology", "pediatric-nephrology",
            "pediatric-neurology", "pediatric-adolescent-gynecology",
            "pediatric-surgery", "dermatovenereology",
            "epidemiology", "phthisiatry", "hematology-transfusiology",
            "internal-diseases-therapy", "hygiene", "communal-hygiene",
            "occupational-hygiene", "narcology", "nephrology", "cardiology",
            "nephrology-hemodialysis", "neonatology", "neurology",
            "neurosurgery", "nutrition", "ophthalmology", "endocrinology",
            "psychiatry", "pulmonology", "rheumatology", "laboratory-work",
            "dentistry-therapeutic", "medical-psychology", "medical-radiology",
            "traumatology-orthopedics", "infectious-diseases", "maxillofacial-surgery",
            "pathological-anatomy", "otorhinolaryngology", "pediatrics_m", "dentistry",
            "therapy", "general-oncology", "general-surgery", "urology",
        ]
        await callback_query.message.edit_text(get_text(lang, "enter-specialty"), reply_markup=direction_buttons(lang, direction_list))
        await state.update_data(faculty='master')
        await state.set_state(UserForm.direction)


# Faculty handler
@dp.callback_query(UserForm.faculty, F.data.startswith("faculty_"))
async def process_faculty(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    faculty_key = callback_query.data.split("_")[1]
    await callback_query.answer(f"You selected {faculty_key} faculty.")
    await state.update_data(faculty=faculty_key)
    global direction_list
    match faculty_key:
        case "general-medicine":
            direction_list = ["general-medicine"]
        case "pediatrics":
            direction_list = ["dentistry", "pharmacy", "pediatrics"]
        case "medical-prevention":
            direction_list = ["biomedical-engineering", "fundamental-medicine", "nursing", "medical-prevention",
                              "folk_medicine"]
        case "international":
            direction_list = ["general-medicine", "pediatrics"]
    await callback_query.message.edit_text(get_text(lang, 'enter-direction'),
                                           reply_markup=direction_buttons(lang, direction_list))

    await state.set_state(UserForm.direction)


# Direction handler
@dp.callback_query(UserForm.direction, F.data.startswith("direction_"))
async def process_direction(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    direction_key = callback_query.data.split("_")[1]
    await state.update_data(direction=direction_key)
    await callback_query.answer(f"You selected {direction_key} direction.")
    data = await state.get_data()
    level = data.get('level')
    if level == 'bachelor':
        number_course = 7
    else:
        number_course = 4
    await callback_query.message.edit_text(get_text(lang, 'enter-course'), reply_markup=course_buttons(number_course))
    await state.set_state(UserForm.course)


# Course handler
async def get_groups(level_name: str, course_number: int, limit: int = 10) -> list:
    # cache_key = f'group_names_{search_term.lower()}'
    # groups = cache.get(cache_key)
    # if groups is None:
    #     cleaned_term = search_term.strip().replace(' ', '')
    #     prefix = re.match(r'^([^-]+)', cleaned_term)
    #     prefix = prefix.group(1) if prefix else cleaned_term
    #     regex_pattern = rf'^{re.escape(prefix)}-\d{{2}}$'
    queryset = Group.objects.filter(direction__level__name=level_name, course=course_number, is_active=True #).filter(
    #     Q(name__iregex=regex_pattern) | Q(name__icontains=search_term)
    ).values_list('name', flat=True)[:limit]
    groups = await orm_async(queryset.__iter__)
    groups = list(groups)

        # cache.set(cache_key, groups, timeout=3600)
    return groups


@dp.callback_query(UserForm.course)
async def process_course(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    course_number = callback_query.data.split("_")[1]
    await state.update_data(course=course_number)
    await callback_query.answer(f"You selected {course_number} course.")

    data = await state.get_data()
    level = data.get('level')

    global level_name
    if level == 'bachelor':
        level_name = "Bakalavr"
    elif level == 'master':
        level_name = "Magistr"
    elif level == 'ordinatura':
        level_name = "Ordinatura"

    course_number = int(data.get('course'))
    matches = await get_groups(level_name, course_number, limit=100)

    await callback_query.message.reply(get_text(lang, 'select-group'), reply_markup=group_buttons(matches))
    await state.set_state(UserForm.group)



# Group handler
# @dp.message(UserForm.group)
# async def process_group(message: Message, state: FSMContext):
#     user_id = message.from_user.id
#     lang = await redis_cl.get(f"user:{user_id}:language")
#
#
#     data = await state.get_data()
#     level = data.get('level')
#
#     global level_name
#     if level == 'bachelor':
#         level_name = "Bakalavr"
#     elif level == 'master':
#         level_name = "Magistr"
#     elif level == 'ordinatura':
#         level_name = "Ordinatura"
#
#     group_guess = message.text.strip()
#     course_number = int(data.get('course'))
#     matches = await get_groups(level_name, course_number, group_guess, limit=10)
#
#     if not matches:
#         await message.reply(get_text(lang, "reenter-group"))
#         return
#
#     await message.reply(get_text(lang, 'select-group'), reply_markup=group_buttons(matches))
#     await state.set_state(UserForm.group)


@dp.callback_query(UserForm.group, F.data.startswith("group_"))
async def process_group(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    group_number = callback_query.data.split("_")[1]
    await state.update_data(group=group_number)
    await callback_query.answer(f"You selected {group_number} group.")
    await callback_query.message.edit_text(get_text(lang, 'enter-firstname'), reply_markup=None)
    await state.set_state(UserForm.first_name)


# First name handler
@dp.message(UserForm.first_name)
async def process_first_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(first_name=message.text)
    await message.answer(get_text(lang, 'enter-lastname'))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.last_name)


# Last name handler
@dp.message(UserForm.last_name)
async def process_last_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(last_name=message.text)
    await message.answer(get_text(lang, 'enter-middlename'))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.middle_name)


# Middle name handler
@dp.message(UserForm.middle_name)
async def process_middle_name(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    await state.update_data(middle_name=message.text)
    await message.answer(get_text(lang, 'enter-phone'), reply_markup=phone_request_keyboard(lang))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.phone)


# Phone handler
@dp.message(UserForm.phone, F.content_type == "contact")
async def process_phone_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")

    phone_number = message.contact.phone_number

    data = await state.get_data()
    await Student.objects.filter(telegram_id=user_id).aupdate(
        is_registered=True,
        level=get_text('uz', 'levels')[data.get('level')],
        level_key=data.get('level'),
        faculty=get_text('uz', 'faculties')[data.get('faculty')],
        faculty_key=data.get('faculty'),
        direction=get_text('uz', 'directions')[data.get('direction')],
        direction_key=data.get('direction'),
        course=data.get('course'),
        group=data.get('group'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        middle_name=data.get('middle_name'),
        phone=phone_number
    )

    await state.clear()
    await message.answer(get_text(lang, "login-success"), reply_markup=menu_buttons(lang))


@dp.message(UserForm.phone)
async def process_phone_number(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    phone_number = message.text
    await message.answer(get_text(lang, "login-success"))
    try:
        await message.bot.delete_message(message.chat.id, message.message_id - 1)
    except:
        pass
    await message.delete()
    await state.set_state(UserForm.phone)
    data = await state.get_data()
    await Student.objects.filter(telegram_id=user_id).aupdate(
        is_registered=True,
        level=get_text('uz', 'levels')[data.get('level')],
        level_key=data.get('level'),
        faculty=get_text('uz', 'faculties')[data.get('faculty')],
        faculty_key=data.get('faculty'),
        direction=get_text('uz', 'directions')[data.get('direction')],
        direction_key=data.get('direction'),
        course=data.get('course'),
        group=data.get('group'),
        first_name=data.get('first_name'),
        last_name=data.get('last_name'),
        middle_name=data.get('middle_name'),
        phone=phone_number
    )

    await state.clear()

    await message.answer(get_text(lang, "menu-message"), reply_markup=menu_buttons(lang))


@dp.callback_query(F.data.startswith("edit_"))
async def process_edit_profile(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer(cache_time=10)
    user_id = callback_query.message.chat.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    updatable = callback_query.data.split("_")[1]
    await state.set_state(ProfileUpdate.value)
    await state.update_data(updatable=updatable)
    match updatable:
        case "firstname":
            await callback_query.message.edit_text(f"{get_text(lang, f'edit-{updatable}')}:",
                                                   reply_markup=None)
        case "lastname":
            await callback_query.message.edit_text(f"{get_text(lang, f'edit-{updatable}')}:",
                                                   reply_markup=None)
        case "middlename":
            await callback_query.message.edit_text(f"{get_text(lang, f'edit-{updatable}')}:",
                                                   reply_markup=None)
        case "group":
            await callback_query.message.edit_text(get_text(lang, "enter-group"), reply_markup=None)
        case "course":
            await callback_query.message.edit_text(get_text(lang, 'enter-course'), reply_markup=course_buttons())
        case "direction":
            await callback_query.message.edit_text(get_text(lang, 'enter-direction'),
                                                   reply_markup=direction_buttons(lang))
        case "faculty":
            await callback_query.message.edit_text(get_text(lang, "enter-faculty"), reply_markup=faculty_buttons(lang))
        case "level":
            await callback_query.message.edit_text(get_text(lang, "enter-level"), reply_markup=level_buttons(lang))


@dp.message(ProfileUpdate.value)
async def process_update_profile_message(message: Message, state: FSMContext):
    user_id = message.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    data = await state.get_data()
    updatable = data.get('updatable')
    new_value = message.text
    student = await orm_async(Student.objects.get, telegram_id=user_id)
    match updatable:
        case "firstname":
            student.first_name = new_value
        case "lastname":
            student.last_name = new_value
        case "middlename":
            student.middle_name = new_value
        case "group":
            group_guess = new_value.strip()

            level = student.level_key
            course_number = student.course
            global level_name
            if level == 'bachelor':
                level_name = "Bakalavr"
            elif level == 'master':
                level_name = "Magistr"
            elif level == 'ordinatura':
                level_name = "Ordinatura"

            matches = await get_groups(level_name, course_number, group_guess, limit=10)
            if not matches:
                await message.reply(get_text(lang, "reenter-group"))
                return
            await message.reply(get_text(lang, 'select-group'), reply_markup=group_buttons(matches))
            return
        case "course":
            student.course = new_value
        case "direction":
            student.direction = new_value
        case "faculty":
            student.faculty = new_value
        case "level":
            student.level = new_value

    await student.asave()
    await state.clear()
    await message.answer(get_text(lang, "edit-success"))
    response = f"{get_text(lang, 'edit-lastname')}: {student.last_name}\n" \
               f"{get_text(lang, 'edit-firstname')}: {student.first_name}\n" \
               f"{get_text(lang, 'edit-middlename')}: {student.middle_name}\n" \
               f"{get_text(lang, 'edit-level')}: {get_text(lang, 'levels')[student.level_key]}\n" \
               f"{get_text(lang, 'edit-faculty')}: {get_text(lang, 'faculties')[student.faculty_key]}\n" \
               f"{get_text(lang, 'edit-direction')}: {get_text(lang, 'directions')[student.direction_key]}\n" \
               f"{get_text(lang, 'edit-course')}: {student.course}\n" \
               f"{get_text(lang, 'edit-group')}: {student.group}\n\n"
    await message.answer(response, reply_markup=profile_buttons(lang))


@dp.callback_query(ProfileUpdate.value)
async def process_update_profile_query(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    lang = await redis_cl.get(f"user:{user_id}:language")
    data = await state.get_data()
    updatable = data.get('updatable')

    student = await orm_async(Student.objects.get, telegram_id=user_id)

    match updatable:
        case "group":
            student.group = callback_query.data.split("_")[1]
        case "course":
            course_number = callback_query.data.split("_")[1]
            student.course = course_number
        case "direction":
            direction_key = callback_query.data.split("_")[1]
            student.direction_key = direction_key
        case "faculty":
            faculty_key = callback_query.data.split("_")[1]
            student.faculty_key = faculty_key
        case "level":
            level_key = callback_query.data.split("_")[1]
            student.level_key = level_key

    await student.asave()
    await state.clear()

    await callback_query.answer(get_text(lang, "edit-success"))

    response = (
        f"{get_text(lang, 'edit-lastname')}: {student.last_name}\n"
        f"{get_text(lang, 'edit-firstname')}: {student.first_name}\n"
        f"{get_text(lang, 'edit-middlename')}: {student.middle_name}\n"
        f"{get_text(lang, 'edit-level')}: {get_text(lang, 'levels')[student.level_key]}\n"
        f"{get_text(lang, 'edit-faculty')}: {get_text(lang, 'faculties')[student.faculty_key]}\n"
        f"{get_text(lang, 'edit-direction')}: {get_text(lang, 'directions')[student.direction_key]}\n"
        f"{get_text(lang, 'edit-course')}: {student.course}\n"
        f"{get_text(lang, 'edit-group')}: {student.group}\n\n"
    )

    await callback_query.message.edit_text(response, reply_markup=profile_buttons(lang))
