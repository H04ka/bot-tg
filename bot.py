from aiogram import Router, F, html
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.enums.dice_emoji import DiceEmoji
import asyncio
import logging
from aiogram.types import LinkPreviewOptions
from aiogram import Bot, Dispatcher, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.client.session.aiohttp import AiohttpSession
import aiohttp
import ssl
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile, ReplyKeyboardMarkup
import random
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from aiogram.utils.formatting import Text, Bold
from keyboard import get_yes_no_kb



TOKEN = 
session = AiohttpSession()
session._connector_init = {'ssl': False}
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML), session=session)
# PROXY_URL = 

logging.basicConfig(level=logging.INFO)
dp = Dispatcher()

router = Router()

@router.message(Command("тест"))  # [2]
async def cmd_start(message:Message):
    await message.answer(
        "Вы довольны своей работай/учёбой   \n/да|/нет",
         reply_markup=get_yes_no_kb()
)
@router.message(F.text.lower() == "да")
async def answer_yes(message: Message):
    await message.answer(
        "Не хвастайся!",
        reply_markup=ReplyKeyboardRemove()
)

@router.message(F.text.lower() == "нет")
async def answer_yes(message: Message):
    await message.answer(
        "Жаль... \n иди поешь что ли",
        reply_markup=ReplyKeyboardRemove()
)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветствую в славянском шопе ''Тихий омут'', дорогой друг! \nЧтобы узнать команды пропиши /команды")

@dp.message(Command("команды"))
async def cmd_help(message: types.Message):
    await message.answer("\n Хотите шутку? напишите /анекдот \n ещё есть тесты /тест /тест1 | /go\n /кубик /вопрос /циферки /ссылочки \n /гифка /качели /random \n /привет (поздороваться с ботом)" )

@dp.message(Command("анекдот"))
async def cmd_start(message: types.Message):
    await message.answer("\nПростите, мимо вас не пробегало стадо баранов?\nЧё отстал?")

@dp.message(Command("тест1"))
async def cmd_test1(message: types.Message):
    await message.answer("Тестов не будет, разработчик устал")

async def cmd_test2(message: types.Message):
    await message.answer("ТЕСТОВ НЕ БУДЕТ! \nthere will be no tests! \nes wird keine Tests geben!")

#стикеры
@dp.message(Command("кубик"))
async def cmd_dice(message: types.Message):
    await message.answer_dice(emoji="🎲")

#супер важая тема
@dp.message(Command("вопрос"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="С пюрешкой"),
            types.KeyboardButton(text="Без пюрешки")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите способ подачи"
    )
    await message.answer("Как подавать котлеты?", reply_markup=keyboard)

@dp.message(F.text.lower() == "с пюрешкой")
async def with_puree(message: types.Message):
    await message.reply("Отличный выбор!")

@dp.message(F.text.lower() == "без пюрешки")
async def without_puree(message: types.Message):
    await message.reply("Так невкусно!")

#тыкалка на циферки
@dp.message(Command("циферки"))
async def reply_builder(message: types.Message):
    builder = ReplyKeyboardBuilder()
    for i in range(1, 17):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(4)
    await message.answer(
        "Выберите число:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )
#выдает все ссылки
@dp.message(Command("ссылочки"))
async def cmd_links(message: Message):
    links_text = (
        "https://youtu.be/P3YFIRDifQU?si=f_7Jak8r84J2Wgpe"
        "\n"
        "https://t.me/telegram"
    )
    options_1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(
        f"Нет превью ссылок\n{links_text}",
        link_preview_options=options_1
    )
#гифка
my_gif = FSInputFile("lol.gif")
@dp.message(Command("гифка"))
async def send_gif(message: types.Message):
    await message.answer_animation(my_gif)
    await asyncio.sleep(2)

@dp.message(Command("random"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Нажми меня",
        callback_data="random_value")
    )
    await message.answer(
        "ЕСЛИ ВЫПАЛО ЧИСЛО БОЛЬШЕ 95 ВЫ ГЕЙ",
        reply_markup=builder.as_markup()
    )

@dp.callback_query(F.data == "random_value")
async def send_random_value(callback: types.CallbackQuery):
    await callback.message.answer(str(random.randint(1, 100)))

user_data = {}

def get_keyboard():
    buttons = [
        [
            types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
            types.InlineKeyboardButton(text="+1", callback_data="num_incr")
        ],
        [types.InlineKeyboardButton(text="Подтвердить", callback_data="num_finish")]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def update_num_text(message: types.Message, new_value: int):
    await message.edit_text(
        f"Укажите число: {new_value}",
        reply_markup=get_keyboard()
    )

#числа +1 или минус 1. выдача результата
@dp.message(Command("качели"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())

@dp.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()

async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard()
        )
#приветствие 
@dp.message(Command("привет"))
async def cmd_hello(message: Message):
    content = Text(
        "Здарова, ебать мой лысый роботический череп ",
        Bold(message.from_user.full_name)
    )
    await message.answer(
        **content.as_kwargs()
    )

#викторина, тут без 100 гр колы не разобраться
current_answer = 0
score = 0

@dp.message(Command("викторина"))
async def cmd_qviz(message: types.Message):
    global current_answer, score
    current_answer = 0
    score = 0  #на этом я всё, викторина одолела меня, 

async def main():
    sslcontext = ssl.create_default_context()
    sslcontext.check_hostname = False
    sslcontext.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=sslcontext)) as session:
        await dp.start_polling(bot)
dp.message.register(cmd_test2, Command("тест2"))

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')

