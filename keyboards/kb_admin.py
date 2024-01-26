from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup

buttons = [[InlineKeyboardButton(text="👁Статистика", callback_data="adminStat")],[InlineKeyboardButton(text="➕Новый пост", callback_data="newPost")],  [InlineKeyboardButton(text="←Назад", callback_data="adminExit")]]
adminMenu = InlineKeyboardMarkup(inline_keyboard=buttons)


buttons2 = [[InlineKeyboardButton(text="←Назад", callback_data="adminMenuExit")]]
adminMenuExit = InlineKeyboardMarkup(inline_keyboard=buttons2)


buttons3 = [[InlineKeyboardButton(text="✅Да", callback_data="adminPostMenu")], [InlineKeyboardButton(text="←Назад", callback_data="adminMenuExit")]]
postMenu = InlineKeyboardMarkup(inline_keyboard=buttons3)

buttons4 = [[InlineKeyboardButton(text="←Назад", callback_data="adminMenuExit")]]
postNext = InlineKeyboardMarkup(inline_keyboard=buttons4)

buttons5 = [[InlineKeyboardButton(text="✅Да", callback_data="postYes")],[InlineKeyboardButton(text="←Назад", callback_data="adminMenuExit")]]
postYesOrNo = InlineKeyboardMarkup(inline_keyboard=buttons5)

buttons6 = [[InlineKeyboardButton(text="←Назад", callback_data="adminMenuExit")]]
kbNext = InlineKeyboardMarkup(inline_keyboard=buttons6)

buttons7 = [[InlineKeyboardButton(text="✅Да", callback_data="photoYes")]]
photoMenu = InlineKeyboardMarkup(inline_keyboard=buttons7)
