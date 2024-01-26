from aiogram.fsm.state import StatesGroup, State

  

class Admin(StatesGroup):
    IN_POST_TEXT = State()
    IN_POST_KB = State()
    IN_POST_KB_TEXT = State()
    IN_POST_PHOTOS = State()
    IN_POST_WAIT_PHOTOS = State()
