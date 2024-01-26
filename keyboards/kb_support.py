from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup

buttons = [[InlineKeyboardButton(text="✅Да", callback_data="supportDialog")],
           [InlineKeyboardButton(text="←Назад", callback_data="supportExit")]]
supportMenu = InlineKeyboardMarkup(inline_keyboard=buttons)

buttons2 = [[InlineKeyboardButton(text="←Назад", callback_data="supportExitDialog")]]
supportExit = InlineKeyboardMarkup(inline_keyboard=buttons2)
