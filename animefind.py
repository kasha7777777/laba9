import telebot

# Вставьте свой токен Telegram API
TOKEN = '5800570790:AAG_R4qI94w3YNTFfQpPrcHR1AUmuEf9zy0'

bot = telebot.TeleBot(TOKEN)
user_lists = {}  # Словарь для хранения списков пользователей
user_selections = {}  # Словарь для хранения выборов пользователей

@bot.message_handler(commands=['start', 'help'])
def start(message):
    chat_id = message.chat.id
    help_text = "Привет! Я бот для ведения списка просмотра.\n\n" \
                "Список доступных команд:\n" \
                "/help - показать список команд\n" \
                "/add - добавить элемент в список\n" \
                "/series - добавить заметку к элементу в списке\n" \
                "/show - показать список"

    bot.send_message(chat_id, help_text)

@bot.message_handler(commands=['add'])
def add_item(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Введите элемент для добавления в список:")
    bot.register_next_step_handler(msg, process_item)

def process_item(message):
    chat_id = message.chat.id
    item = message.text

    if chat_id not in user_lists:
        user_lists[chat_id] = []

    user_list = user_lists[chat_id]
    item_number = len(user_list) + 1
    user_list.append(f"{item_number}. {item}")

    bot.send_message(chat_id, f"Элемент '{item}' успешно добавлен в список.")

@bot.message_handler(commands=['series'])
def add_series(message):
    chat_id = message.chat.id
    if chat_id in user_lists and user_lists[chat_id]:
        list_text = "\n".join(user_lists[chat_id])
        msg = bot.send_message(chat_id, f"Выберите номер элемента из списка:\n{list_text}")
        bot.register_next_step_handler(msg, process_series)
    else:
        bot.send_message(chat_id, "Ваш список пуст.")

def process_series(message):
    chat_id = message.chat.id
    selected_item_number = message.text

    if chat_id in user_lists and user_lists[chat_id]:
        try:
            selected_item_index = int(selected_item_number.split('.')[0]) - 1
            user_list = user_lists[chat_id]

            if selected_item_index >= 0 and selected_item_index < len(user_list):
                user_selections[chat_id] = selected_item_index

                msg = bot.send_message(chat_id, "Введите заметку, которую нужно добавить к элементу:")
                bot.register_next_step_handler(msg, process_note)
            else:
                bot.send_message(chat_id, "Некорректный номер элемента. Попробуйте снова.")
        except ValueError:
            bot.send_message(chat_id, "Некорректный номер элемента. Попробуйте снова.")
    else:
        bot.send_message(chat_id, "Ваш список пуст.")

def process_note(message):
    chat_id = message.chat.id
    note_text = message.text

    if chat_id in user_lists and chat_id in user_selections:
        selected_item_index = user_selections[chat_id]
        user_list = user_lists[chat_id]

        selected_item = user_list[selected_item_index]
        note_added_item = f"{selected_item} ({note_text})"
        user_list[selected_item_index] = note_added_item

        bot.send_message(chat_id, f"Заметка успешно добавлена к элементу '{selected_item}'.")
        user_selections.pop(chat_id)  # Удаляем выбор пользователя
    else:
        bot.send_message(chat_id, "Что-то пошло не так. Попробуйте снова.")

@bot.message_handler(commands=['show'])
def show_list(message):
    chat_id = message.chat.id

    if chat_id in user_lists and user_lists[chat_id]:
        list_text = "\n".join(user_lists[chat_id])
        bot.send_message(chat_id, f"Ваш список:\n{list_text}")
    else:
        bot.send_message(chat_id, "Ваш список пуст.")

bot.polling()
