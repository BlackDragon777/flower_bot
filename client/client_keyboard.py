from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

client_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_keyboard.add(KeyboardButton('Техподдержка'), KeyboardButton('Оставить отзыв'))

client_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_cancel.add(KeyboardButton('Отмена'))

