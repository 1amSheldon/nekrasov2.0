from aiogram.filters import BaseFilter
from aiogram.types import Message


class MessageFilterSupportAdmin(BaseFilter):
    async def __call__(self, message: Message) -> bool:  # [3]
        try:
            if message.reply_to_message.text.startswith("Проблема:") or message.reply_to_message.text.startswith(
                    "Ответ от пользователя:"):
                return True
        except:
            return False


class MessageFilterSupportUser(BaseFilter):
    async def __call__(self, message: Message) -> bool:  # [3]
        try:
            if message.reply_to_message.text.startswith("Новое сообщение от поддержки!"):
                return True
        except:
            return False
