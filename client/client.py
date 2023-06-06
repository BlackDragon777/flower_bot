from config import *
from .client_keyboard import client_keyboard, client_cancel
from admin import admin_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from general_heandler import general

class Client(StatesGroup):
    support = State()
    review = State()

async def support(message: types.Message):
    if not message.chat.id in ADMIN_CHAT_ID:
        await Client.support.set()
        await bot.send_message(message.chat.id, 'Пожалуйста, укажите следующую информацию:\n\n'
                             '1. Номер телефона, по которому можно связаться с вами\n'
                             '2. Адрес электронной почты, на который вы хотите получить ответ\n'
                             '3. Краткое описание проблемы или вопроса, с которым вы столкнулись\n\n'
                             'Наша команда технической поддержки свяжется с вами для решения вашей проблемы. '
                             'Благодарим вас за обращение!', reply_markup=client_cancel)
    else:
        await general.any_message(message)
async def send_support_response(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await general.cancel_start(message, state)
    else:
        await bot.send_message(message.chat.id, 'Ваш запрос принят. Мы свяжемся с вами в ближайшее время.', reply_markup=client_keyboard)
        async with state.proxy() as data:
            data['support'] = message.text

        for chat_id in ADMIN_CHAT_ID:
            await bot.send_message(chat_id=chat_id, text=f'Сообщение в техподдержку было отправлено от @{message.from_user.username}: {data["support"]}')

    await state.finish()

async def view(message: types.Message, state: FSMContext):
    if not message.chat.id in ADMIN_CHAT_ID:
        await Client.review.set()
        await message.answer('Оставьте ваш отзыв:', reply_markup=client_cancel)
    else:
        await general.any_message(message)

async def send_review_response(message: types.Message, state: FSMContext):
    if message.text == 'Отмена':
        await general.cancel_start(message, state)
    else:
        await bot.send_message(message.chat.id, 'Спасибо за ваш отзыв!', reply_markup=client_keyboard)
        async with state.proxy() as data:
            data['review'] = message.text

        for chat_id in ADMIN_CHAT_ID:
            await bot.send_message(chat_id=chat_id, text=f'Оставлен отзыв от @{message.from_user.username}: {data["review"]}')
    await state.finish()

def register_client_command(dp: Dispatcher):
    dp.register_message_handler(support, lambda message: message.text == 'Техподдержка')
    dp.register_message_handler(view, lambda message: message.text == 'Оставить отзыв')
    dp.register_message_handler(send_review_response, state=Client.review)
    dp.register_message_handler(send_support_response, state=Client.support)
