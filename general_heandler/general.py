from config import *
from client import client_keyboard
from admin import admin_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from Database.database import Database


db = Database('client.db')

async def startup_screen(message: types.Message):
    if message.chat.id not in ADMIN_CHAT_ID:
        await bot.send_photo(chat_id=message.chat.id, photo=open('img/hello_flower.jpg', 'rb'), caption='''
            Добро пожаловать в наш уютный магазин комнатных растений! 🌺🌱🌿 
            Я - ваш верный помощник-бот, готовый ответить на любые ваши вопросы о выборе, уходе и выращивании растений. 🤖💬
            У нас вы найдете множество разнообразных видов растений - от зеленых и сочных до цветущих и ароматных. 🌸🌺🌼
            Мы организуем доставку до вашего дома и предлагаем все необходимые аксессуары для ухода за растениями. 🚚🌱💦
            Так что, не теряйте времени и приходите к нам за свежими и здоровыми растениями! 🌿👍
            ''')
        if db.exicts_userid(message.from_user.id):
            pass
        else:
            db.add_userid(message.from_user.id)
        await message.delete()
        await bot.send_message(message.chat.id, 'Выберите действие: ', reply_markup=client_keyboard.client_keyboard)

    elif message.chat.id in ADMIN_CHAT_ID:
        await message.delete()
        await bot.send_message(message.chat.id, 'Приветствую админ', reply_markup=admin_keyboard.admin_keyboard)

async def cancel_start(message: types.Message, state: FSMContext):
    if message.chat.id not in ADMIN_CHAT_ID:
        await state.finish()
        await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=client_keyboard.client_keyboard)
    elif message.chat.id in ADMIN_CHAT_ID:
        await state.finish()
        await bot.send_message(message.chat.id, 'Выберите действие:', reply_markup=admin_keyboard.admin_keyboard)

async def any_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Это не похоже на команду. Попробуйте еще раз.')

def register_general_heandler(dp: Dispatcher):
    dp.register_message_handler(startup_screen, commands=['start'], state='*')
    dp.register_message_handler(cancel_start, lambda message: message.text == 'Отмена', state='*')
    dp.register_message_handler(any_message, content_types=types.ContentType.TEXT)