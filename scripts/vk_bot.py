import requests
from bs4 import BeautifulSoup

class VkBot:
    def __init__(self, user_id, questions, answers):
        self._USER_ID = user_id
        self._USERNAME = self._get_username_from_vk_id(user_id)
        self._QUESTIONS = questions
        self._ANSWERS = answers

        self._GREETING = ['привет', 'ку', 'хай']
        self._BYE = ['пока', 'до свидания']

    def _get_username_from_vk_id(self, user_id):
        request = requests.get('https://vk.com/id' + str(user_id))
        bs = BeautifulSoup(request.text, 'html.parser')

        user_name = self._clean_all_tag_from_str(bs.find_all('title')[0])
        return user_name.split()[0]
    
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        result = ''
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == '<':
                    not_skip = False
                else: result += i
            else:
                if i == '>': not_skip = True
        
        return result
    
    def new_message(self, message):
        if message.lower() in self._GREETING:
            return f'Привет, {self._USERNAME}!'
        elif message.lower() in self._BYE:
            return f'Пока, {self._USERNAME}!'