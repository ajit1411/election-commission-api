# -*- coding: utf-8 -*-
"""
Created on Sun Jul 19 00:33:22 2020

@author: Ajit
"""

import pymongo
import logging
class Database:
    def __init__(self, database_name):
        logging.info('========== Database called  ==========')
        self.database = database_name
    
    def connect(self):
        client = pymongo.MongoClient('mongodb+srv://ajittest:1234@monogtest.wrp9t.mongodb.net/?retryWrites=true&w=majority')
        return client
        
    def fetch_documents(self, collection_name, classifiers = {}, projections = {}):
        client = self.connect()
        database = client[self.database]
        collection = database[collection_name]
        documents = list(collection.find(classifiers, projections))
        return documents
    
    def inject_data(self, collection_name, data):
        client = self.connect()
        database = client[self.database]
        collection = database[collection_name]
        status = collection.insert_one(data)
        if status:
            return 'success'
        else:
            return 'fail'
                