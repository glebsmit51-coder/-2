import telebot
from telebot import types
import json
import os
from datetime import datetime
BOT_TOKEN = "8358611518:AAHHJLP4auxuIBW8KvpzKL5smaTf7S0pHyc"
bot = telebot.TeleBot(BOT_TOKEN)
DATA_FILE = "bot_data.json"
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if "weeks" not in data:
                data["weeks"] = {}
                data["current_week"] = "week_1"
                data["weeks"]["week_1"] = create_new_week()
            if "current_week" not in data:
                data["current_week"] = "week_1"
            current_week_data = data["weeks"][data["current_week"]]
            for name in current_week_data["names"]:
                if name not in current_week_data["lives"]:
                    current_week_data["lives"][name] = 3
            return data
    else:
        return {
            "weeks": {
                "week_1": create_new_week()
            },
            "current_week": "week_1"
        }
def create_new_week():
    initial_names = ["Алексей", "Мария", "Иван", "Анна", "Дмитрий"]
    return {
        "names": initial_names,
        "scores": {name: ["❌", "❌", "❌", "❌", "❌"] for name in initial_names},
        "lives": {name: 3 for name in initial_names},
        "bonus_points": {name: 0 for name in initial_names}, 
        "created_date": datetime.now().strftime("%d.%m.%Y %H:%M")
    }
def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
def get_current_week_data(data):
    return data["weeks"][data["current_week"]]
def get_lives(week_data, name):
    return week_data["lives"].get(name, 3)
def get_bonus_points(week_data, name):
    return week_data["bonus_points"].get(name, 0)
def calculate_total_score(scores, lives, bonus_points=0):
    base_score = scores.count("✅") * 10
    penalty = (3 - lives) * 50  
    total_score = base_score - penalty + bonus_points  
    return total_score
def get_week_stats(week_data):
    total_checkmarks = 0
    total_points = 0
    for name in week_data["names"]:
        scores = week_data["scores"].get(name, ["❌", "❌", "❌", "❌", "❌"])
        lives = get_lives(week_data, name)
        bonus_points = get_bonus_points(week_data, name)
        total_checkmarks += scores.count("✅")
        total_points += calculate_total_score(scores, lives, bonus_points)
    return total_checkmarks, total_points
def get_sorted_participants(week_data):
    participants = []
    for name in week_data["names"]:
        scores = week_data["scores"].get(name, ["❌", "❌", "❌", "❌", "❌"])
        lives = get_lives(week_data, name)
        bonus_points = get_bonus_points(week_data, name)
        total_score = calculate_total_score(scores, lives, bonus_points)
        participants.append({
            "name": name,
            "scores": scores,
            "lives": lives,
            "bonus_points": bonus_points,
            "total_score": total_score
        })
    participants.sort(key=lambda x: x["total_score"], reverse=True)
    return participants
def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📊 Показать оценки")
    btn2 = types.KeyboardButton("👥 Изменить состав")
    btn3 = types.KeyboardButton("✅ Изменить оценки")
    btn4 = types.KeyboardButton("💔 Снять жизнь")
    btn5 = types.KeyboardButton("➕ Добавить баллы")
    btn6 = types.KeyboardButton("📅 Управление неделями")
    btn7 = types.KeyboardButton("❓ Помощь")
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7)
    return markup
