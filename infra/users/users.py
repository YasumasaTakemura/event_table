from datetime import datetime, timedelta, timezone
from google.cloud import datastore
from infra import JST
from abc import ABC
import os

# class UserModel(object):
#     """interface"""
#     def __init__(self,user):
#         self.user_name =  user['user_name']
#         self.created_at =  datetime.now(JST)
#         self.updated_at =  datetime.now(JST)



class Users(object):
    __key_name = 'user_id'

    def __init__(self, user:dict=None):
        project = os.getenv('PROJECT_ID', 'event-table-dev')
        self.client = datastore.Client(project, __class__.__name__)
        self.user = user

    def user_exist(self, user_name):
        query = self.client.query(**{"kind": __class__.__name__})
        query.add_filter('user_name', '=', user_name)
        query_iter = query.fetch()
        result = list(query_iter)
        if result:
            return True
        return False

    def add(self):
        """
        self.user
            - use_id
            - use_name
            - desc
            - gender
            -
        :return: user data:dict
        """
        if self.user_exist(self.user['user_name']):
            return {'message': {'type': 'duplicate', 'value': 'user_name'}}
        key = self.client.key(__class__.__name__)
        user = datastore.Entity(key)
        self.user['gender'] = self.user.get('gender')
        self.user['birth_day'] = self.user.get('birth_day')
        self.user['created_at'] = datetime.now(JST)
        self.user['update_at'] = datetime.now(JST)
        user.update(self.user)
        try:
            self.client.put(user)
            return {"user_id": user.key.id, "user_name": self.user['user_name']}
        except Exception:
            return {'message': {'type': 'unknown_error', 'value': 'unknown_error.do it again after few minutes later'}}

    def update(self, user_data: dict):
        user_id = int(user_data.pop(self.__key_name))
        if user_data.get('user_name',None):
            if self.user_exist(user_data['user_name']):
                return {'message': {'type': 'duplicate', 'value': 'user_name'}}
        key = self.client.key(__class__.__name__, user_id)
        # user = datastore.Entity(key)
        user = self.client.get(key)
        print(user)
        user.update(user_data)
        self.client.put(user)
        return user.key.id