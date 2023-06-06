from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN, bot, dp, ADMIN_CHAT_ID
from client import client, client_keyboard
from admin import admin, admin_keyboard
from bacground import keep_alive
from general_heandler import general


# Initialize bot and dispatcher

async def on_startup(_):
    print('Бот запущен...')


client.register_client_command(dp)
admin.register_admin_command(dp)
general.register_general_heandler(dp)


if __name__ == '__main__':
    keep_alive()
    executor.start_polling(dispatcher=dp, skip_updates=True, on_startup=on_startup)
