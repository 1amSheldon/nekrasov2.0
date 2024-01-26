from aiogram import Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from database.db_statistic import databaseStatistics
from filters import supportFilters
from handlers.start import cmd_start
from keyboards.kb_support import *
from states.users import User

router = Router()


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.message.edit_text(
        "Пожалуйста, обратите внимание, что в поддержке работает *главный трудяга админ и команда разработчиков*\."
        "Мы постараемся помочь как можно быстрее, но ожидание может занять время\.\n\n"
        "График работы: _10:00\-20:00 по московскому времени_\.\n\n"
        "Желаете связаться со службой поддержки?",
        reply_markup=supportMenu)


@router.callback_query(F.data == "supportDialog")
async def supportDialog(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "✅ Чат с поддержкой установлен\n\nПереходите сразу к сути дела в обращении за помощью, стараясь максимально осветить проблему в *одном сообщении*\."
        "\nТаким образом мы сможем быстро дать ответ и решить Вашу проблему\.",
        reply_markup=supportExit)
    await state.set_state(User.IN_SUPPORT_DIALOG)


@router.callback_query(F.data == "supportExit")
async def supportMenuExit(callback: CallbackQuery):
    await cmd_start(callback)


@router.callback_query(F.data == "supportExitDialog")
async def supportDialogExit(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Пожалуйста, обратите внимание, что в поддержке работает *главный трудяга админ и команда разработчиков*\."
        "Мы постараемся помочь как можно быстрее, но ожидание может занять время\.\n\n"
        "График работы: _10:00\-20:00 по московскому времени_\.\n\n"
        "Желаете связаться со службой поддержки?",
        reply_markup=supportMenu)
    await state.clear()


@router.message(User.IN_SUPPORT_DIALOG)
async def sendSupport(message: Message, state: FSMContext, bot: Bot):
    await bot.send_message(chat_id=295092847,
                           text=f"Проблема: {message.text}\n\n"
                                f"TECH_INFORMATION\n\n"
                                f"Username: {message.from_user.username}\n"
                                f"ID: &№{message.from_user.id}&№\n"
                                f"FirstName/LastName: {message.from_user.first_name} {message.from_user.last_name}\n\np.s. символы до айдишника и после айдишника чисто технические и нужны для корректной работы",
                           parse_mode=None)
    await message.answer("*Ваше обращение доставлено\. Благодарим за обратную связь\!*")
    databaseStatistics.addSupportQuestion()
    await state.clear()


@router.message(supportFilters.MessageFilterSupportAdmin())
async def answerSupport(message: Message, bot: Bot):
    userId = int(message.reply_to_message.text[
                 message.reply_to_message.text.find("&№") + 2:message.reply_to_message.text.rfind("&№")])
    await bot.send_message(chat_id=userId,
                           text=f"Новое сообщение от поддержки!: \n\n{message.text}\n\nДостаточно ответить на это сообщение, чтоб мы получили от вас сообщение",
                           parse_mode=None)
    await message.answer('*Сообщение доставлено\!*')


@router.message(supportFilters.MessageFilterSupportUser())
async def answerUser(message: Message, bot: Bot):
    await bot.send_message(chat_id=295092847,
                           text=f"Ответ от пользователя: {message.text}\n\n"
                                f"TECH_INFORMATION\n\n"
                                f"Username: {message.from_user.username}\n"
                                f"ID: &№{message.from_user.id}&№\n"
                                f"FirstName/LastName: {message.from_user.first_name} {message.from_user.last_name}\n\np.s. символы до айдишника и после айдишника чисто технические и нужны для корректной работы",
                           parse_mode=None)
    await message.answer('*Сообщение доставлено\!*')
    databaseStatistics.addSupportQuestion()
