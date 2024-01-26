from aiogram.types import InlineKeyboardButton, \
    InlineKeyboardMarkup


async def startMenu(id):
    if id == 295092847:
        buttons = [[InlineKeyboardButton(text="➕Новый диалог", callback_data="new_dialog")],
                   [
                       InlineKeyboardButton(text="🤖Модель", callback_data="model"),
                       InlineKeyboardButton(text="🎭Роли", callback_data="roles"),
                   ],
                   [
                    InlineKeyboardButton(text="🆘Поддержка", callback_data="support")
                    ],
                   [InlineKeyboardButton(text="🧠Админ-панель", callback_data="adminPanel"),
                    ]
                   ]
    else:
        buttons = [[InlineKeyboardButton(text="➕Новый диалог", callback_data="new_dialog")],
                   [
                       InlineKeyboardButton(text="🤖Модель", callback_data="model"),
                       InlineKeyboardButton(text="🎭Роли", callback_data="roles"),
                   ],
                   [InlineKeyboardButton(text="🆘Поддержка", callback_data="support")
                    ]
                   ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
