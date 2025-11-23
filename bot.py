import os
import json
import requests
from flask import Flask, request

app = Flask(__name__)

# Безопасное хранение токена
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEB_APP_URL = "https://qwaszx112233.github.io/telegram-love-puzzle/"

def send_message(chat_id, text, keyboard=None):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    
    if keyboard:
        data['reply_markup'] = json.dumps(keyboard)
    
    try:
        response = requests.post(url, json=data)
        return response.status_code == 200
    except:
        return False

@app.route('/')
def home():
    return "💖 Love Puzzle Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    
    if 'message' in update:
        message = update['message']
        chat_id = message['chat']['id']
        text = message.get('text', '')
        user_name = message['chat'].get('first_name', 'кохана')
        
        if text == '/start':
            keyboard = {
                'inline_keyboard': [[
                    {
                        'text': '🎮 Грати в Love Puzzle',
                        'web_app': {'url': WEB_APP_URL}
                    }
                ]]
            }
            
            welcome_text = f"""
💖 <b>Love Number Puzzle</b> 💖

Привіт {user_name}! Ласкаво просимо до гри любові та чисел! ❤️

🎮 <b>Особливості:</b>
• 30 романтичних рівнів
• Автоматичне збереження
• Любовні фрази
• Красиві анімації

Натисни кнопку нижче, щоб розпочати гру! 💕
            """
            send_message(chat_id, welcome_text, keyboard)
            
        elif text in ['/game', '/help']:
            keyboard = {
                'inline_keyboard': [[
                    {
                        'text': '🎮 Грати в Love Puzzle', 
                        'web_app': {'url': WEB_APP_URL}
                    }
                ]]
            }
            send_message(chat_id, "Запускай гру та насолоджуйся коханням! 💕", keyboard)
    
    return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
