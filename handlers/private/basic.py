"""Данный файл является аналогом basic.py в /groups
Сделанно это для того, чтоб не мешать все в одном хендлере.
Все хендлеры созданы для личных сообщнений и все изменения
будут видны лишь там"""

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold

from filters import IsPrivate
from keyboards.inline import start_markup


async def start(message: types.Message):
    """Хендлер на команду /start
    Приветствует пользователя.
    Используется в личных сообщениях"""

    # Отправляем приветствие
    await message.answer(
        f"Привет, {hbold(message.from_user.full_name)}\n\n"
        "Я простой чат-менеджер.\n"
        "Для полного функционала добавь меня в группу "
    )


async def help_cmd(message: types.Message):
    """
    Хендлер на команду /help
    Выводит список комманд.
    Используется в личных сообщениях
    """

    # Создаем текст сообщения
    text = """{header1}
/start - Начать диалог со мной
/help - Помощь по комманде

{header2}
/gay [цель*] -  Тест на гея
/biba - Проверить бибу
/roll - Случайное число
/metabolism - Узнать свою суточную норму калорий

{warning}
""".format(
        header1=hbold("Основные комманды"),
        header2=hbold("Другие комманды"),
        warning=hbold("В группах функционал бота может отличаться.\n"
                      "* - необязательный аргумент"))

    # Отправляем список комманд
    await message.answer(text)


async def callback_handler(query: types.CallbackQuery):
    """
    CallBack хендлер, который проверяет
    на что нажал пользователь
    """

    # Присваиваем query дату переменной
    answer_data = query.data

    # Отвечаем пользователю, чтоб возле инлайн кнопки
    # не было "часиков", это нужно делать даже когда нечего сказать
    # P.S. пользователь сообщение не увидит без аргумента show_alert=True
    await query.answer()

    # Выводим список комманд, если пользователь нажал на кнопку
    # со списком комманд, которая имеет CB дату "help"
    if answer_data == "help":
        await help_cmd(query.message)


def register_basic_handlers(dp: Dispatcher):
    """Регистрация всех хендлеров для личных сообщений"""

    dp.register_message_handler(start, IsPrivate(), Command("start", prefixes="/"))
    dp.register_message_handler(help_cmd, IsPrivate(), Command("help", prefixes="/"))
    dp.register_callback_query_handler(callback_handler, text="help")
