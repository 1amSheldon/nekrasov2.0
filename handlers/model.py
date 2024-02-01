from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.kb_model import modelMenuKb
from keyboards.kb_roles import *

router = Router()


@router.callback_query(F.data == "model")
async def modelMenu(callback: CallbackQuery):
    await callback.message.edit_text("*Выберите одну из доступных моделей Некрасова2\.0\.*",
                                     reply_markup=await modelMenuKb(callback.from_user.id))


@router.callback_query(F.data.startswith("changeGPT"))
async def modelMenu(callback: CallbackQuery):
    databaseUsers.setModel(
        0 if callback.data.replace("changeGPT", "") == "3.5"
        else 2 if callback.data.replace("changeGPT","") == "4Turbo"
        else 3 if callback.data.replace("changeGPT", "") == "Vision"
        else 1,
        callback.from_user.id)
    try:
        await callback.message.edit_text("*Выберите одну из доступных моделей Некрасова2\.0\.*",
                                         reply_markup=await modelMenuKb(callback.from_user.id))
    except:
        await callback.answer()
