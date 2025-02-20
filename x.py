import http.client
import json
import time
import logging
import random

choose_ans = ["Нет, скажи Да", "Я так много прошу - скажи да", "Это не серьезно, скажи да",
              "Пропробуй еще раз, у тебя получиться, скажи да"]
if_ans = ["Умница, я пока не умею ничего другого, но это пока..."]
TOKEN = ' '
BASE_URL = f'https://api.telegram.org/bot{TOKEN}'
logging.basicConfig(filename="bot.log", level=logging.INFO)
logger = logging.getLogger(__name__)
def get_updates(offset=None):
    conn = http.client.HTTPSConnection("api.telegram.org")
    url = f"/bot{TOKEN}/getUpdates"
    if offset:
        url += f"?offset={offset}"
    conn.request("GET", url)
    response = conn.getresponse()
    data = response.read()
    return json.loads(data)

def send_message(chat_id, text):
    conn = http.client.HTTPSConnection("api.telegram.org")
    url = f"/bot{TOKEN}/sendMessage"
    parse_mode = "HTML"
    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": parse_mode

    })
    headers = {
        'Content-Type': 'application/json'
    }
    conn.request("POST", url, payload, headers)
    response = conn.getresponse()
    return response.read()

def main():
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates['result']:
            chat_id = update['message']['chat']['id']
            message_text = update['message']['text']
            frm = update['message']['chat']
            logger.info("%s %s %s", chat_id, message_text, frm)
            print(f"Received message: {message_text} from chat_id: {chat_id}")

            # Обработка команды /start
            if message_text == "/start":
                send_message(chat_id, "Скажи да")
            elif message_text == "/help":
                str_i = "Здесь все просто, я ЗурнаБот - скажи да"
                send_message(chat_id, str_i)
            elif message_text == "да":
                send_message(chat_id, "<b>Зурна</b>")
            elif message_text.lower() =="Зурна":
                send_message(chat_id, if_ans[0])
            else:
                answer = random.choice(choose_ans)
                send_message(chat_id, answer)

            offset = update['update_id'] + 1

        time.sleep(1)  # Задержка перед следующим запросом

if __name__ == '__main__':
    main()