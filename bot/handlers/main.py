from aiogram.types import Message

from bot.data.loader import dp


@dp.message_handler(commands=['start', 'help'])
async def welcome(message: Message):
    await message.reply('Welcome!\n[bot description]')


@dp.message_handler()
async def not_supported(message: Message):
    await message.reply('Command not supported.')
    