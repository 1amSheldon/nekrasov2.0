from aiogram.fsm.state import StatesGroup, State


class User(StatesGroup):
    IN_GPT_DIALOG = State()
    IN_SUPPORT_DIALOG = State()
