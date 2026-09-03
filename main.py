import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import random
import time

TOKEN = os.getenv("BOT_TOKEN")  # Твой токен

# Авторизация
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

print("🤖 Бот группы 'Меч Хаоса' запущен!")

def send_message(user_id, message, keyboard=None):
    vk.messages.send(
        user_id=user_id,
        message=message,
        random_id=random.randint(1, 999999999),
        keyboard=keyboard
    )

# Основной цикл бота
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        msg = event.text.lower().strip()
        user_id = event.user_id
        
        print(f"💬 {user_id}: {msg}")
        
        # КОМАНДЫ
        if msg in ["начать", "/start", "старт"]:
            keyboard = VkKeyboard(one_time=True)
            keyboard.add_button("Привет", color=VkKeyboardColor.PRIMARY)
            keyboard.add_button("Помощь", color=VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button("Инфо", color=VkKeyboardColor.NEGATIVE)
            
            send_message(
                user_id,
                "🔥 Добро пожаловать в Меч Хаоса!\nВыбери кнопку или напиши команду:",
                keyboard.get_keyboard()
            )
            
        elif msg == "привет":
            send_message(user_id, "👋 Привет, воин! Да пребудет с тобой сила!")
            
        elif msg == "помощь":
            help_text = """
📋 **Команды бота:**
• Начать / Старт — главное меню
• Привет — поздороваться
• Инфо — информация о группе
• Кто я — узнать своё имя
• Пока — попрощаться
"""
            send_message(user_id, help_text)
            
        elif msg == "инфо":
            group = vk.groups.getById()[0]
            info = f"""
📊 **О группе:**
Название: {group['name']}
ID: {group['id']}
Тип: {group['type']}
Статус: {group.get('status', 'Нет статуса')}
"""
            send_message(user_id, info)
            
        elif msg == "кто я":
            user = vk.users.get(user_ids=user_id)[0]
            send_message(user_id, f"👤 Ты — {user['first_name']} {user['last_name']}!")
            
        elif msg == "пока":
            send_message(user_id, "👋 Пока! Возвращайся к Мечу Хаоса!")
            
        elif msg == "кнопки":
            keyboard = VkKeyboard(one_time=False)
            keyboard.add_button("Привет", color=VkKeyboardColor.PRIMARY)
            keyboard.add_button("Помощь", color=VkKeyboardColor.SECONDARY)
            keyboard.add_line()
            keyboard.add_button("Инфо", color=VkKeyboardColor.NEGATIVE)
            keyboard.add_button("Кто я", color=VkKeyboardColor.POSITIVE)
            send_message(user_id, "🎯 Выбери кнопку:", keyboard.get_keyboard())
            
        else:
            send_message(user_id, f"Неизвестная команда. Напиши 'Помощь' для списка команд.")
