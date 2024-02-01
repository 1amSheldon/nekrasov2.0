from aiogram import Router, F, Bot
from aiogram.enums import content_type
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.db_statistic import databaseStatistics
from database.db_users import databaseUsers
from handlers.start import cmd_start
from keyboards.kb_admin import *
from states.admin import Admin

router = Router()

@router.callback_query(F.data == "adminPanel")
async def adminPanel(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Админ панель\.\n\nТехнический администратор: \@iamsheldon \(По всем вопросам\)\n\n"
        f"*Выберите нужное действие:*", reply_markup=adminMenu)


@router.callback_query(F.data == "adminExit")
async def adminReturnToMenu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await cmd_start(callback)


@router.callback_query(F.data == "adminStat")
async def adminStatistics(callback: CallbackQuery):
    await callback.message.edit_text(
        "*Статистика:*"
        f"\n*Человек в базе:* {databaseStatistics.getUsers()}"
        f"\n*Всего опубликовано постов:* {databaseStatistics.getPosts()}"
        f"\n*Всего запросов в ТП:* {databaseStatistics.getSupportQuestions()}",
        reply_markup=adminMenuExit)


@router.callback_query(F.data == "adminMenuExit")
async def adminMenuFromExitStat(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Админ панель\.\n\nТехнический администратор: \@iamsheldon \(По всем вопросам\)\n\n"
        f"*Выберите нужное действие:*", reply_markup=adminMenu)


@router.callback_query(F.data == "newPost")
async def adminPostMenu(callback: CallbackQuery):
    await callback.message.edit_text("*Перейти в режим отправки поста?*", reply_markup=postMenu)


@router.callback_query(F.data == "adminPostMenu")
async def adminPostTEXT(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "*Привет\!*\n\nОтправь боту текст поста\(форматируй тгшными встроенными функциями если надо\)",
        reply_markup=adminMenuExit)
    await state.set_state(Admin.IN_POST_TEXT)


@router.message(Admin.IN_POST_TEXT)
async def adminPostNextTEXT(message: Message, state: FSMContext):
    try:
        await message.answer(
            f"Текст поста:\n\n\n\n{message.html_text}\n\n\n\nЕсли что-то пошло не так, отправь повторно текст или же перейдем к клавиатурам",
            reply_markup=postYesOrNo, parse_mode="HTML", disable_web_page_preview=True)
        await state.update_data(text=message.html_text)
    except Exception as ex:
        await message.answer(f"Ошибка! \n\nStack-Trace:\n{ex.args[0]}", parse_mode=None)


@router.callback_query(F.data == "postYes")
async def adminPostNextKBTEXT(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Введи ЧЕРЕЗ ТОЧКУ С ЗАПЯТОЙ названия кнопок(со смайликами и прочим)\n\nПример: \n\n←Перейти;🔴США;🔊РОССИЯ"
        "\n\nЕсли кнопки не нужны отправь символ Z(обязательно большая)",
        reply_markup=adminMenuExit, parse_mode=None)
    await callback.answer()
    await state.set_state(Admin.IN_POST_KB)


@router.message(Admin.IN_POST_KB)
async def adminPostNextKBLINKS(message: Message, state: FSMContext):
    await message.answer(
        "Теперь введи ЧЕРЕЗ ТОЧКУ С ЗАПЯТОЙ ссылки, на которые будут ссылаться кнопки(строго по примеру)\n\nПример: \n\nt.me/iamsheldon;t.me;telegram.org"
        "\n\nЕсли кнопки не нужны отправь символ Z(обязательно заглавная)",
        reply_markup=adminMenuExit, parse_mode=None)
    await state.update_data(text_kb=message.text)
    await state.set_state(Admin.IN_POST_PHOTOS)


@router.message(Admin.IN_POST_PHOTOS)
async def adminPostNextPIC(message: Message, state: FSMContext):
    await message.answer("Теперь отправь ОДНУ фотографию, которая должна быть прикреплена к посту"
                         "\n\nЕсли фото не нужно, отправь символ Z(обязательно заглавная)",
                         reply_markup=adminMenuExit, parse_mode=None)
    await state.update_data(links_kb=message.text)
    await state.set_state(Admin.IN_POST_WAIT_PHOTOS)


