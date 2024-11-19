import asyncio
import logging
import re  # Для регулярных выражений
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
import datetime
import re 

# Путь к файлу пользователей
USERS_FILE = "users.txt"

users = {}

# Установим уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Ваш API Token
API_TOKEN = "7781171058:AAGePHekHN46_O6TpCA3-XqupVcjWPc7TyQ"

# ID администратора
ADMIN_ID = 866385484

# Функция для загрузки пользователей из файла
def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            for line in file:
                user_id, date_str = line.strip().split(',')
                users[int(user_id)] = datetime.datetime.fromisoformat(date_str)
    except FileNotFoundError:
        logging.warning(f"{USERS_FILE} не найден. Будет создан новый.")

def save_user(user_id, join_date):
    with open(USERS_FILE, "a") as file:
        file.write(f"{user_id},{join_date.strftime('%Y-%m-%d %H:%M:%S')}\n")
      

# Функция для сохранения пользователей в файл
def save_users():
    with open(USERS_FILE, 'w') as file:
        for user_id, date in users.items():
            file.write(f"{user_id},{date.isoformat()}\n")



# Путь к изображению
IMAGE_PATH_1 = "images/1.jpg"
IMAGE_PATH_2 = "images/2.jpg"
IMAGE_PATH_3 = "images/3.jpg"  # Новое изображение
IMAGE_PATH_4 = "images/4.jpg"

# Словарь для хранения последних сообщений для каждого чата
last_messages = {}

# Тексты сообщений на разных языках
GAME_SELECT_MESSAGE = {
    'ru': "Выберите игру в которую хотите поиграть 🕹",
    'en': "Select the game you want to play 🕹"
}

WELCOME_MESSAGES = {
    'ru': "👋Добро пожаловать в Matrix|Signal!\n\n"
          "🔥 ЛУЧШИЙ бот, который предоставляет ПОЛНУЮ аналитику вашего игрового аккаунта с сигналами, помогающими выйти на стабильный доход с казино.\n\n"
          "💠 Проект основан на Искусственном Интеллекте Reationale.\n\n"
          "",
    'en': "👋Welcome to Matrix|Signal!\n\n"
          "🔥 THE BEST bot that provides COMPLETE analytics of your gaming account with signals that help you achieve stable income from the casino.\n\n"
          "💠This project is based on Rational AI.\n\n"
}

NEXT_BUTTONS = {
    'ru': "Дальше",
    'en': "Next"
}

SECOND_MESSAGE = {
    'ru': "📛 Онлайн казино — это скрипт, из-за которого 75% игроков проигрывают, а 25% выигрывают.\n"
          "⚜️ Мы с командой нашли способ обмануть казино через hash вашей игры.\n"
          "🎯 Совместно с сигналами от бота вы можете выйти на доход от 5000$ в месяц\n"
          "💠Если у вас уже есть аккаунт, то нужен новый. Это нужно для того что бы наш бот подвязался к вашему персональному ID.",
    
    'en': "📛 Online casinos are a script that causes 75% of players to lose, while 25% win.\n"
          "⚜️ My team and I found a way to outsmart the casino through the hash of your game.\n"
          "🎯 Together with signals from the bot, you can achieve an income of $5,000 per month.\n"
          "💠If you already have an account, you'll need a new one. This is required so that our bot can link to your personal ID."
}

ACCOUNT_MESSAGE = {
    'ru': "💠Создайте новый аккаунт, чтобы бот мог подключиться к вашему ID.",
    'en': "💠Create a new account so the bot can connect to your ID."
}

CREATE_ACCOUNT_BUTTON = {
    'ru': "Создать аккаунт",
    'en': "Create Account"
}

REGISTRATION_MESSAGE = {
    'ru':
          "🔷 1. Зарегистрируйтесь на сайте 1WIN по кнопке ниже (используйте промокод MTRX , он даст вам 500% к депозиту)\n"
          "🔷 2. После успешной регистрации скопируйте ваш ID на сайте (Пример на фото).\n"
          "🔷 3. Отправьте его боту в ответ на это сообщение (только цифры)!\n"
          "👨‍💻Если у вас есть вопросы, то напишите нашему менеджеру - @matrix_support",
    
    'en': "🔷 1. Register on the 1WIN website using the button below (use promo code MTRX for a 500% deposit bonus)\n"
          "🔷 2. After successful registration, copy your ID on the site (Example in the photo).\n"
          "🔷 3. Send it to the bot in response to this message (numbers only)!\n"
          "👨‍💻If you have any questions, contact our manager - @matrix_support"
}

