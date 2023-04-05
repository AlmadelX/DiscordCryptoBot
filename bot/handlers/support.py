from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from sqlalchemy import func

from bot.data.loader import dp, bot
from bot.data.texts import load_button, load_text
from bot.keyboards import start_menu, back_menu
from bot.states import Support
from bot.data.config import get_admins


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

    for admin in get_admins():
        await bot.send_message(admin, f'New support call from {user_id}:\n{message.text}')

    reply = load_text('support_success', user_id)

    await state.finish()
    await message.reply(reply, reply_markup=start_menu(user_id))
