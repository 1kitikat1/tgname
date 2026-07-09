import os
import logging
import asyncio
import random
import string
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram import F

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ТОКЕН БОТА (ваш токен)
BOT_TOKEN = "8017305376:AAErAkhY-KZWA6IkC9Gryv_A3-SJpIpdZ0M"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Списки красивых никнеймов
BEAUTIFUL_WORDS = [
    "luna", "star", "moon", "sun", "sky", "dream", "angel", "devil",
    "fire", "ice", "storm", "shadow", "light", "dark", "crystal", "diamond",
    "royal", "queen", "king", "emperor", "legend", "myth", "eternal", "infinity",
    "serenity", "harmony", "destiny", "victory", "glory", "grace", "elegance",
    "aurora", "nova", "cosmos", "galaxy", "nebula", "stellar", "celestial"
]

RARE_CHARS = [
    "𝙰", "𝙱", "𝙲", "𝙳", "𝙴", "𝙵", "𝙶", "𝙷", "𝙸", "𝙹", "𝙺", "𝙻", "𝙼",
    "𝙽", "𝙾", "𝙿", "𝚀", "𝚁", "𝚂", "𝚃", "𝚄", "𝚅", "𝚆", "𝚇", "𝚈", "𝚉"
]

def generate_rare_username(length=6):
    """Генерация редкого никнейма"""
    word = random.choice(BEAUTIFUL_WORDS)
    if length > len(word):
        extra_chars = ''.join(random.choices(string.digits + string.ascii_lowercase, k=length - len(word)))
        username = word + extra_chars
    else:
        username = word[:length]
    
    rare_username = ''
    for char in username:
        if char.isalpha() and random.random() < 0.3:
            rare_char = random.choice(RARE_CHARS)
            rare_username += rare_char
        else:
            rare_username += char
    return rare_username

def generate_vip_username():
    """Генерация VIP никнейма"""
    prefixes = ['@', '$', '✦', '✧', '♛', '♚', '⚡', '🔥', '💎']
    prefix = random.choice(prefixes)
    word = random.choice(BEAUTIFUL_WORDS)
    suffix = ''.join(random.choices(string.digits, k=2))
    return f"{prefix}{word}{suffix}"

def check_username_rarity(username):
    """Проверка редкости никнейма"""
    score = 0
    if len(username) <= 4:
        score += 3
    elif len(username) <= 6:
        score += 2
    else:
        score += 1
    
    rare_count = sum(1 for char in username if char in RARE_CHARS)
    score += rare_count
    
    digit_count = sum(1 for char in username if char.isdigit())
    if digit_count > 0:
        score += 1
    
    for word in BEAUTIFUL_WORDS:
        if word in username.lower():
            score += 2
            break
    
    if score >= 6:
        return "⭐️ РЕДКИЙ"
    elif score >= 4:
        return "🌟 КРАСИВЫЙ"
    else:
        return "💫 ОБЫЧНЫЙ"

def format_username_for_sale(username):
    """Форматирование никнейма для продажи"""
    rarity = check_username_rarity(username)
    price = 0
    if "РЕДКИЙ" in rarity:
        price = random.randint(1000, 5000)
    elif "КРАСИВЫЙ" in rarity:
        price = random.randint(500, 999)
    else:
        price = random.randint(100, 499)
    
    return {
        'username': username,
        'rarity': rarity,
        'price': price,
        'date': datetime.now().strftime("%d.%m.%Y")
    }

def get_main_keyboard():
    """Главная клавиатура"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🎯 Найти ник", callback_data="find_username")
        ],
        [
            InlineKeyboardButton(text="💎 VIP никнеймы", callback_data="vip_usernames")
        ],
        [
            InlineKeyboardButton(text="💰 Мои никнеймы", callback_data="my_usernames")
        ],
        [
            InlineKeyboardButton(text="📋 ТУТОР", callback_data="tutor")
        ]
    ])
    return keyboard

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    """Обработчик команды /start"""
    welcome_text = f"""
🌟 <b>Добро пожаловать в магазин редких никнеймов!</b>

Я помогу вам найти и купить уникальные и красивые никнеймы для Telegram, Instagram и других соцсетей.

✨ <b>Что я умею:</b>
• 🎯 Генерировать редкие никнеймы
• 💎 Создавать VIP варианты
• 📊 Оценивать редкость никнеймов
• 💰 Выставлять на продажу

