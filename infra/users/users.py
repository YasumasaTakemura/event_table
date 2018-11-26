from datetime import datetime, timedelta, timezone
from google.cloud import datastore
from infra import JST
from abc import ABC
import os


class UserFromName(object):
    def __init__(self, user_name):
        project = os.getenv('PROJECT_ID', 'event-table-dev')
        self.client = datastore.Client(project)
        self.user_name = user_name


    def add(self,user_id:int):
        key = self.client.key(__class__.__name__,self.user_name)
        user = datastore.Entity(key)
        user.update({'user_id':user_id})
        self.client.put(user)
        return user.key.id

class Users(object):
    __key_name = 'user_id'

    class UserEntity:
        def __init__(self,user_name):
            self.user_name = user_name


    def __init__(self, **kwargs):
        project = os.getenv('PROJECT_ID', 'event-table-dev')
        # if not project:
        #     raise Exception('PROJECT_ID not set.Please set PROJECT_ID first.')
        self.client = datastore.Client(project)
        self.user = kwargs

    def user_exist(self,name):
        user_id = name
        key = self.client.key(__class__.__name__, user_id).id
        print(key)

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
        # with self.client.transaction():
        print('=======================')
        key = self.client.key(__class__.__name__)
        user = datastore.Entity(key)
        print(user.get('user_name'))
        is_user = self.client.get(key)
        print(is_user)
        user.update(self.user)
        user_name_obj = UserFromName(self.user['user_name'])
        # self.client.put(user)
        # print(key.id)
        # user_name_obj.add(key.id)
        # print(user.key.id)
        return {"user_id":user.key.id,"user_name":self.user['user_name']}

    def update(self,user_data: dict):
        user_id = int(user_data.pop(self.__key_name))
        key = self.client.key(__class__.__name__, user_id)
        user = datastore.Entity(key)
        print(user_data)
        user.update(user_data)
        self.client.put(user)
        return user.key.id







        # def create_client(project_id):
        #     return datastore.Client(project_id)
        # # [END datastore_build_service]
        #
        #
        # # [START datastore_add_entity]
        # def add_task(client, description):
        #     key = client.key('Task')
        #
        #     task = datastore.Entity(
        #         key, exclude_from_indexes=['description'])
        #
        #     task.update({
        #         'created': datetime.datetime.utcnow(),
        #         'description': description,
        #         'done': False
        #     })
        #
        #     client.put(task)
        #
        #     return task.key
        # # [END datastore_add_entity]
        #
        #
        # # [START datastore_update_entity]
        # def mark_done(client, task_id):
        #     with client.transaction():
        #         key = client.key('Task', task_id)
        #         task = client.get(key)
        #
        #         if not task:
        #             raise ValueError(
        #                 'Task {} does not exist.'.format(task_id))
        #
        #         task['done'] = True
        #
        #         client.put(task)
        # # [END datastore_update_entity]
        #
        #
        # # [START datastore_retrieve_entities]
        # def list_tasks(client):
        #     query = client.query(kind='Task')
        #     query.order = ['created']
        #
        #     return list(query.fetch())
        # # [END datastore_retrieve_entities]
        #
        #
        # # [START datastore_delete_entity]
        # def delete_task(client, task_id):
        #     key = client.key('Task', task_id)
        #     client.delete(key)
        # # [END datastore_delete_entity]
        #
        #
        # def format_tasks(tasks):
        #     lines = []
        #     for task in tasks:
        #         if task['done']:
        #             status = 'done'
        #         else:
        #             status = 'created {}'.format(task['created'])
        #
        #         lines.append('{}: {} ({})'.format(
        #             task.key.id, task['description'], status))
        #
        #     return '\n'.join(lines)
        #
        #
        # def new_command(client, args):
        #     """Adds a task with description <description>."""
        #     task_key = add_task(client, args.description)
        #     print('Task {} added.'.format(task_key.id))
        #
        #
        # def done_command(client, args):
        #     """Marks a task as done."""
        #     mark_done(client, args.task_id)
        #     print('Task {} marked done.'.format(args.task_id))
        #
        #
        # def list_command(client, args):
        #     """Lists all tasks by creation time."""
        #     print(format_tasks(list_tasks(client)))
        #
        #
        # def delete_command(client, args):
        #     """Deletes a task."""
        #     delete_task(client, args.task_id)
        #     print('Task {} deleted.'.format(args.task_id))
        #
        #
        # if __name__ == '__main__':
        #     parser = argparse.ArgumentParser()
        #     subparsers = parser.add_subparsers()
        #
        #     parser.add_argument('--project-id', help='Your cloud project ID.')
        #
        #     new_parser = subparsers.add_parser('new', help=new_command.__doc__)
        #     new_parser.set_defaults(func=new_command)
        #     new_parser.add_argument('description', help='New task description.')
        #
        #     done_parser = subparsers.add_parser('done', help=done_command.__doc__)
        #     done_parser.set_defaults(func=done_command)
        #     done_parser.add_argument('task_id', help='Task ID.', type=int)
        #
        #     list_parser = subparsers.add_parser('list', help=list_command.__doc__)
        #     list_parser.set_defaults(func=list_command)
        #
        #     delete_parser = subparsers.add_parser(
        #         'delete', help=delete_command.__doc__)
        #     delete_parser.set_defaults(func=delete_command)
        #     delete_parser.add_argument('task_id', help='Task ID.', type=int)
        #
        #     args = parser.parse_args()
        #
        #     client = create_client(args.project_id)
        #     args.func(client, args)
