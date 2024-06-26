from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from dal.telegramm_db import *
from data.questions import *


async def cmd_start(message:types.Message): 
    kb = [
        [
            types.KeyboardButton(text="start"),
            types.KeyboardButton(text="rating")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer('Welcome to quiz', reply_markup=keyboard)


async def cmd_quiz(message:types.Message):     
    await message.answer('GO')
    await new_quiz(message)


async def cmd_rating(message:types.Message):
    rating = await get_users_result()
    rating_message = ''
    for result in rating:
        rating_message += f'{result[1]} : {result[2]} \n'
    
    if rating_message == '':
        rating_message = 'no results'
    await message.answer(rating_message)

async def new_quiz(message:types.Message):     
    user_id = message.from_user.id
    question_index = 0
    user_result = 0
    await update_quiz_state(user_id, question_index, user_result)
    await get_question(message,user_id)


async def get_question(message,user_id):     
    question_index = await get_question_index(user_id)
    opts = quiz_data[question_index]['options']
    kb = generate_options_kb(opts)
    await message.answer(f"{quiz_data[question_index]['question']}", reply_markup=kb)



def generate_options_kb(opts):
    builder = InlineKeyboardBuilder()
    for i,option in enumerate(opts):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=str(i))
        )
    builder.adjust(1)
    return builder.as_markup()



async def answer(callback:types.CallbackQuery):
    
    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )

    current_question_index = await get_question_index(callback.from_user.id)
    current_question = quiz_data[current_question_index]
    user_answer = int(callback.data)
    
    await callback.message.answer(current_question['options'][user_answer])
    user_result = await get_result(callback.from_user.id)
    
    if current_question['correct_option'] == user_answer:
        user_result +=1
    
    current_question_index +=1
    await update_quiz_state(callback.from_user.id, current_question_index, user_result)

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        await callback.message.answer("Это был последний вопрос. Квиз завершен!")
        result = await get_result(callback.from_user.id)
        user_name = callback.from_user.full_name
        await update_result(callback.from_user.id, user_name, result)
        