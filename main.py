import vk_api, vk
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data import vk_token, gs_read

TOKEN = 'vk1.a.WYRyeCV_VKvbVfkxmzZ6hsGBaU0egHSJ1tFinYfRFLF9rG7SeJnV35QdECvgxvLf6hkL1SjM-pZvaBhtsyywrQxxjWU-SV5JCyflr9YLnUx0ZJQhnv3fbExquErCbLR4o3-e1VUpcDf1or41woiHfFAGClpTM2Xj9sV3xUKnRK3EUbCOEvVJLtsIMeGtTHQyr3UnaTw4_xDV3P2oqJd74A'
GROUP_ID = '223402170'

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('botvk-406913-d3f1f2b907ad.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Вопросы-Ответы')

def search_posts_by_keyword(keyword):
    session = vk_api.VkApi(token='vk1.a.1bawSWfDbqe-HaFAIzLTCy8PHaolkFeXMp87avJHEOdhWWG1Ji01su3ez3PbOSyIbkpbl_Qh6Ip4cyxx0lbg_rJ5bgd4ankuvY0TXgV15zQpOVSjVyyxNLXBG67AtXjTqikfQ9GXdy0pRdHFWBEzCHmLHoUJC7sCbaXrnFgNpuF1HJtlMOV53D6cpsFHkG9s1ilo9YCLnJXxR45tGH1oUg')
    vk = session.get_api()
    response = vk.wall.get(owner_id='-' + GROUP_ID, query=keyword, count=10)
    posts = response['items']

    return posts

rows = gs_read.get_rows(spreadsheet)
questions = gs_read.get_questions(rows)
answers = gs_read.get_answers(rows)

def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})


print('Сервер запущен')
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        if event.text.lower() in questions:
            index = questions.index(event.text.lower())
            send_message(event.user_id, f'{answers[index]}')
        elif event.text.startswith('искать'):
            keyword = event.text.split()[1]
            found_posts = search_posts_by_keyword(keyword)
            if len(found_posts) > 0:
                response = "Найдено {} постов:nn{}".format(len(found_posts), 'nn'.join(found_posts))
            else:
                response = "Постов по ключевому слову '{}' не найдено".format(keyword)
            send_message(event.user_id, response)
        elif event.text.lower() == 'привет':
            send_message(event.user_id, 'Привет!')
        elif event.text.lower() == 'пока':
            send_message(event.user_id, 'До свидания!')