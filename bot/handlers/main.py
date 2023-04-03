from aiogram.types import Message

from bot.data.loader import dp

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply('Welcome!')

@dp.message_handler()
async def echo(message: Message):
    await message.answer(message.text)
