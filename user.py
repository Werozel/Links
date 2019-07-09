from globals import api
import time


class User:

    def __init__(self, id):
        self.avaliable = True
        self.info = {}
        self.id = id
        self.name = ""
        self.last_name = ""
        self.friends = []
        self.last_update_time = time.time()
        try:
            self.info = api.users.get(user_ids=id, fields="is_friend")[0]
            self.id = int(self.info.get("id"))
            self.name = self.info.get('first_name')
            self.last_name = self.info.get('last_name')
            self.friends = api.friends.get(user_id=self.id).get("items")
            self.last_update_time = time.time()
        except:
            self.avaliable = False

    def update(self):
        if self.avaliable:
            self.info = api.users.get(user_ids=self.id, fields="is_friend")[0]
            self.name = self.info.get('first_name')
            self.last_name = self.info.get('last_name')
            self.friends = api.friends.get(user_id=self.id).get("items")
            self.last_update_time = time.time()

    def __eq__(self, other):
        return self.id == other.id

    def get_mutual(self, other):
        mutual = []
        for id in self.friends:
            if id in other.friends:
                mutual.append(id)
        return mutual
