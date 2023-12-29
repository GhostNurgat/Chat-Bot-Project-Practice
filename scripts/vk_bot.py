import vk_api

class VkBot:
    def __init__(self, user_id, questions, answers):
        self._USER_ID = user_id
        self._QUESTIONS = questions
        self._ANSWERS = answers
        self._KEYWORDS = ['долг', 'без проекта', 'без команды', 'нет проекта', 'нет команды', 'контрольные точки', 'итерации', 'teamproject', 'исследовательского трека', 'без проектов', 'контрольная точка', 'стартап', 'диплом', 'балл', 'оценил', 'пересдач', 'форм', 'тем', 'участник']

        self._TOKEN = 'vk1.a.1bawSWfDbqe-HaFAIzLTCy8PHaolkFeXMp87avJHEOdhWWG1Ji01su3ez3PbOSyIbkpbl_Qh6Ip4cyxx0lbg_rJ5bgd4ankuvY0TXgV15zQpOVSjVyyxNLXBG67AtXjTqikfQ9GXdy0pRdHFWBEzCHmLHoUJC7sCbaXrnFgNpuF1HJtlMOV53D6cpsFHkG9s1ilo9YCLnJXxR45tGH1oUg'
        self._GROUP_ID = '223402170'
    
    def _get_keyword(self, message):
        keyword = ''
        for key in self._KEYWORDS:
            if key in message.lower():
                keyword = key
        
        return keyword

    def _search_posts_by_keyword(self, keyword):
        session = vk_api.VkApi(token=self._TOKEN)
        vk = session.get_api()
        response = vk.wall.get(owner_id='-' + self._GROUP_ID, count=50)

        if keyword is None:
            return None
        
        posts = response['items']
        found_posts = []
        for post in posts:
            if keyword in post['text'].lower():
                found_posts.append(post['text'])
        return found_posts

    def get_answers(self, message):
        if message.lower() in self._QUESTIONS:
            index = self._QUESTIONS.index(message.lower())
            return "Ответ на ваш вопрос: {}".format(self._ANSWERS[index])
        
        keyword = self._get_keyword(message)
        found_posts = self._search_posts_by_keyword(keyword)
        if found_posts:
            return '\n\n'.join(found_posts)
        else:
            return f'Ваш вопрос с ключевым словом ответ не найдено'

        