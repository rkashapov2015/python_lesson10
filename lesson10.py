import requests
from urllib.parse import urlencode
from pprint import pprint

APP_ID = 6703198
OAUTH_URL = 'https://oauth.vk.com/authorize'
API_URL = 'https://api.vk.com/method/'
VK_URL = 'https://vk.com'
TOKEN = 'NONE'

oauth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'scope': 'friends',
    'response_type': 'token'
}

full_url = '?'.join((OAUTH_URL, urlencode(oauth_data)))
print('Получите свой токен')
print(full_url)


class Factory:

    def __init__(self):
        pass
        
    def get_user_by_id(self, id):
        params = {
            'access_token': TOKEN,
            'user_ids': id,
            'fields': 'domain',
            'v': '5.85'
        }
        result = requests.get(API_URL + '/users.get', params)
        json = result.json()
        user = User()
        user.load(json['response'][0])
        user.get_friends()
        return user
        

class User:

    def __init__(self):
        self.id = None
        self.first_name = ''
        self.last_name = ''
        self.domain = ''
        self.friends = []

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, first_name):
        self.__first_name = first_name
    
    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, last_name):
        self.__last_name = last_name
    
    @property
    def domain(self):
        return self.__domain

    @domain.setter
    def domain(self, domain):
        self.__domain = domain
    
    def __and__(self, other):
        params = {
            'access_token': TOKEN,
            'source_uid': self.id,
            'target_uid': other.id,
            'v': '5.85'
        }
        result = requests.get(API_URL + '/friends.getMutual', params)
        json = result.json()
        common_friends = []
        for friend in self.friends:
            if friend.id in json['response']:
                common_friends.append(friend)

        return common_friends
        
    def __repr__(self):
        return '/'.join((VK_URL, self.domain))

    def __str__(self):
        return '/'.join((VK_URL, self.domain))

    def show_friends(self):
        for friend in self.friends:
            print(friend)

    def get_friends(self):
        params = {
            'access_token': TOKEN,
            'user_id': self.id,
            'fields': 'domain',
            'v': '5.85'
        }
        print(self.id)
        result = requests.get(API_URL + '/friends.get', params)
        json = result.json()
        for data in json['response']['items']:
            friend = User()
            friend.load(data)
            self.friends.append(friend)
        
    def load(self, user_data):
        if type(user_data) == dict:
            for key in user_data.keys():
                if hasattr(self, key):
                    setattr(self, key, user_data[key])

if TOKEN == 'NONE':
    print('Получите токен')
    quit()

factory = Factory()
user1 = factory.get_user_by_id(6)
user2 = factory.get_user_by_id(7)

print('User1: ', user1)

print('User2: ', user2)

print(user1 & user2)
