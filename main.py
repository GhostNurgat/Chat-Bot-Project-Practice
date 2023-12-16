import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from data import gs_read
from scripts.vk_bot import VkBot

TOKEN = 'vk1.a.WYRyeCV_VKvbVfkxmzZ6hsGBaU0egHSJ1tFinYfRFLF9rG7SeJnV35QdECvgxvLf6hkL1SjM-pZvaBhtsyywrQxxjWU-SV5JCyflr9YLnUx0ZJQhnv3fbExquErCbLR4o3-e1VUpcDf1or41woiHfFAGClpTM2Xj9sV3xUKnRK3EUbCOEvVJLtsIMeGtTHQyr3UnaTw4_xDV3P2oqJd74A'
GROUP_ID = '223402170'

vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('botvk-406913-d3f1f2b907ad.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Вопросы-Ответы')

rows = gs_read.get_rows(spreadsheet)
questions = gs_read.get_questions(rows)
answers = gs_read.get_answers(rows)

def send_message(user_id, message):
    vk_session.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': 0})

def main():
    print('Сервер запущен')
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            print('New message')
            print(f'For me by: {event.user_id}', end=' ')
            bot = VkBot(event.user_id, questions, answers)
            send_message(event.user_id, bot.new_message(event.text))
            print('Text:', event.text)

if __name__ == '__main__':
    main()