def weeks_menu(data):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for week_key in data["weeks"]:
        week_number = week_key.replace("week_", "")
        is_current = " ✅" if week_key == data["current_week"] else ""
        markup.add(types.KeyboardButton(f"📅 Неделя {week_number}{is_current}"))
    markup.add(types.KeyboardButton("🆕 Создать новую неделю"))
    markup.add(types.KeyboardButton("🗑️ Удалить неделю"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup
def lives_menu(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in names:
        markup.add(types.KeyboardButton(f"💔 {name}"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup
def bonus_points_menu(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in names:
        markup.add(types.KeyboardButton(f"➕ {name}"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup
def scores_menu(names):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in names:
        markup.add(types.KeyboardButton(f"📝 {name}"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    return markup
def emoji_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=5)
    for i in range(5):
        buttons = [types.KeyboardButton(f"{i+1}:✅"), types.KeyboardButton(f"{i+1}:❌")]
        markup.add(*buttons)
    markup.add(types.KeyboardButton("🔙 Назад к списку"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    data = load_data()
    welcome_text = """👋 Добро пожаловать в бот для учета оценок
📊 **Показать оценки** - посмотреть текущие результаты
👥 **Изменить состав** - добавить или удалить участников
✅ **Изменять оценки** - изменить оценки участников
💔 **Снять жизнь** - снять жизнь (-50 очков)
➕ **Добавить баллы** - добавить бонусные баллы
📅 **Управление неделями** - создать/удалить недели
❓ **Помощь** - показать справку
🎯 У каждого участника 3 жизни. За каждую снятую жизнь снимается 50 очков
Используйте кнопки ниже для управления ботом!"""
    bot.send_message(message.chat.id, welcome_text, 
                    reply_markup=main_menu(), parse_mode='Markdown')
@bot.message_handler(func=lambda message: message.text == "❓ Помощь")
def send_help(message):
    help_text = """📋 **Доступные команды:**
📊 **Показать оценки** - посмотреть текущие результаты всех участников
👥 **Изменить состав** - управление списком участников:
   - Для добавления: отправьте сообщение с именем
   - Для удаления: нажмите на кнопку с именем
✅ **Изменить оценки** - изменение оценок участников:
   - Выберите участника из списка
   - Выберите номер оценки для изменения (1-5)
   - Выберите смайлик (✅ или ❌)
💔 **Снять жизнь** - снять одну жизнь у участника:
   - Штраф -50 очков за каждую снятую жизнь
➕ **Добавить баллы** - добавить или снять бонусные баллы участнику:
   - Можно вводить положительные и отрицательные числа
   - Пример: +10 добавит 10 баллов, -5 снимет 5 баллов
📅 **Управление неделями** - работа с неделями:
   - Создать новую неделю (сброс всех данных)
   - Удалить неделю
   - Переключиться между неделями
🔙 **Назад** - вернуться в главное меню
🎯 **Система подсчета:**
   - У каждого участника 3 жизни в начале недели
   - Каждая ✅ = 10 очков
   - Каждая снятая жизнь = -50 очков
   - Бонусные баллы добавляются/вычитаются из общего счета
   - Общий счет может быть отрицательным
   - Участники сортируются по убыванию очков"""
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')
@bot.message_handler(func=lambda message: message.text == "📊 Показать оценки")
def show_scores(message):
    data = load_data()
    week_data = get_current_week_data(data)
    participants = get_sorted_participants(week_data)
    total_checkmarks, total_points = get_week_stats(week_data)
    week_number = data["current_week"].replace("week_", "")
    message_text = f"🎯 *Текущие оценки (Неделя {week_number}):*\n\n"
    for i, participant in enumerate(participants, 1):
        name = participant["name"]
        scores = participant["scores"]
        lives = participant["lives"]
        bonus_points = participant["bonus_points"]
        total_score = participant["total_score"]
        score_display = " ".join(scores)
        hearts = "❤️" * lives + "♡" * (3 - lives)
        message_text += f"{i}. *{name}*\n"
        message_text += f"   Оценки: {score_display}\n"
        message_text += f"   Жизни: {hearts} ({lives}/3)\n"
        if bonus_points != 0:
            bonus_sign = "+" if bonus_points > 0 else ""
            message_text += f"   Бонусы: {bonus_sign}{bonus_points} баллов\n"
        score_display = str(total_score) if total_score >= 0 else f"-{abs(total_score)}"
        message_text += f"   Очки: *{score_display}*\n\n"
    
    message_text += f"📈 *Статистика недели:*\n"
    message_text += f"• Всего ✅: {total_checkmarks}\n"
    total_points_display = str(total_points) if total_points >= 0 else f"-{abs(total_points)}"
    message_text += f"• Всего очков: {total_points_display}\n"
    message_text += f"• Участников: {len(participants)}"
    
    bot.send_message(message.chat.id, message_text, parse_mode='Markdown')

@bot.message_handler(func=lambda message: message.text == "💔 Снять жизнь")
def remove_life_menu(message):
    data = load_data()
    week_data = get_current_week_data(data)
    
    if not week_data["names"]:
        bot.send_message(message.chat.id, "❌ Список участников пуст! Добавьте участников через меню 'Изменить состав'")
        return
    
    text = "💔 *Снятие жизни:*\n\n"
    text += "Выберите участника, у которого нужно снять жизнь:\n"
    text += "⚠️ *Внимание:* за каждую снятую жизнь снимается 50 очков!\n\n"
    
    participants = get_sorted_participants(week_data)
    for i, participant in enumerate(participants, 1):
        text += f"{i}. {participant['name']} - {participant['lives']}/3 жизней\n"
    
    bot.send_message(message.chat.id, text, 
                    reply_markup=lives_menu(week_data["names"]), parse_mode='Markdown')
    bot.register_next_step_handler(message, process_life_removal)

def process_life_removal(message):
    if message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
        return
    if not message.text.startswith("💔 "):
        bot.send_message(message.chat.id, "❌ Пожалуйста, выберите участника из списка кнопок!")
        remove_life_menu(message)
        return
    
    data = load_data()
    week_data = get_current_week_data(data)
    selected_name = message.text.replace("💔 ", "")
    
    if selected_name in week_data["names"]:
        current_lives = get_lives(week_data, selected_name)
        
        if current_lives > 0:
            week_data["lives"][selected_name] = current_lives - 1
            save_data(data)
            scores = week_data["scores"].get(selected_name, ["❌", "❌", "❌", "❌", "❌"])
            new_lives = get_lives(week_data, selected_name)
            bonus_points = get_bonus_points(week_data, selected_name)
            new_score = calculate_total_score(scores, new_lives, bonus_points)
            
            text = f"💔 У участника *{selected_name}* снята 1 жизнь!\n\n"
            text += f"• Было жизней: {current_lives}/3\n"
            text += f"• Стало жизней: {new_lives}/3\n"
            text += f"• Штраф: -50 очков\n"
            score_display = str(new_score) if new_score >= 0 else f"-{abs(new_score)}"
            text += f"• Текущие очки: *{score_display}*\n\n"
            
            if new_lives == 0:
                text += "⚠️ *Внимание:* У участника не осталось жизней!"
            
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, 
                           f"❌ У участника *{selected_name}* уже не осталось жизней!", 
                           parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, "❌ Участник не найден!")
    
    remove_life_menu(message)

@bot.message_handler(func=lambda message: message.text == "➕ Добавить баллы")
def add_bonus_points_menu(message):
    data = load_data()
    week_data = get_current_week_data(data)
    
    if not week_data["names"]:
        bot.send_message(message.chat.id, "❌ Список участников пуст! Добавьте участников через меню 'Изменить состав'")
        return
    
    text = "➕ *Добавление/снятие баллов:*\n\n"
    text += "Выберите участника:\n"
    text += "ℹ️ Можно вводить положительные и отрицательные числа\n\n"
    
    participants = get_sorted_participants(week_data)
    for i, participant in enumerate(participants, 1):
        current_bonus = participant["bonus_points"]
        bonus_text = f" ({current_bonus:+})" if current_bonus != 0 else ""
        text += f"{i}. {participant['name']}{bonus_text}\n"
    
    bot.send_message(message.chat.id, text, 
                    reply_markup=bonus_points_menu(week_data["names"]), parse_mode='Markdown')
    bot.register_next_step_handler(message, select_person_for_bonus)

def select_person_for_bonus(message):
    if message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
        return
    if not message.text.startswith("➕ "):
        bot.send_message(message.chat.id, "❌ Пожалуйста, выберите участника из списка кнопок!")
        add_bonus_points_menu(message)
        return
    
    data = load_data()
    week_data = get_current_week_data(data)
    selected_name = message.text.replace("➕ ", "")
    
    if selected_name in week_data["names"]:
        bot.send_message(message.chat.id, 
                        f"Введите количество баллов для добавления участнику *{selected_name}*:\n(можно вводить отрицательные числа)",
                        parse_mode='Markdown',
                        reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, process_bonus_points, selected_name)
    else:
        bot.send_message(message.chat.id, "❌ Участник не найден!")
        add_bonus_points_menu(message)

def process_bonus_points(message, selected_name):
    try:
        points = int(message.text.strip())  
        data = load_data()
        week_data = get_current_week_data(data)
        current_bonus = get_bonus_points(week_data, selected_name)
        week_data["bonus_points"][selected_name] = current_bonus + points
        save_data(data)
        scores = week_data["scores"].get(selected_name, ["❌", "❌", "❌", "❌", "❌"])
        lives = get_lives(week_data, selected_name)
        new_total_score = calculate_total_score(scores, lives, current_bonus + points)
        
        text = f"✅ Участнику *{selected_name}* "
        if points >= 0:
            text += f"добавлено *+{points}* баллов!\n\n"
        else:
            text += f"снято *{points}* баллов!\n\n"
        
        text += f"• Было бонусных баллов: {current_bonus}\n"
        text += f"• Стало бонусных баллов: {current_bonus + points}\n"
        total_score_display = str(new_total_score) if new_total_score >= 0 else f"-{abs(new_total_score)}"
        text += f"• Общий счет: *{total_score_display}*"
        
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        add_bonus_points_menu(message)
        
    except ValueError:
        bot.send_message(message.chat.id, "❌ Пожалуйста, введите целое число!")
        add_bonus_points_menu(message)

@bot.message_handler(func=lambda message: message.text == "📅 Управление неделями")
def manage_weeks(message):
    data = load_data()
    
    text = "📅 *Управление неделями:*\n\n"
    text += "✅ - текущая неделя\n\n"
    
    for week_key in data["weeks"]:
        week_number = week_key.replace("week_", "")
        week_data = data["weeks"][week_key]
        is_current = " ✅" if week_key == data["current_week"] else ""
        total_checkmarks, total_points = get_week_stats(week_data)
        
        text += f"*Неделя {week_number}*{is_current}\n"
        text += f"Создана: {week_data['created_date']}\n"
        text += f"Участников: {len(week_data['names'])}\n"
        text += f"✅: {total_checkmarks} | Очки: {total_points}\n\n"
    
    bot.send_message(message.chat.id, text, 
                    reply_markup=weeks_menu(data), parse_mode='Markdown')
    bot.register_next_step_handler(message, process_weeks_management)

def process_weeks_management(message):
    if message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
        return
    
    elif message.text == "🆕 Создать новую неделю":
        data = load_data()
        
        # Создаем новую неделю
        new_week_number = len(data["weeks"]) + 1
        new_week_key = f"week_{new_week_number}"
        data["weeks"][new_week_key] = create_new_week()
        data["current_week"] = new_week_key
        save_data(data)
        
        bot.send_message(message.chat.id, 
                        f"✅ Создана *Неделя {new_week_number}*!\nВсе данные сброшены, жизни восстановлены.",
                        parse_mode='Markdown')
        manage_weeks(message)
        return
    
    elif message.text == "🗑️ Удалить неделю":
        data = load_data()
        
        if len(data["weeks"]) <= 1:
            bot.send_message(message.chat.id, "❌ Нельзя удалить единственную неделю!")
            manage_weeks(message)
            return
        
        text = "🗑️ *Удаление недели:*\n\nВыберите неделю для удаления:\n\n"
        
        for week_key in data["weeks"]:
            week_number = week_key.replace("week_", "")
            week_data = data["weeks"][week_key]
            total_checkmarks, total_points = get_week_stats(week_data)
            
            text += f"*Неделя {week_number}*\n"
            text += f"✅: {total_checkmarks} | Очки: {total_points}\n\n"
        
        bot.send_message(message.chat.id, text, parse_mode='Markdown')
        bot.register_next_step_handler(message, process_week_deletion)
        return
    
    elif message.text.startswith("📅 Неделя "):
        data = load_data()
        week_number = message.text.replace("📅 Неделя ", "").replace(" ✅", "").strip()
        week_key = f"week_{week_number}"
        
        if week_key in data["weeks"]:
            data["current_week"] = week_key
            save_data(data)
            bot.send_message(message.chat.id, f"✅ Переключено на *Неделя {week_number}*", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ Неделя не найдена!")
        
        manage_weeks(message)
        return
    
    else:
        bot.send_message(message.chat.id, "❌ Неизвестная команда!")
        manage_weeks(message)

def process_week_deletion(message):
    if message.text == "🔙 Назад":
        manage_weeks(message)
        return
    
    data = load_data()
    
    try:
        week_number = message.text.replace("Неделя ", "").strip()
        week_key = f"week_{week_number}"
        
        if week_key in data["weeks"]:
            if len(data["weeks"]) <= 1:
                bot.send_message(message.chat.id, "❌ Нельзя удалить единственную неделю!")
                manage_weeks(message)
                return
            

            del data["weeks"][week_key]
            if data["current_week"] == week_key:
                data["current_week"] = list(data["weeks"].keys())[0]
            
            save_data(data)
            bot.send_message(message.chat.id, f"✅ Неделя {week_number} удалена!", parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, "❌ Неделя не найдена!")
    
    except:
        bot.send_message(message.chat.id, "❌ Ошибка при удалении недели!")
    
    manage_weeks(message)

@bot.message_handler(func=lambda message: message.text == "👥 Изменить состав")
def edit_composition(message):
    data = load_data()
    week_data = get_current_week_data(data)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    for name in week_data["names"]:
        markup.add(types.KeyboardButton(f"❌ Удалить {name}"))
    
    markup.add(types.KeyboardButton("➕ Добавить нового"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    
    week_number = data["current_week"].replace("week_", "")
    text = f"👥 *Управление составом (Неделя {week_number}):*\n\n"
    text += "• Для *добавления*: нажмите '➕ Добавить нового' и отправьте имя\n"
    text += "• Для *удаления*: нажмите на кнопку с именем\n"
    text += "• *Новые участники* получают 3 жизни\n"
    text += "• Текущий состав:\n"
    
    participants = get_sorted_participants(week_data)
    for i, participant in enumerate(participants, 1):
        text += f"  {i}. {participant['name']} - {participant['lives']}/3 жизней\n"
    
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode='Markdown')
    bot.register_next_step_handler(message, process_composition_edit)

def process_composition_edit(message):
    data = load_data()
    week_data = get_current_week_data(data)
    
    if message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
        return
    
    elif message.text == "➕ Добавить нового":
        bot.send_message(message.chat.id, "Введите имя нового участника:", 
                        reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_new_member)
        return
    
    elif message.text.startswith("❌ Удалить "):
        name_to_remove = message.text.replace("❌ Удалить ", "")
        if name_to_remove in week_data["names"]:
            week_data["names"].remove(name_to_remove)
            if name_to_remove in week_data["scores"]:
                del week_data["scores"][name_to_remove]
            if name_to_remove in week_data["lives"]:
                del week_data["lives"][name_to_remove]
            if name_to_remove in week_data["bonus_points"]:
                del week_data["bonus_points"][name_to_remove]
            save_data(data)
            bot.send_message(message.chat.id, f"✅ Участник {name_to_remove} удален!")
        else:
            bot.send_message(message.chat.id, "❌ Участник не найден!")
    
    edit_composition(message)

def add_new_member(message):
    data = load_data()
    week_data = get_current_week_data(data)
    new_name = message.text.strip()
    
    if not new_name:
        bot.send_message(message.chat.id, "❌ Имя не может быть пустым!")
    elif new_name in week_data["names"]:
        bot.send_message(message.chat.id, "❌ Участник с таким именем уже существует!")
    else:
        week_data["names"].append(new_name)
        week_data["scores"][new_name] = ["❌", "❌", "❌", "❌", "❌"]
        week_data["lives"][new_name] = 3  
        week_data["bonus_points"][new_name] = 0  
        save_data(data)
        bot.send_message(message.chat.id, f"✅ Участник {new_name} добавлен с 3 жизнями!")
    
    edit_composition(message)

@bot.message_handler(func=lambda message: message.text == "✅ Изменить оценки")
def edit_scores(message):
    data = load_data()
    week_data = get_current_week_data(data)
    
    if not week_data["names"]:
        bot.send_message(message.chat.id, "❌ Список участников пуст! Добавьте участников через меню 'Изменить состав'")
        return
    
    week_number = data["current_week"].replace("week_", "")
    text = f"✅ *Изменение оценок (Неделя {week_number}):*\n\nВыберите участника для изменения оценок:"
    bot.send_message(message.chat.id, text, 
                    reply_markup=scores_menu(week_data["names"]), parse_mode='Markdown')
    bot.register_next_step_handler(message, select_person_for_editing)

def select_person_for_editing(message):
    if message.text == "🔙 Назад":
        bot.send_message(message.chat.id, "Главное меню:", reply_markup=main_menu())
        return
    if not message.text.startswith("📝 "):
        bot.send_message(message.chat.id, "❌ Пожалуйста, выберите участника из списка кнопок!")
        edit_scores(message)
        return
    
    data = load_data()
    week_data = get_current_week_data(data)
    selected_name = message.text.replace("📝 ", "")
    
    if selected_name in week_data["names"]:
        scores = week_data["scores"].get(selected_name, ["❌", "❌", "❌", "❌", "❌"])
        lives = get_lives(week_data, selected_name)
        bonus_points = get_bonus_points(week_data, selected_name)
        current_score = calculate_total_score(scores, lives, bonus_points)
        
        score_display = " ".join([f"{i+1}" for i in range(5)])
        emoji_display = " ".join(scores)
        
        text = f"📝 *Редактирование оценок для {selected_name}:*\n\n"
        text += f"Номера:    {score_display}\n"
        text += f"Оценки:  {emoji_display}\n"
        current_score_display = str(current_score) if current_score >= 0 else f"-{abs(current_score)}"
        text += f"Жизни: {lives}/3 | Бонусы: +{bonus_points} | Очки: {current_score_display}\n\n"
        text += "Выберите номер оценки для изменения (1-5):"
        
        bot.send_message(message.chat.id, text, 
                        reply_markup=emoji_menu(), parse_mode='Markdown')
        bot.register_next_step_handler(message, select_score_to_change, selected_name)
    else:
        bot.send_message(message.chat.id, "❌ Участник не найден!")
        edit_scores(message)

def select_score_to_change(message, selected_name):
    if message.text == "🔙 Назад к списку":
        edit_scores(message)
        return
    
    data = load_data()
    week_data = get_current_week_data(data)
    
    try:
        if ":" in message.text:
            score_num = int(message.text.split(":")[0]) - 1
            new_emoji = "✅" if "✅" in message.text else "❌"
            
            if 0 <= score_num <= 4:
                if selected_name not in week_data["scores"]:
                    week_data["scores"][selected_name] = ["❌", "❌", "❌", "❌", "❌"]
                
                week_data["scores"][selected_name][score_num] = new_emoji
                save_data(data)
                
                scores = week_data["scores"][selected_name]
                lives = get_lives(week_data, selected_name)
                bonus_points = get_bonus_points(week_data, selected_name)
                new_score = calculate_total_score(scores, lives, bonus_points)
                
                score_display = " ".join([f"{i+1}" for i in range(5)])
                emoji_display = " ".join(scores)
                
                text = f"✅ Оценка обновлена!\n\n"
                text += f"*{selected_name}:*\n"
                text += f"Номера:    {score_display}\n"
                text += f"Оценки:  {emoji_display}\n"
        
                new_score_display = str(new_score) if new_score >= 0 else f"-{abs(new_score)}"
                text += f"Жизни: {lives}/3 | Бонусы: +{bonus_points} | Очки: {new_score_display}\n\n"
                text += "Выберите следующую оценку для изменения или вернитесь назад:"
                
                bot.send_message(message.chat.id, text, 
                                reply_markup=emoji_menu(), parse_mode='Markdown')
                bot.register_next_step_handler(message, select_score_to_change, selected_name)
            else:
                bot.send_message(message.chat.id, "❌ Неверный номер оценки! Выберите от 1 до 5.")
                select_person_for_editing(message)
    except ValueError:
        bot.send_message(message.chat.id, "❌ Неверный формат! Используйте кнопки.")
        select_person_for_editing(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    main_menu_buttons = ["📊 Показать оценки", "👥 Изменить состав", "✅ Изменить оценки", 
                        "💔 Снять жизнь", "➕ Добавить баллы", "📅 Управление неделями", "❓ Помощь"]
    
    if message.text not in main_menu_buttons:
        bot.send_message(message.chat.id, 
                        "Используйте кнопки ниже для управления ботом:",
                        reply_markup=main_menu())


bot.remove_webhook()

bot.polling()
