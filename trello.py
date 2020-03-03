import requests
import misc
import json

trello_token = misc.token['trello']
trello_api_key = misc.api_key['trello']

url = 'https://api.trello.com/1/'

params = {
    'key': trello_api_key,
    'token': trello_token
}


class Board:
    def __init__(self, name):
        self.board_name = name
        self.id = None
        self.lists = None
        self.labels = None
        self.get_bot_board()

    def get_bot_board(self):
        response = requests.get(url + 'members/me/boards', params=params)
        board_list = response.json()
        bot_board = next(board for board in board_list if board['name'] == self.board_name)
        self.id = bot_board['id']
        self.get_labels()
        return bot_board

    def get_board_lists(self):
        response = requests.get(url + 'boards/' + self.id + '/lists', params=params)
        self.lists = response.json()
        return response.json()

    def create_label(self, label_name):
        query = {
            'name': label_name,
            'color': None,
            'idBoard': self.id,
        }

        response = requests.post(f'{url}labels/', params={**query, **params})
        self.get_labels()
        return response.json()['id']

    def get_labels(self):
        raw_labels = requests.get(f'{url}/boards/{self.id}/labels/', params=params).json()
        self.labels = [label for label in raw_labels if label['name'] != '']


class List:
    def __init__(self, board_lists, list_name):
        self.name = list_name
        self.id = next(list for list in board_lists if list['name'] == self.name)['id']


class Card:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def post_card(self, list_id, labels):
        query = {
            **params,
            'idList': list_id,
            'name': self.name,
            'desc': self.description,
            'idLabels': ','.join(labels)
        }

        requests.post(url + '/cards', params=query)
