'''

# Search RESTful API for fetching the users list registered through the portal
Author:- Ajit Jadhav

'''
from extras import Docs as Database
import logging
from bson.json_util import dumps
import os
import sys
import json
import azure.functions as func
directory = os.path.dirname(__file__)
sys.path.insert(0, directory)


def get_users(database_name, collection_name, query=''):
    database_client = Database.Database(database_name)
    users = database_client.fetch_documents(
        collection_name, {'email': query}, {'_id': 0})
    return users


def add_user_data(database_name, collection_name, user_data={}):
    client = Database.Database(database_name)
    if user_data:
        status = client.inject_data('users', user_data)
        return status
    else:
        return 'fail'


def main(req: func.HttpRequest) -> func.HttpResponse:
    headers = {}
    headers['Access-Control-Allow-Headers'] = 'http://localhost:3000'
    headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    headers['Content-Type'] = 'application/json'
    logging.info('Python HTTP trigger function processed a request.')
    if req.method == 'OPTIONS':
        return func.HttpResponse(dumps({}), status_code=200, headers=headers)
    if req.method == 'GET':
        params_body = req.params
        logging.info(params_body)
        users = get_users('election', 'users', params_body['query'])
        return func.HttpResponse(dumps({'users': users}), status_code=200, headers=headers)
    elif req.method == 'POST':
        req_body = req.get_json()
        status = add_user_data('election', 'users', req_body)
        if status == 'success':
            return func.HttpResponse(dumps({'status': 'created'}), status_code=201, headers=headers)
        else:
            return func.HttpResponse(dumps({'status': 'failed'}), status_code=501, headers=headers)
    else:
        return func.HttpResponse('failed', status_code=404, headers=headers)
