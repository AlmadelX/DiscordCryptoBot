from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot.bot import dispatcher, bot
from bot.keyboards import start_menu, back_menu
from bot.states import Support
from bot.resources.config import config


@dispatcher.message_handler(text='👨‍💻 Поддержка', state=None)
async def support(message: Message):
    await Support.input.set()
    await message.reply('Ваше сообщение для службы поддержки:', reply_markup=back_menu())


@dispatcher.message_handler(text='Назад', state=Support.input)
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.reply('Отменено', reply_markup=start_menu(message.from_user.id))


@dispatcher.message_handler(state=Support.input)
async def query(message: Message, state: FSMContext):
    user_id = message.from_user.id

    for admin in config.bot_admins:
        await bot.send_message(admin, f'Обращение в поддержку от @{message.from_user.username}:\n{message.text}')

    reply = 'Ваше сообщение отправлено.\nВскоре служба поддержки с вами свяжется.'

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))
