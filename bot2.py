import telebot
from telebot import types
import time

bot=telebot.TeleBot('7578496619:AAFOnrG9l_qL6yRdjd0TGvWWjr4eQGdIdWU')

users = {}


def register_user(chat_id, name, surname, grade):
    users[chat_id] = {
        'name': name,
        'surname': surname,
        'grade': grade,
        'completed_courses': []  
    }

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Пожалуйста, зарегистрируйтесь. Введите ваше имя:")
    bot.register_next_step_handler(message, process_name_step)

def process_name_step(message):
    name = message.text
    bot.send_message(message.chat.id, "Введите вашу фамилию:")
    bot.register_next_step_handler(message, process_surname_step, name)

def process_surname_step(message, name):
    surname = message.text
    bot.send_message(message.chat.id, "Введите ваш класс (5-11):")
    bot.register_next_step_handler(message, process_grade_step, name, surname)

def process_grade_step(message, name, surname):
    try:
        grade = int(message.text)
        if grade < 5 or grade > 11:
            raise ValueError("Курс не предусмотрен для младшего звена школы!")
        
        register_user(message.chat.id, name, surname, grade)
        
        markup = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="Разработчик", url="https://t.me/prost_lolkin") 
        markup.add(button)
        
        bot.send_message(message.chat.id, f"Вы успешно зарегистрировались на курс по нейросетям, {name} {surname}!", reply_markup=markup)
        show_course_options(message)

    except ValueError as e:
        bot.send_message(message.chat.id, str(e))
        bot.send_message(message.chat.id, "Введите ваш класс (5-11):")
        bot.register_next_step_handler(message, process_grade_step, name, surname)

def show_course_options(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Что такое нейросети?", "Примеры использования", "Как они работают?", "Машинное обучение - это…"]
    markup.add(*buttons)
    
    bot.send_message(message.chat.id, "Выберите курс:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text in ["Что такое нейросети?", "Примеры использования", "Как они работают?", "Машинное обучение - это…"])
def handle_course_selection(message):
    chat_id = message.chat.id
    completed_courses = users[chat_id]['completed_courses']

    if message.text == "Что такое нейросети?":  # Курс 1
        bot.send_message(chat_id, "Нейросети – это как упрощенная модель человеческого мозга, состоящая из множества соединенных между собой 'нейронов'. Они учатся распознавать закономерности в данных...")
        time.sleep(3)  
        completed_courses.append("Что такое нейросети?")
        check_completion(chat_id)

    elif message.text == "Примеры использования":  # Курс 2
        bot.send_message(chat_id, "Распознавание лиц: В смартфонах и системах безопасности.")
        time.sleep(3)  
        bot.send_message(chat_id, "Автоматический перевод: Google Translate и другие переводчики.")
        time.sleep(3)  
        bot.send_message(chat_id, "Рекомендации фильмов и музыки: Netflix, Spotify.")
        time.sleep(3)  
        bot.send_message(chat_id, "Автопилоты в автомобилях: Tesla и другие.")
        time.sleep(3)  
        bot.send_message(chat_id, "Медицина: Диагностика болезней по снимкам.")
        time.sleep(3)  
        completed_courses.append("Примеры использования")
        check_completion(chat_id)
    elif message.text == "Как они работают?":  # Курс 3
        bot.send_message(chat_id, "1. Представь себе, что ты учишь робота различать яблоки и апельсины.")
        time.sleep(3)  
        bot.send_message(chat_id, "2. Ты показываешь ему много картинок яблок и апельсинов. Каждое изображение – это входные данные.")
        time.sleep(3)  
        bot.send_message(chat_id, "3. Нейросеть анализирует эти картинки и ищет закономерности: цвет, форму, размер.")
        time.sleep(3)  
        bot.send_message(chat_id, "4. Она настраивает связи между своими 'нейронами', чтобы лучше отличать яблоки от апельсинов. Это называется 'обучение'.")
        time.sleep(3) 
        bot.send_message(chat_id, "5. Когда ты показываешь ей новую картинку, она пытается предсказать, что на ней изображено. Если она ошиблась, ты говоришь ей об этом.")
        time.sleep(3)  
        bot.send_message(chat_id, "6. После многих повторений робот становится очень хорош в распознавании яблок и апельсинов!")
        time.sleep(3)  
        completed_courses.append("Как они работают?")
        check_completion(chat_id)

    elif message.text == "Машинное обучение - это…":  # Курс 4
        bot.send_message(chat_id, "Машинное обучение – это область искусственного интеллекта, которая позволяет компьютерам обучаться и делать прогнозы или принимать решения на основе имеющихся данных.")
        time.sleep(3)  
        completed_courses.append("Машинное обучение - это…")
        check_completion(chat_id)

def check_completion(chat_id):
    completed_courses = users[chat_id]['completed_courses']
    required_courses = ["Что такое нейросети?", "Примеры использования", "Как они работают?", "Машинное обучение - это…"]
    if set(completed_courses) == set(required_courses):
        bot.send_message(chat_id, "Поздравляем! Вы успешно завершили курс по нейросетям!")

bot.polling(none_stop=True)