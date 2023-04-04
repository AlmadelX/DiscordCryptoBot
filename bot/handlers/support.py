from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import func

from bot.data.loader import dp
from bot.data.texts import load_button, load_text
from bot.keyboards import start_menu, back_menu
from bot.models import Server, Subscription
from bot.services.db_session import db_session
from bot.states import Support
from bot.utils.bot_logging import bot_logger


@dp.message_handler(text=load_button('support_btn'), state=None)
async def support(message: Message):
    user_id = message.from_user.id
    reply = load_text('support_query', user_id)

    await Support.input.set()
    await message.reply(reply, reply_markup=back_menu(user_id))


@dp.message_handler(state=Support.input)
async def input(message: Message, state: FSMContext):
    user_id = message.from_user.id

    if message.text in ['Back', 'Назад']:
        reply = load_text('canceled', user_id)

        await state.finish()
        await message.reply(reply, reply_markup=start_menu(user_id))
        return

    # TODO: Send message
    bot_logger.info(message.text)

    reply = load_text('support_success', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))
