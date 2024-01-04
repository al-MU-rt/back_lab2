import json
class User:
    def __init__(self, username):
        self.username = username

class Category:
    def __init__(self, name):
        self.name = name

class Record:
    def __init__(self, user_id, category_id, amount):
        self.user_id = user_id
        self.category_id = category_id
        self.amount = amount
