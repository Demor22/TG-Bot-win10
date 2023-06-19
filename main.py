import telebot

TOKEN = '6151919437:AAExTd6miz_SAch-QXRHMqANQVQH8gF3SwQ'  # Замените на свой токен

# Загрузка ключей из файла
def load_keys():
    with open('keys.txt', 'r') as file:
        keys = file.read().splitlines()
    return keys

# Загрузка серийных ключей из файла
def load_serial_keys():
    with open('license.txt', 'r') as file:
        keys = file.read().splitlines()
    return keys

# Сохранение серийного ключа в файл восстановления
def save_serial_key(key):
    with open('recovery_licen.txt', 'a') as file:
        file.write(key + '\n')


# Создание реплей клавиатуры с доступными ключами
def create_keyboard(keys):
    keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for key in keys:
        keyboard.add(key)
    return keyboard

bot = telebot.TeleBot(TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    keys = load_keys()
    keyboard = create_keyboard(keys)
    bot.send_message(message.chat.id, 'Добро пожаловать! Выберите ключ для покупки:', reply_markup=keyboard)

# Обработчик выбора ключа
@bot.message_handler(func=lambda message: message.text in load_keys())
def handle_key_selection(message):
    key = message.text
    # Сохраняем выбранный ключ в контексте пользователя
    bot.send_message(message.chat.id, f'Вы выбрали ключ: {key}')
    # Запрашиваем количество лицензий
    bot.send_message(message.chat.id, 'Укажите количество лицензий:')
    bot.register_next_step_handler(message, handle_license_quantity)

# Обработчик указания количества лицензий
def handle_license_quantity(message):
    quantity = message.text
    # Рассчитываем стоимость на основе количества лицензий
    try:
        quantity = int(quantity)
        price = 500 * quantity
        card_number = '2200700723055777'
        nickname = '@AsaselD'
        # Отправляем информацию о стоимости и реквизитах для оплаты
        reply_text = f'Стоимость {quantity} лицензий: {price} руб.\n' \
                     f'Оплатите на карту: {card_number}\n' \
                     f'После оплаты направьте оператору {nickname} скриншот оплаты и он выдаст вам лицензионный ключ.'
        bot.send_message(message.chat.id, reply_text)
    except ValueError:
        bot.send_message(message.chat.id, 'Некорректное количество лицензий.')

# Обработчик команды /give
@bot.message_handler(commands=['give'])
def handle_give(message):
    # Проверяем ID пользователя
    if message.from_user.id == 185156683:
        serial_keys = load_serial_keys()
        if serial_keys:
            key = serial_keys.pop(0)  # Выбираем первый ключ из списка и удаляем его
            save_serial_key(key)  # Сохраняем выданный ключ в файл recovery_licen.txt

            # Обновляем файл license.txt
            with open('license.txt', 'w') as file:
                for serial_key in serial_keys:
                    file.write(serial_key + '\n')

            bot.send_message(message.chat.id, f'Вот серийный ключ для вас: {key}')
        else:
            bot.send_message(message.chat.id, 'Нет доступных ключей.')
    else:
        bot.send_message(message.chat.id, 'Недостаточно прав для выполнения этой команды.')


bot.polling()


