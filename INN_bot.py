import logging
import asyncio
import requests
from aiogram import Bot, Dispatcher, types, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router
from bs4 import BeautifulSoup

TOKEN = "6908856914:AAH1DceujYEnrBYbDsokw88PC-lUKO3UaNg"

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
logging.basicConfig(level=logging.INFO)


# Функция для парсинга адреса по ИНН
def get_address_by_inn(inn):
    url = f"https://orginfo.uz/search/all/?q={inn}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        address_tag = soup.find("p", class_="text-body-tertiary mb-0")

        if address_tag:
            return ', '.join(filter(None, map(str.strip, address_tag.text.split('\n'))))
        else:
            return "Адрес не найден. Возможно, ИНН неверен."
    else:
        return "Ошибка при получении данных. Попробуйте позже."


# Обработчик команды /start
@router.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Привет! Отправьте мне ИНН организации, и я найду её адрес.")


# Обработчик сообщений с ИНН
@router.message(F.text)
async def handle_inn(message: Message):
    inn = message.text.strip()
    if inn.isdigit() and len(inn) in [9, 10]:  # Проверка формата ИНН
        address = get_address_by_inn(inn)
        await message.reply(f"Адрес организации:\n{address}")
    else:
        await message.reply("Пожалуйста, введите корректный ИНН (9 или 10 цифр).")


async def main():
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
