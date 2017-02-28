# -*- coding: utf-8 -*-

import json
import requests
from pymongo import MongoClient

channel_url = 'https://api.channel.io/desk/channels/474/user_chats?state=&sortField=updatedAt&sortOrder=DESC&since={}&limit=100'

class Channel:
    def __init__(self):
        headers = {}
        headers['cookie'] = 'X-Veil-Id=586e1a010022a62d; X-Manager=on0PAPYQn36C5O_VQFuCvwl5lbwNJ7mv3K26WPlMdgrE4Z7bFtxixAS6Hno_3Wnj9dinQq8Wcvl5WxKnD4Zbaw'

        self.headers = headers

        mongo = MongoClient(host='112.169.13.105', port=37773)
        self.db = mongo.message.channel

    def get_messages(self, url):
        print(url)
        res = requests.get(url, headers=self.headers)
        if not res:
            return

        data = json.loads(res.content)
        if not data:
            return

        if 'messages' not in data:
            return

        messages = data['messages']
        self.db.insert_many(messages)

        for m in messages:
            print(m)

        if 'next' in data:
            since = data['next']
            if since == '' or since == 'None':
                return

            self.get_messages(channel_url.format(since))

channel = Channel()
channel.get_messages(channel_url.format(''))
