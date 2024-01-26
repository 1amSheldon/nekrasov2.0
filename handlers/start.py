from aiogram import Router
from aiogram.types import Message, CallbackQuery

from database.db_statistic import databaseStatistics
from database.db_users import databaseUsers
from database.history import databaseHistory
from keyboards import kb_start

router = Router()


@router.message()
async def cmd_start(message: Message | CallbackQuery, *args):
    if databaseUsers.updateUser(message.from_user.id):
        if type(message) == Message:
            await message.answer(
                "Добро пожаловать в Nerkasov2\.0\! Откройте для себя новый мир с помощью ИИ\.\n\n*Выберите нужно действие*",
                reply_markup=await kb_start.startMenu(message.from_user.id))
        else:
            message: CallbackQuery
            if len(args) != 0:  # гавнокод но без него никак, проверяем для функции gptexitdialog
                await message.message.answer(
                    "Добро пожаловать в Nerkasov2\.0\! Откройте для себя новый мир с помощью ИИ\.\n\n*Выберите нужно действие*",
                    reply_markup=await kb_start.startMenu(message.from_user.id))
                return
            else:
                await message.message.edit_text(
                    "Добро пожаловать в Nerkasov2\.0\! Откройте для себя новый мир с помощью ИИ\.\n\n*Выберите нужно действие*",
                    reply_markup=await kb_start.startMenu(message.from_user.id))
        return
    databaseHistory.addUser(message.from_user.id)
    databaseStatistics.addUsers()
    await message.answer(
        "Откройте для себя бесконечные возможности в сфере ИИ\.\n\n*Выберите нужное действие:*",
        reply_markup=await kb_start.startMenu(message.from_user.id))