REGISTRATION_BUTTON = {
    'ru': "📲Регистрация",
    'en': "📲Registration"
}

# Добавляем сообщение для ввода ID
ID_PROMPT_MESSAGES = {
    'ru': "💠Введите свой ID (только цифры):",
    'en': "💠Enter your ID (numbers only):"
}

# Функция приветственного сообщения с выбором языка
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    current_time = datetime.datetime.now()
    
    # Если пользователь новый, добавляем его с текущей датой
    if user_id not in users:
        users[user_id] = current_time
        save_user(user_id, current_time)  # Сохраняем пользователя в файл
        print(f"Новый пользователь добавлен: {user_id}")
    else:
        print(f"Пользователь уже существует: {user_id}")
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data='ru'),
            InlineKeyboardButton("🇬🇧 English", callback_data='en')
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    # Отправляем сообщение с изображением
    with open(IMAGE_PATH_4, 'rb') as photo:
        await update.message.reply_photo(
            photo=photo,
            caption="Выберите язык / Choose a language:",
            reply_markup=reply_markup
        ) 

# Функция удаления предыдущих сообщений
async def delete_last_message(chat_id):
    if chat_id in last_messages:
        try:
            await last_messages[chat_id].delete()
        except Exception as e:
            logging.error(f"Error deleting message: {e}")

