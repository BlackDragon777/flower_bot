from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_keyboard.add(KeyboardButton('Отправить рассылку'))

choice = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
choice.add(KeyboardButton('Да'), KeyboardButton('Нет'))

admin_cancel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_cancel.add(KeyboardButton('Отмена'))
