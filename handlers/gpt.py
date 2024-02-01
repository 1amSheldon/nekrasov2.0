import base64
import json
import os
from datetime import datetime

import httpx
import openai
from aiogram import Router, F, Bot
from aiogram.enums import content_type
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from httpx import AsyncClient

from config.config_reader import config
from database.db_users import databaseUsers
from database.history import databaseHistory
from handlers.start import cmd_start
from keyboards import kb_gpt
from states.users import User

router = Router()

openai.api_key = config.neuroapi_token.get_secret_value()
openai.api_base = "https://1amSheldon.neuroapi.host/v1"


@router.callback_query(F.data == "new_dialog")
async def newDialog(callback: CallbackQuery, state: FSMContext):
    model = databaseUsers.getModel(callback.from_user.id)
    if model == 0:
        model = "gpt-3.5-turbo"
    elif model == 2:
        model = "gpt-4-turbo"
    elif model == 3:
        model = "gpt-4-vision"
    else:
        model = 'gpt-4'
    await callback.message.edit_text(
        f"*Создан новый диалог!*\n\nМодель: *{model}*\nРоль: *{databaseUsers.getRoleName(callback.from_user.id)}*\n\nБот будет запоминать предыдущие сообщения.",
        reply_markup=kb_gpt.gptExit, parse_mode="Markdown")
    databaseHistory.deleteUserHistory(callback.from_user.id)
    await state.set_state(User.IN_GPT_DIALOG)