# Функция отправки сообщения с кнопкой "Дальше"
async def send_welcome_message(update: Update, language: str):
    await delete_last_message(update.message.chat.id)  # Удаляем предыдущее сообщение

    keyboard = [
        [
            InlineKeyboardButton(NEXT_BUTTONS[language], callback_data=f'next_message_{language}')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение с картинкой и кнопкой
    with open(IMAGE_PATH_1, 'rb') as photo:
        message = await update.message.reply_photo(
            photo=photo,
            caption=WELCOME_MESSAGES[language],
            reply_markup=reply_markup
        )

    # Сохраняем ссылку на сообщение для удаления
    last_messages[update.message.chat.id] = message

# Функция отправки второго сообщения с задержкой и эффектом печати
async def send_second_message(query, language: str):
    await query.answer()

    # Удаляем предыдущее сообщение
    await delete_last_message(query.message.chat.id)

    # Отправляем первое сообщение "‼️"
    await query.message.reply_text("‼️")
    
    # Задержка 2 секунды
    await asyncio.sleep(2)
    
    # Отправка следующего сообщения с текстом и кнопкой "Дальше"
    keyboard = [
        [
            InlineKeyboardButton(NEXT_BUTTONS[language], callback_data=f'account_info_{language}')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    print(f"Language for second message: {language}")  # Отладочное сообщение
    message = await query.message.reply_text(
        SECOND_MESSAGE[language],
        reply_markup=reply_markup
    )

    # Сохраняем ссылку на сообщение для удаления
    last_messages[query.message.chat.id] = message

# Функция отправки сообщения о создании аккаунта
async def send_account_message(update: Update, language: str):
    query = update.callback_query
    await query.answer()

    # Удаляем предыдущее сообщение
    await delete_last_message(query.message.chat.id)

    # Получаем язык из callback_data
    chosen_language = query.data.split('_')[-1]
    print(f"Chosen language for account message: {chosen_language}")  # Отладочное сообщение

    # Кнопка "Создать аккаунт"
    keyboard = [
        [
            InlineKeyboardButton(CREATE_ACCOUNT_BUTTON[chosen_language], callback_data='create_account_' + chosen_language)
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем сообщение о создании аккаунта
    message = await query.message.reply_text(
        ACCOUNT_MESSAGE[chosen_language],
        reply_markup=reply_markup
    )

    # Сохраняем ссылку на сообщение для удаления
    last_messages[query.message.chat.id] = message

# Функция отправки сообщения с инструкциями по регистрации
async def send_registration_instructions(query, language: str, context: ContextTypes.DEFAULT_TYPE):
    await query.answer()

    # Удаляем предыдущее сообщение
    await delete_last_message(query.message.chat.id)

    # Отправляем первое сообщение "📝"
    await query.message.reply_text("📝")
    
    # Задержка 2 секунды
    await asyncio.sleep(2)
    
    # Отправка сообщения с инструкциями и кнопкой-ссылкой
    keyboard = [
        [
            InlineKeyboardButton(REGISTRATION_BUTTON[language], url="https://1wxxlb.com/casino/list?open=register&p=xpxf")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем, какой язык используется
    print(f"Language for registration instructions: {language}")  # Отладочное сообщение

    with open(IMAGE_PATH_2, 'rb') as photo:
        message = await query.message.reply_photo(
            photo=photo,
            caption=REGISTRATION_MESSAGE[language],
            reply_markup=reply_markup
        )

        # Сохраняем ссылку на сообщение для удаления
        last_messages[query.message.chat.id] = message

    # Задержка 3 секунды перед запросом ID
    await asyncio.sleep(3)
    message = await query.message.reply_text(
        "💠Введите свой ID (только цифры):" if language == 'ru' else "💠Enter your ID (numbers only):"
    )

      # Ожидание ввода ID
    context.user_data['awaiting_id'] = True  # Установка флага ожидания ID

# Функция проверки введённого ID
def is_valid_id(user_id: str) -> bool:
    return bool(re.match(r'^9\d{7}$', user_id))

# Функция обработки выбора языка
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Сохранение выбранного языка и отправка следующего сообщения
    chosen_language = query.data
    print(f"Chosen language: {chosen_language}")  # Отладочное сообщение
    await send_welcome_message(query, chosen_language)

# Функция обработки нажатия на кнопку "Дальше" для второго сообщения
async def next_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chosen_language = query.data.split('_')[-1]
    
    # Отправка второго сообщения с задержкой и эффектом печати
    await send_second_message(query, chosen_language)

# Функция обработки нажатия на кнопку "Создать аккаунт"
async def create_account(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chosen_language = query.data.split('_')[-1]

    # Отправка инструкций по регистрации
    await send_registration_instructions(query, chosen_language, context)  # Передаем context

# Функция обработки введенного ID
async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text.strip()
    
    # Получаем статус отправленного сообщения
    already_sent_success_message = context.user_data.get('already_sent_success_message', False)

    if is_valid_id(user_id):
        await update.message.reply_text("✅")
        context.user_data['already_sent_success_message'] = True  # Устанавливаем флаг, что сообщение "✅" было отправлено

        # Функция обработки выбора языка
async def language_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Сохранение выбранного языка
    chosen_language = query.data
    context.user_data['language'] = chosen_language  # Сохраняем язык в контексте пользователя
    print(f"Chosen language: {chosen_language}")  # Отладочное сообщение
    await send_welcome_message(query, chosen_language)

# Функция обработки введенного ID
async def handle_user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.text.strip()
    
    # Получаем статус отправленного сообщения
    already_sent_success_message = context.user_data.get('already_sent_success_message', False)

    if is_valid_id(user_id):
        await update.message.reply_text("✅")
        context.user_data['already_sent_success_message'] = True  # Устанавливаем флаг, что сообщение "✅" было отправлено

        # Определяем язык из контекста
        language = context.user_data.get('language', 'en')

        # Отправляем сообщение с кнопками и изображением
        keyboard = [
            [
                InlineKeyboardButton("⭐️Mines", url="https://t.me/matrix_signal_bot/mines"),
                InlineKeyboardButton("💣BomBucks", url="https://t.me/matrix_signal_bot/bombucks"),
            ],
            [
                InlineKeyboardButton("🚀LuckyJet", url="https://t.me/matrix_signal_bot/lucky"),
                InlineKeyboardButton("💀BrawlPirates", url="https://t.me/matrix_signal_bot/brawl"),
            ],
            [
                InlineKeyboardButton("👨‍🦯‍➡️RoyalMines", url="https://t.me/matrix_signal_bot/royal"),
                InlineKeyboardButton("🛩Aviator", url="https://t.me/matrix_signal_bot/aviator"),
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Получаем текст сообщения на выбранном языке
        caption = GAME_SELECT_MESSAGE.get(language, GAME_SELECT_MESSAGE['en'])

        with open(IMAGE_PATH_3, 'rb') as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                reply_markup=reply_markup
            )

        # Здесь можно добавить дополнительные действия после успешного ввода ID
    else:
        if not already_sent_success_message:  # Проверяем, было ли отправлено сообщение "✅"
            await update.message.reply_text("❌")


async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:  # Проверяем, является ли пользователь администратором
        context.user_data['is_admin'] = True  # Устанавливаем флаг администратора
        await update.message.reply_text("Вы находитесь в админ-панели!")
        await show_admin_panel(update, context)  # Показать панель администратора
    else:
        await update.message.reply_text("У вас нет доступа к админ-панели.")

        
# Добавляем обработчик для команды /admin
async def handle_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await check_admin(update, context)


def admin_panel_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊Статистика", callback_data="statistics")]
    ]
    return InlineKeyboardMarkup(keyboard)

async def show_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('is_admin', False):
        commands = (
            "/broadcast <текст> - Рассылка текстового сообщения всем пользователям.\n"
            "Фотография + текст - Отправка фотографии всем пользователям.\n"
            "/admin_panel - Показать панель администратора с командами и статистикой.\n"
            "/statistics - Просмотр статистики пользователей.\n"
        )
        stats = await get_statistics()
        response_message = (
            "👨‍💼 Панель администратора:\n"
            f"{commands}\n"
            f"{stats}"
        )
        await update.message.reply_text(response_message)
    else:
        await update.message.reply_text("Вы не администратор.")

async def statistics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('is_admin', False):
        stats = await get_statistics()
        await update.message.reply_text(stats)
    else:
        await update.message.reply_text("Вы не администратор.")

async def get_statistics():
    now = datetime.datetime.now()
    
    # За сутки
    daily_users = len([user_id for user_id, date in users.items() if (now - date).days < 1])
    
    # За месяц
    monthly_users = len([user_id for user_id, date in users.items() if (now - date).days < 30])
    
    # Общее количество
    total_users = len(users)
    
    return (
        f"📊 Статистика:\n"
        f"За последние сутки: {daily_users} пользователей\n"
        f"За последний месяц: {monthly_users} пользователей\n"
        f"Всего пользователей: {total_users}"
    )

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('is_admin', False):
        if context.args:
            message_text = ' '.join(context.args)
            print(f"Рассылаем сообщение: '{message_text}' для {len(users)} пользователей.")
            
            if not users:
                print("Ошибка: нет пользователей для рассылки.")
                await update.message.reply_text("Нет пользователей для рассылки.")
                return
            
            for user_id in users:
                try:
                    # Отправляем текстовое сообщение
                    await context.bot.send_message(chat_id=user_id, text=message_text)
                    print(f"Сообщение отправлено пользователю {user_id}")
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user_id}: {e}")
                    
            await update.message.reply_text("Сообщение разослано!")
        else:
            await update.message.reply_text("Пожалуйста, введите сообщение для рассылки. Пример: /broadcast Ваше сообщение")
    else:
        await update.message.reply_text("Вы не администратор.")

async def broadcast_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('is_admin', False):
        if update.message.photo:
            photo = update.message.photo[-1]  # Получаем наибольшее качество фотографии
            caption = update.message.caption or ""  # Получаем подпись к фотографии, если есть
            
            print(f"Рассылаем фотографию для {len(users)} пользователей.")
            
            if not users:
                print("Ошибка: нет пользователей для рассылки.")
                await update.message.reply_text("Нет пользователей для рассылки.")
                return
            
            for user_id in users:
                try:
                    # Отправляем фотографию
                    await context.bot.send_photo(chat_id=user_id, photo=photo.file_id, caption=caption)
                    print(f"Фотография отправлена пользователю {user_id}")
                except Exception as e:
                    print(f"Ошибка отправки фотографии пользователю {user_id}: {e}")
                    
            await update.message.reply_text("Фотография разослана!")
        else:
            await update.message.reply_text("Пожалуйста, отправьте фотографию для рассылки.")
    else:
        await update.message.reply_text("Вы не администратор.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "statistics":
        stats = await get_statistics()
        await query.message.reply_text(stats)

async def statistics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('is_admin', False):
        stats = await get_statistics()
        await update.message.reply_text(stats)
    else:
        await update.message.reply_text("Вы не администратор.")
        

# Основная функция
def main():
    load_users()  # Загружаем пользователей из файла
    app = ApplicationBuilder().token(API_TOKEN).build()



    # Обработчики команд и callback'ов
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(language_choice, pattern='^(ru|en)$'))
    app.add_handler(CallbackQueryHandler(next_message, pattern='^next_message_(ru|en)$'))
    app.add_handler(CallbackQueryHandler(send_account_message, pattern='^account_info_(ru|en)$'))
    app.add_handler(CallbackQueryHandler(create_account, pattern='^create_account_(ru|en)$'))
    app.add_handler(CommandHandler("admin", admin))
    app.add_handler(CommandHandler("admin", handle_command))  # Добавьте этот обработчик для команды /admin
    app.add_handler(CallbackQueryHandler(show_admin_panel, pattern='^admin_panel$'))
    app.add_handler(CommandHandler("admin_panel", show_admin_panel))  # Новая команда для панели администратора
    app.add_handler(CommandHandler("statistics", statistics_command))
    app.add_handler(CommandHandler("broadcast", broadcast)) 
    app.add_handler(MessageHandler(filters.PHOTO & ~filters.COMMAND, broadcast_photo))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    
    # Обработчик для ввода ID
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_id))

    # Запуск бота
    app.run_polling()

if __name__ == "__main__":
    main()
