from config import *
from .admin_keyboard import admin_keyboard, admin_cancel, choice
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from general_heandler import general
from Database.database import Database

db = Database('client.db')
class Rassylka(StatesGroup):
    photo = State()
    description = State()
    choice = State()

async def rassylka(message: types.Message):
    if message.chat.id in ADMIN_CHAT_ID:
        await bot.send_message(message.chat.id, 'Пришлите фотографию для рассылки:', reply_markup=admin_cancel)
        await Rassylka.photo.set()
    else:
        await bot.send_message(message.chat.id, 'Вы не являетесь администратором')

async def photo_handler(message: types.Message, state: FSMContext):
    if message.photo:
        async with state.proxy() as data:
            data['photo'] = message.photo[-1].file_id
        await Rassylka.next()
        await text_handler(message, state)
    elif message.text == 'Отмена':
        await general.cancel_start(message, state)
    else:
        await bot.send_message(message.chat.id, 'Вы не прислали фотографию. Попробуйте снова.')
        return
async def text_handler(message: types.Message, state: FSMContext):
    await message.answer('Введите текст для рассылки:', reply_markup=admin_cancel)
    if message.text == 'Отмена':
        await general.cancel_start(message, state)
        return
    if message.text:
        async with state.proxy() as data:
            data['description'] = message.text
        await Rassylka.next()
        await choice_handler(message, state)

async def choice_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.send_photo(message.chat.id, data['photo'], caption=data['description'])
        await Rassylka.next()
        await Rassylka.choice.set()
        await bot.send_message(message.chat.id, 'Все верно?', reply_markup=choice)


async def process_choice(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == 'Да':
            user = db.get_userid()
            users = (i[0] for i in user)
            for user in users:
                try:
                    await bot.send_photo(user, data['photo'], caption=data['description'])
                except:
                    continue
            await bot.send_message(message.chat.id, 'Рассылка завершена.', reply_markup=admin_keyboard)
        elif message.text == 'Нет':
            await bot.send_message(message.chat.id, 'Отменено.', reply_markup=admin_keyboard)
    await state.finish()

def register_admin_command(dp: Dispatcher):
    dp.register_message_handler(rassylka, lambda message: message.text == 'Отправить рассылку', state='*')
    dp.register_message_handler(photo_handler, content_types=types.ContentType.ANY, state=Rassylka.photo)
    dp.register_message_handler(text_handler, content_types=types.ContentType.TEXT, state=Rassylka.description)
    dp.register_message_handler(process_choice, content_types=types.ContentType.TEXT, state=Rassylka.choice)