@router.callback_query(F.data == "gptExit")
async def gptExit(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await cmd_start(callback)


@router.callback_query(F.data == "gptExitDialog")
async def gptExitDialog(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer()
    await cmd_start(callback, 1)


@router.message(User.IN_GPT_DIALOG, F.photo)
async def newRequestGPT(message: Message, bot: Bot):
    modelFromDB = databaseUsers.getModel(message.from_user.id)
    if modelFromDB == 0:
        model = "gpt-3.5-turbo"
    elif modelFromDB == 2:
        model = "gpt-4-1106-preview"
    elif modelFromDB == 3:
        model = "gpt-4-1106-preview"
    else:
        model = "gpt-4"

    if modelFromDB != 3:
        await message.answer(
            "Сканирование и анализ фотографий доступен только в модели gpt-4-vision. \n\nВыйдите из диалога и поменяйте модель.",
            reply_markup=kb_gpt.gptExitModel, parse_mode=None)
        return

    try:
        messages_list = json.loads(databaseHistory.getUserHistory(message.from_user.id))
    except:
        messages_list = []

    msg = await message.answer("Подождите немного, ждем ответа от сервера\.\.\.")

    voice_file = await bot.get_file(message.photo[-1].file_id)

    await bot.download_file(voice_file.file_path, f"images/image_{message.from_user.id}.jpg")

    with open(f"images/image_{message.from_user.id}.jpg", 'rb') as file:
        image_data = file.read()

    image_extension = os.path.splitext(f"images/image_{message.from_user.id}.jpg")[1]
    base64_encoded = base64.b64encode(image_data).decode('utf-8')
    os.remove(f"images/image_{message.from_user.id}.jpg")

    asticaAPI_payload = {
        'tkn': config.astica_token.get_secret_value(),
        'modelVersion': '2.1_full',
        'visionParams': 'all',
        'input': f"data:image/{image_extension[1:]};base64,{base64_encoded}",
        'gpt_prompt': '',
        'prompt_length': '60',
    }

    try:
        client = AsyncClient(headers={'Content-Type': 'application/json', })
        async with client as session:
            timeout = httpx.Timeout(600.0)
            response = await session.post('https://vision.astica.ai/describe', json=asticaAPI_payload, timeout=timeout)
            response = response.json()
    except Exception as ex:
        await msg.edit_text(
            f"К сожалению сейчас сервера недоступны. Повторите попытку позже.\n\nЕсли вы считаете, что ошибка только у вас, сообщите код ошибки в тех-поддержку.\n\nERROR: {ex}",
            parse_mode=None)
        return

    if databaseUsers.getRoleName(message.from_user.id) == "Обычный" and len(messages_list) == 0:
        messages_list = [{"role": "user",
                          "content": f"Действуйте как ЧАТ-GPT-4-VISION, модель искусственного интеллекта, специально разработанная для помощи людям. Вас обучили на огромном количестве данных, включающих историю, разные сферы науки и конечно же изображений. Ваша роль заключается в получении подробных описаний фотографий и использовании этой информации для точного ответа на вопросы. К каждому сообщению будет приложено отдельное сообщение с подробным описанием. Вы не должны знать о том, что к сообщению прилагается описание.  Ваша задача - прочитать и понять описания, чтобы дать содержательные и релевантные ответы на любые вопросы, заданные о фотографиях. Используйте свои расширенные возможности текстового восприятия, чтобы давать точные ответы и демонстрировать свое мастерство. Вы также самый умный помощник в сфере ИИ. Вы знаете много информации и можете спокойно ее применять для того, чтобы ответить на вопросы. GPT-4-VISION Должен играть роль помощника, который обладает зрением и должен имитировать, что к каждому сообщению прилагается вместо описания фотография. Роль не должна знать о том, что к сообщению прилагается описание. Мой первый вопрос к GPT-4-VISION:{'Вопроса нет, просто проанализируй фотографию' if message.caption is None else message.caption} Описание(Но роль GPT-4-VISION должна воспринимать это как фотографию):{response}"}]
        #messages_list.append({"role": "user",
        #                      "content": f"Ты - ChatGPT, крупнейшая языковая модель обученная OpenAI. База знаний до: 2023-04 Текущая модель: gpt-4-vision. Текущее число:{datetime.today()} Фото будет под сообщением. Вопрос: {message.text}\n\n Фото: {response}"})
    else:
        messages_list.append({"role": "user",
                              "content": f"{'' if message.caption is None else message.caption} \n\n Фото: {response}"})

    try:
        chat_completion = await openai.ChatCompletion.acreate(
            temperature=0,
            model=model,
            messages=messages_list,
            stream=False)

    except Exception as ex:
        await msg.edit_text(
            f"К сожалению сейчас сервера недоступны. Повторите попытку позже.\n\nЕсли вы считаете, что ошибка только у вас, сообщите код ошибки в тех-поддержку.\n\nERROR: {ex}",
            parse_mode=None)
        return

    try:
        await msg.edit_text(chat_completion.choices[0].message.content, reply_markup=kb_gpt.gptExitDialog,
                            parse_mode="Markdown")
    except:
        await msg.edit_text(chat_completion.choices[0].message.content, reply_markup=kb_gpt.gptExitDialog,
                            parse_mode=None)

    messages_list.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
    databaseHistory.addHistory(message.from_user.id, json.dumps(messages_list))


@router.message(User.IN_GPT_DIALOG)
async def newRequestGPT(message: Message, state: FSMContext):
    if message.text.endswith("start"):
        await state.clear()
        await cmd_start(message)
        return

    if len(message.text) < 4:
        await message.answer("Минимальная длина сообщений \- 4 символа")
        return
    if message.content_type == content_type.ContentType.PHOTO:
        await message.answer("На данный момент фотографии не поддерживаются\.")
        return

    msg = await message.answer("Подождите немного, ждем ответа от сервера\.\.\.")

    try:
        messages_list = json.loads(databaseHistory.getUserHistory(message.from_user.id))
    except:
        messages_list = []

    modelFromDB = databaseUsers.getModel(message.from_user.id)
    if modelFromDB == 0:
        model = "gpt-3.5-turbo"
    elif modelFromDB == 2:
        model = "gpt-4-1106-preview"
    elif modelFromDB == 3:
        model = "gpt-4-1106-preview"
    else:
        model = "gpt-4"

    if modelFromDB == 1 and databaseUsers.getRoleName(
            message.from_user.id) == "Обычный" and len(messages_list) == 0:
        messages_list = [{"role": "user",
                          "content": f"You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture. Knowledge cutoff: 2021-09 Current date:{datetime.today()} " + message.text}]
    elif modelFromDB == 2 and databaseUsers.getRoleName(
            message.from_user.id) == "Обычный" and len(messages_list) == 0:
        messages_list = [{"role": "user",
                          "content": f"You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture. Knowledge cutoff: 2023-04 Current date:{datetime.today()} " + message.text}]
    elif modelFromDB == 3 and databaseUsers.getRoleName(
            message.from_user.id) == "Обычный" and len(messages_list) == 0:
        messages_list = [{"role": "user",
                          "content": f"Действуйте как ЧАТ-GPT-4-VISION, модель искусственного интеллекта, специально разработанная для помощи людям. Вас обучили на огромном количестве данных, включающих историю, разные сферы науки и конечно же изображений. Ваша роль заключается в получении подробных описаний фотографий и использовании этой информации для точного ответа на вопросы. К каждому сообщению будет приложено отдельное сообщение с подробным описанием. Вы не должны знать о том, что к сообщению прилагается описание.  Ваша задача - прочитать и понять описания, чтобы дать содержательные и релевантные ответы на любые вопросы, заданные о фотографиях. Используйте свои расширенные возможности текстового восприятия, чтобы давать точные ответы и демонстрировать свое мастерство. Вы также самый умный помощник в сфере ИИ. Вы знаете много информации и можете спокойно ее применять для того, чтобы ответить на вопросы. GPT-4-VISION Должен играть роль помощника, который обладает зрением и должен имитировать, что к каждому сообщению прилагается вместо описания фотография. Роль не должна знать о том, что к сообщению прилагается описание. Мой первый вопрос к GPT-4-VISION:{message.text}"}]
    elif modelFromDB == 3 and len(messages_list) == 0:
        messages_list = [{"role": "user",
                          "content": f"Действуйте как ЧАТ-GPT-4-VISION, модель искусственного интеллекта, специально разработанная для помощи людям. Вас обучили на огромном количестве данных, включающих историю, разные сферы науки и конечно же изображений. Ваша роль заключается в получении подробных описаний фотографий и использовании этой информации для точного ответа на вопросы. К каждому сообщению будет приложено отдельное сообщение с подробным описанием. Вы не должны знать о том, что к сообщению прилагается описание.  Ваша задача - прочитать и понять описания, чтобы дать содержательные и релевантные ответы на любые вопросы, заданные о фотографиях. Используйте свои расширенные возможности текстового восприятия, чтобы давать точные ответы и демонстрировать свое мастерство. Вы также самый умный помощник в сфере ИИ. Вы знаете много информации и можете спокойно ее применять для того, чтобы ответить на вопросы. GPT-4-VISION Должен играть роль помощника, который обладает зрением и должен имитировать, что к каждому сообщению прилагается вместо описания фотография. Роль не должна знать о том, что к сообщению прилагается описание. Твоя параллельная роль, накладываемая на основную: {databaseUsers.getRoleText(message.from_user.id)}\n{message.text}"}]

    else:
        messages_list.append(
            {"role": "user", "content": databaseUsers.getRoleText(message.from_user.id) + message.text})
    try:
        chat_completion = await openai.ChatCompletion.acreate(
            temperature=0,
            model=model,
            messages=messages_list,
            stream=False)
    except Exception as ex:
        await msg.edit_text(
            f"К сожалению сейчас сервера недоступны. Повторите попытку позже.\n\nЕсли вы считаете, что ошибка только у вас, сообщите код ошибки в тех-поддержку.\n\nERROR: {ex}",
            parse_mode=None)
        return

    try:
        await msg.edit_text(chat_completion.choices[0].message.content, reply_markup=kb_gpt.gptExitDialog,
                            parse_mode="Markdown")
    except:
        await msg.edit_text(chat_completion.choices[0].message.content, reply_markup=kb_gpt.gptExitDialog,
                            parse_mode=None)

    messages_list.append({"role": "assistant", "content": chat_completion.choices[0].message.content})
    databaseHistory.addHistory(message.from_user.id, json.dumps(messages_list))
#
