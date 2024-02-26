from fake_useragent import UserAgent

class UserAgentManager:
    def __init__(self):
        self.ua = UserAgent()
    
    def get_random_user_headers(self):
        return {'User-Agent': self.ua.random}