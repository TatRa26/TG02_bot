import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from gtts import gTTS
from googletrans import Translator
from dotenv import load_dotenv
from keyboards import main_menu, links_menu, dynamic_button, dynamic_options

# Загрузка токена из файла .env
load_dotenv()
API_TOKEN = os.getenv("API_TOKEN")

if not API_TOKEN:
    raise ValueError("Токен не найден! Убедитесь, что он добавлен в файл .env.")

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Инициализация переводчика
translator = Translator()

# Создаем папку для фотографий
os.makedirs("img", exist_ok=True)

# Обработчик команды /start
@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.answer(
        "Добро пожаловать! Выберите действие из меню:",
        reply_markup=main_menu()
    )

# Обработка кнопок "Привет" и "Пока"
@dp.message(F.text == "Привет")
async def greet_user(message: Message):
    await message.answer(f"Привет, {message.from_user.first_name}!")

@dp.message(F.text == "Пока")
async def goodbye_user(message: Message):
    await message.answer(f"До свидания, {message.from_user.first_name}!")

# Обработчик команды /links
@dp.message(Command("links"))
async def send_links(message: Message):
    await message.answer("Выберите ссылку:", reply_markup=links_menu())

# Обработчик команды /dynamic
@dp.message(Command("dynamic"))
async def show_dynamic(message: Message):
    await message.answer("Выберите опцию:", reply_markup=dynamic_button())

# Обработка нажатия на кнопку "Показать больше"
@dp.callback_query(F.data == "show_more")
async def show_more_options(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=dynamic_options())

# Обработка нажатий на кнопки "Опция 1" и "Опция 2"
@dp.callback_query(F.data.in_({"option_1", "option_2"}))
async def handle_option(callback: CallbackQuery):
    option_text = "Опция 1" if callback.data == "option_1" else "Опция 2"
    await callback.message.answer(f"Вы выбрали: {option_text}")

# Обработчик команды /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "📋 Мои команды:\n"
        "/start - Начало работы с ботом\n"
        "/help - Список возможностей\n"
        "/links - Ссылки на ресурсы\n"
        "/dynamic - Динамические кнопки\n"
        "📷 Отправьте фото, чтобы я сохранил его в папке img\n"
        "🗣 Используйте команду /voice <текст> для создания голосового сообщения\n"
        "🌍 Используйте команду /translate <текст> для перевода на английский язык"
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

# Главная асинхронная функция запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





