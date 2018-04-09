from pymongo import MongoClient
from urlparse import urlparse
from settings import *
from bson import json_util

source_db_name = urlparse(source_connection).path[1:]


def remark(*parts):
    print '/// ', ' '.join(parts)


def should_include_collection(collection):
    if('*' in include_collections):
        return True

    return collection in include_collections


def strip_catalog_fields(definition):
    definition.pop('v')
    definition.pop('ns')
    return definition


def ensure_background(definition):
    definition['bacground'] = True


def get_collections(db, db_name):
    for name in db.list_collection_names():
        if (should_include_collection(name)):
            yield name


def get_indexes(db, collection_names):

    for collection_name in collection_names:
        item = {'name': collection_name, 'indexes': []}
        for index in db[collection_name].list_indexes():
            if(index['name'] == '_id_'):
                continue

            item['indexes'].append(strip_catalog_fields(index))

        yield item


remark('included collections:', include_collections)
remark('server connection:', source_connection)
remark('source database:', source_db_name)

source_db = MongoClient(source_connection).get_database(source_db_name)

collections = get_collections(source_db, source_db_name)

indexes = get_indexes(source_db, collections)

for item in indexes:
    remark('Collection:', item['name'])
    for ix in item['indexes']:
        remark("Index:", ix['name'])
        field_def = ix.pop('key')
        options = ix
        statement = 'db.' + item['name'] + '.createIndex(' + json_util.dumps(
            field_def)+',' + json_util.dumps(options) + ');'

        print statement