<b>Используйте кнопки ниже для навигации:</b>
    """
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard(),
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "find_username")
async def callback_find_username(callback: types.CallbackQuery):
    """Поиск никнеймов"""
    await callback.message.delete()
    
    usernames = []
    for _ in range(5):
        username = generate_rare_username(random.randint(4, 8))
        usernames.append(username)
    
    response = "<b>🔍 РЕЗУЛЬТАТЫ ПОИСКА:</b>\n\n"
    keyboard_buttons = []
    
    for i, username in enumerate(usernames, 1):
        data = format_username_for_sale(username)
        response += f"{i}. <code>{username}</code> - {data['rarity']} - 💰 {data['price']}₽\n"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"Купить {username}",
                callback_data=f"buy_{username}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="🔄 Новые никнеймы", callback_data="find_username"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "vip_usernames")
async def callback_vip_usernames(callback: types.CallbackQuery):
    """VIP никнеймы"""
    await callback.message.delete()
    
    vip_names = []
    for _ in range(3):
        vip_names.append(generate_vip_username())
    
    response = "<b>💎 VIP НИКНЕЙМЫ:</b>\n\n"
    keyboard_buttons = []
    
    for i, username in enumerate(vip_names, 1):
        data = format_username_for_sale(username)
        response += f"{i}. <code>{username}</code> - {data['rarity']} - 💰 {data['price'] * 2}₽\n"
        keyboard_buttons.append([
            InlineKeyboardButton(
                text=f"Купить {username}",
                callback_data=f"buy_{username}"
            )
        ])
    
    keyboard_buttons.append([
        InlineKeyboardButton(text="🔄 Обновить VIP", callback_data="vip_usernames"),
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
    ])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)
    
    await callback.message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "my_usernames")
async def callback_my_usernames(callback: types.CallbackQuery):
    """Мои никнеймы"""
    await callback.message.delete()
    
    response = """
<b>📦 ВАШИ НИКНЕЙМЫ:</b>

У вас пока нет купленных никнеймов.
Найдите никнейм через кнопку "Найти ник" или "VIP никнеймы"!

💡 <i>Совет: Чем короче и красивее никнейм, тем он дороже!</i>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🛒 Найти никнеймы", callback_data="find_username"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
        ]
    ])
    
    await callback.message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "tutor")
async def callback_tutor(callback: types.CallbackQuery):
    """Тутор по использованию бота"""
    await callback.message.delete()
    
    tutor_text = """
📚 <b>ТУТОРИАЛ ПО ИСПОЛЬЗОВАНИЮ БОТА</b>

<b>1. 🔍 ПОИСК НИКНЕЙМОВ</b>
• Нажмите "Найти ник" для генерации 5 случайных никнеймов
• Оцените их редкость и стоимость
• Выберите понравившийся и нажмите "Купить"

<b>2. 💎 VIP НИКНЕЙМЫ</b>
• Эксклюзивные никнеймы с премиум символами
• Более высокая стоимость, но уникальный дизайн
• Идеально для Instagram и Telegram

<b>3. 💰 ПРОДАЖА НИКНЕЙМОВ</b>
• Все никнеймы имеют оценку редкости
• Стоимость зависит от редкости и длины
• Вы можете перепродать никнеймы другим пользователям

<b>4. 📝 КАК ОЦЕНИВАЕТСЯ РЕДКОСТЬ:</b>
⭐️ РЕДКИЙ - короткий (до 4 символов) + спецсимволы
🌟 КРАСИВЫЙ - от 5 до 7 символов, есть смысл
💫 ОБЫЧНЫЙ - более 7 символов без спецсимволов

<b>5. 💡 СОВЕТЫ:</b>
• Короткие никнеймы ценятся выше
• Использование редких символов повышает стоимость
• Трендовые слова (Luna, Star, etc) всегда в цене

<b>6. 🔄 КАК КУПИТЬ:</b>
1. Найдите никнейм
2. Нажмите кнопку "Купить"
3. Следуйте инструкциям для оплаты
4. Получите никнейм в личные сообщения

<i>Бот работает круглосуточно! 🌙☀️</i>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")
        ]
    ])
    
    await callback.message.answer(
        tutor_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "back_to_main")
async def callback_back_to_main(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    await callback.message.delete()
    await cmd_start(callback.message)

@dp.callback_query(F.data.startswith("buy_"))
async def callback_buy(callback: types.CallbackQuery):
    """Покупка никнейма"""
    username = callback.data.replace("buy_", "")
    
    response = f"""
✅ <b>ВЫ ВЫБРАЛИ НИКНЕЙМ:</b> <code>{username}</code>

📊 <b>Информация о никнейме:</b>
• Редкость: {check_username_rarity(username)}
• Стоимость: {random.randint(100, 5000)}₽

<b>💰 Как оплатить:</b>
1. Переведите сумму на кошелек: @example_wallet
2. Напишите в поддержку: @support_bot
3. Получите никнейм в течение 5 минут

<i>После оплаты никнейм будет закреплен за вами!</i>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Я оплатил", callback_data="payment_done"),
            InlineKeyboardButton(text="⬅️ Назад", callback_data="find_username")
        ]
    ])
    
    await callback.message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.callback_query(F.data == "payment_done")
async def callback_payment_done(callback: types.CallbackQuery):
    """Подтверждение оплаты"""
    await callback.message.delete()
    
    response = """
✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА!</b>

Ваш никнейм отправлен в личные сообщения.
Проверьте папку "Запросы" если не видите сообщения.

📌 <b>Что дальше?</b>
• Сохраните никнейм
• Используйте в Telegram/Instagram
• Приятного использования! 🎉

<i>Если возникли проблемы, напишите @support_bot</i>
    """
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="back_to_main")
        ]
    ])
    
    await callback.message.answer(
        response,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@dp.message()
async def echo(message: types.Message):
    """Обработка текстовых сообщений"""
    await message.answer(
        "Используйте кнопки для навигации!",
        reply_markup=get_main_keyboard()
    )

async def main():
    """Запуск бота"""
    logger.info("Бот запускается...")
    
    # Удаляем вебхук, если он установлен
    await bot.delete_webhook(drop_pending_updates=True)
    
    # Запускаем polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())