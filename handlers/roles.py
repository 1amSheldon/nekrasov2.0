from aiogram import Router, F
from aiogram.types import CallbackQuery

from keyboards.kb_roles import *

router = Router()


@router.callback_query(F.data == "roles")
async def roleMenu(callback: CallbackQuery):
    await callback.message.edit_text("*Некрасова2\.0 будет общаться с вами так, как захотите\.*\n\nВыберите нужную роль\.",
                                     reply_markup=await rolesMenu(callback.from_user.id))


@router.callback_query(F.data.startswith("changeRole"))
async def changeRoles(callback: CallbackQuery):
    try:
        roleName = callback.data.replace("changeRole", "")
        databaseUsers.setRoleText(callback.from_user.id, roles.get(roleName))
        databaseUsers.setRoleName(callback.from_user.id, roleName)
        await callback.message.edit_text("*Некрасова2\.0 будет общаться с вами так, как захотите\.*\n\nВыберите нужную роль\.",
                                         reply_markup=await rolesMenu(callback.from_user.id))
    except:
        await callback.answer()
