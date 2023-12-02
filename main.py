import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
from oauth2client.service_account import ServiceAccountCredentials

token = 'vk1.a.WYRyeCV_VKvbVfkxmzZ6hsGBaU0egHSJ1tFinYfRFLF9rG7SeJnV35QdECvgxvLf6hkL1SjM-pZvaBhtsyywrQxxjWU-SV5JCyflr9YLnUx0ZJQhnv3fbExquErCbLR4o3-e1VUpcDf1or41woiHfFAGClpTM2Xj9sV3xUKnRK3EUbCOEvVJLtsIMeGtTHQyr3UnaTw4_xDV3P2oqJd74A'
vk_session = vk_api.VkApi(token=token)
vk = vk_session.get_api
longpoll = VkLongPoll(vk_session)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('botvk-406913-d3f1f2b907ad.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Test')

def search_posts(keyword):
    sheet = spreadsheet.sheet1
    rows = sheet.get_all_values()
    found_posts = []

    for row in rows:
        if keyword.lower() in row[1].lower():  # Проверяем, содержит ли пост ключевое слово
            found_posts.append(row)

    return found_posts

def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

print('Сервер запущен')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text.startswith('найти'):
            keyword = event.text.split()[1]
            posts = search_posts(keyword)
            if posts:
                send_message(event.user_id, f"Найдено постов:")
                for post in posts:
                    send_message(event.user_id, post[1])  # Отправляем текст поста
            else:
                send_message(event.user_id, "Постов не найдено.")
        elif event.text.lower() == 'привет':
            send_message(event.user_id, 'Привет!')
        elif event.text.lower() == 'пока':
            send_message(event.user_id, 'До свидания!')