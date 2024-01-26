from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from database.db_users import databaseUsers


async def modelMenuKb(id):
    model = databaseUsers.getModel(id)
    if model == 0:
        buttons = [[InlineKeyboardButton(text="✅gpt-3.5-turbo", callback_data="changeGPT3.5")],
                   [InlineKeyboardButton(text="gpt-4", callback_data="changeGPT4")],
                   [InlineKeyboardButton(text="gpt-4-turbo", callback_data="changeGPT4Turbo")],
                   [InlineKeyboardButton(text="gpt-4-vision", callback_data="changeGPTVision")],
                   [InlineKeyboardButton(text="←Назад", callback_data="gptExit")]]
    elif model == 2:
        buttons = [[InlineKeyboardButton(text="gpt-3.5-turbo", callback_data="changeGPT3.5")],
                   [InlineKeyboardButton(text="gpt-4", callback_data="changeGPT4")],
                   [InlineKeyboardButton(text="✅gpt-4-turbo", callback_data="changeGPT4Turbo")],
                   [InlineKeyboardButton(text="gpt-4-vision", callback_data="changeGPTVision")],
                   [InlineKeyboardButton(text="←Назад", callback_data="gptExit")]]
    elif model == 1:
        buttons = [[InlineKeyboardButton(text="gpt-3.5-turbo", callback_data="changeGPT3.5")],
                   [InlineKeyboardButton(text="✅gpt-4", callback_data="changeGPT4")],
                   [InlineKeyboardButton(text="gpt-4-turbo", callback_data="changeGPT4Turbo")],
                   [InlineKeyboardButton(text="gpt-4-vision", callback_data="changeGPTVision")],
                   [InlineKeyboardButton(text="←Назад", callback_data="gptExit")]]
    else:
        buttons = [[InlineKeyboardButton(text="gpt-3.5-turbo", callback_data="changeGPT3.5")],
                   [InlineKeyboardButton(text="gpt-4", callback_data="changeGPT4")],
                   [InlineKeyboardButton(text="gpt-4-turbo", callback_data="changeGPT4Turbo")],
                   [InlineKeyboardButton(text="✅gpt-4-vision", callback_data="changeGPTVision")],
                   [InlineKeyboardButton(text="←Назад", callback_data="gptExit")]]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
