import asyncio
from datetime import datetime
from app import cluster



db = cluster['StackedUp']

dbs = {
    'users': db.users,
}


timestamp = datetime.now()


class Users:
    def by_id(self, id):
        self.id = id
        return self

    @property
    def monogo_dict(self):
        d = {}

        if hasattr(self, 'id'):
            d['user_name'] = self.id

        return d

    def get(self): 
        return dbs['users'].find_one(self.monogo_dict)

    def push(self, _set):
        dbs['users'].update_one(self.monogo_dict, {'$push':_set})

    def pull(self, _set):
        dbs['users'].update_one(self.monogo_dict, {'$pull':_set})

    def update(self, _set):
        dbs['users'].update_one(self.monogo_dict, {'$set': _set})

    def create(self, data):
        dbs['users'].insert_one(data)

    def delete(self):
        dbs['users'].delete_one(self.monogo_dict)

    def get_all(self):
        return dbs['users'].find().to_list(length=100000)



























