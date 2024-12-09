from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню с кнопками "Привет" и "Пока"
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Привет"),
                KeyboardButton(text="Пока")
            ]
        ],
        resize_keyboard=True
    )

# Инлайн-кнопки с URL-ссылками
def links_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Новости", url="https://news.example.com")],
            [InlineKeyboardButton(text="Музыка", url="https://music.example.com")],
            [InlineKeyboardButton(text="Видео", url="https://video.example.com")]
        ]
    )

# Кнопка "Показать больше"
def dynamic_button():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Показать больше", callback_data="show_more")]
        ]
    )

# Кнопки "Опция 1" и "Опция 2"
def dynamic_options():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Опция 1", callback_data="option_1")],
            [InlineKeyboardButton(text="Опция 2", callback_data="option_2")]
        ]
    )
