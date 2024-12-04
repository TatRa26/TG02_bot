import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from gtts import gTTS
from googletrans import Translator
from dotenv import load_dotenv
from aiogram.filters import Command

# Загрузка токена из файла .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что он добавлен в файл .env.")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Создаем папку для фотографий, если она отсутствует
os.makedirs("img", exist_ok=True)

# Инициализация переводчика
translator = Translator()


# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Привет! Я бот с несколькими функциями:\n"
        "1️⃣ Сохраняю фотографии.\n"
        "2️⃣ Генерирую голосовые сообщения из текста.\n"
        "3️⃣ Перевожу текст на английский язык.\n\n"
        "Используй команду /help для списка возможностей!"
    )


# Обработчик команды /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📋 Мои команды:\n"
        "/start - Начало работы с ботом\n"
        "/help - Описание возможностей\n"
        "📷 Отправьте фото, чтобы я сохранил его в папке img\n"
        "🗣 Используйте команду /voice <текст> для создания голосового сообщения\n"
        "🌍 Используйте команду /translate <текст> для перевода на английский язык\n"
        "🎤 Используйте команду /send_voice для получения голосового сообщения"
    )


# Обработка фотографий
@dp.message(F.photo)
async def save_photo(message: Message):
    photo = message.photo[-1]  # Берем фотографию самого высокого качества
    file_path = await bot.get_file(photo.file_id)

    # Сохраняем фото
    destination = f"img/{photo.file_id}.jpg"
    await bot.download_file(file_path.file_path, destination)

    await message.answer("Фото сохранено в папке 'img'!")


# Генерация голосового сообщения из текста
@dp.message(Command("voice"))
async def create_voice(message: Message):
    args = message.text[len("/voice "):].strip()  # Извлекаем текст после команды
    if not args:
        await message.answer("Пожалуйста, добавьте текст после команды /voice.")
        return

    # Генерация голосового сообщения
    tts = gTTS(text=args, lang='ru')
    audio_path = "voice_message.ogg"
    tts.save(audio_path)

    # Отправляем голосовое сообщение
    voice_file = FSInputFile(audio_path)
    await message.answer_voice(voice_file)

    # Удаляем временный файл
    os.remove(audio_path)


# Перевод текста на английский язык
@dp.message(Command("translate"))
async def translate_text(message: Message):
    args = message.text[len("/translate "):].strip()  # Извлекаем текст после команды
    if not args:
        await message.answer("Пожалуйста, добавьте текст для перевода.")
        return

    translation = translator.translate(args, src='auto', dest='en')
    await message.answer(f"Перевод:\n{translation.text}")


# Новая команда для отправки голосового сообщения
@dp.message(Command("send_voice"))
async def send_voice(message: Message):
    text_to_speak = "Привет, я отправляю тебе голосовое сообщение!"

    # Генерация голосового сообщения
    tts = gTTS(text=text_to_speak, lang='ru')
    audio_path = "hello_message.ogg"
    tts.save(audio_path)

    # Отправка голосового сообщения
    voice_file = FSInputFile(audio_path)
    await message.answer_voice(voice_file)

    # Удаление временного файла
    os.remove(audio_path)


# Главная асинхронная функция запуска бота
async def main():
    # Удаляем старые обновления и запускаем диспетчер
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())





