from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup

buttons = [[InlineKeyboardButton(text="←Назад", callback_data="gptExit")]]

gptExit = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons2 = [[InlineKeyboardButton(text="Выйти из диалога", callback_data="gptExitDialog")]]

gptExitDialog = InlineKeyboardMarkup(inline_keyboard=buttons2)