@router.message(Admin.IN_POST_WAIT_PHOTOS)
async def adminPostDemo(message: Message, state: FSMContext, bot: Bot):
    try:
        data = await state.get_data()
        builder = InlineKeyboardBuilder()

        if data["text_kb"] != "Z" and message.content_type == content_type.ContentType.PHOTO:
            for text, link in zip(data["text_kb"].split(";"), data["links_kb"].split(";")):
                builder.row(InlineKeyboardButton(
                    text=text,
                    url=link))
            await bot.send_photo(chat_id=message.from_user.id, caption=data["text"], photo=message.photo[-1].file_id,
                                 reply_markup=builder.as_markup(), parse_mode="HTML")
            await state.clear()
            await state.update_data(builder=builder, photo=message.photo[-1].file_id, text=data["text"])

        if data["text_kb"] == "Z" and message.content_type == content_type.ContentType.PHOTO:
            await bot.send_photo(chat_id=message.from_user.id, caption=data["text"], photo=message.photo[-1].file_id,
                                 parse_mode="HTML")
            await state.clear()
            await state.update_data(builder="Z", photo=message.photo[-1].file_id, text=data["text"])

        if data["text_kb"] == "Z" and message.content_type == content_type.ContentType.TEXT:
            await bot.send_message(chat_id=message.from_user.id, text=data["text"], parse_mode="HTML")
            await state.clear()
            await state.update_data(builder="Z", photo="Z", text=data["text"])

        if data["text_kb"] != "Z" and message.content_type == content_type.ContentType.TEXT:
            for text, link in zip(data["text_kb"].split(";"), data["links_kb"].split(";")):
                builder.row(InlineKeyboardButton(
                    text=text,
                    url=link))
            await bot.send_message(chat_id=message.from_user.id, text=data["text"], reply_markup=builder.as_markup(),
                                   parse_mode="HTML")
            await state.clear()
            await state.update_data(builder=builder, photo="Z", text=data["text"])

        builder2 = InlineKeyboardBuilder()
        builder2.row(InlineKeyboardButton(
            text="Начать рассылку", callback_data='GOPOST')
        )
        builder2.row(InlineKeyboardButton(
            text="Отмена", callback_data='adminMenuExit')
        )
        await message.answer("Начать рассылку?", reply_markup=builder2.as_markup())
    except Exception as ex:
        await state.clear()
        await message.answer(f"Аварийный сброс состояния. Ошибка: {ex.args}", parse_mode=None)


@router.callback_query(F.data == "GOPOST")
async def adminPostGo(callback: CallbackQuery, state: FSMContext, bot: Bot):
    try:

        data = await state.get_data()
        await callback.answer()
        await callback.message.answer("Рассылка начата")
        databaseStatistics.addPost()
        await cmd_start(callback)

        if data["builder"] == "Z" and data["photo"] == "Z":
            for i in databaseUsers.getUsers():
                try:
                    await bot.send_message(chat_id=i, text=data["text"], parse_mode="HTML")
                except:
                    pass
        if data["builder"] != "Z" and data["photo"] == "Z":
            for i in databaseUsers.getUsers():
                try:
                    await bot.send_message(chat_id=i, text=data["text"], reply_markup=data["builder"].as_markup(),
                                           parse_mode="HTML")
                except:
                    pass
        if data["builder"] == "Z" and data["photo"] != "Z":
            for i in databaseUsers.getUsers():
                try:
                    await bot.send_photo(chat_id=i, caption=data["text"], photo=data["photo"], parse_mode="HTML")
                except:
                    pass
        if data["builder"] != "Z" and data["photo"] != "Z":
            for i in databaseUsers.getUsers():
                try:
                    await bot.send_photo(chat_id=i, caption=data["text"], photo=data["photo"],
                                         reply_markup=data["builder"].as_markup(), parse_mode="HTML")
                except:
                    pass

        await state.clear()
        await callback.message.answer("Рассылка закончена")
    except Exception as ex:
        await state.clear()
        await callback.message.answer(f"Аварийная остановка рассылки. Ошибка: {ex.args}", parse_mode=None)
