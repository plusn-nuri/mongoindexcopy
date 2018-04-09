from pymongo import MongoClient
from urlparse import urlparse
import settings
from bson import json_util




def remark(*parts):
    print '/// ', ' '.join(parts)


def should_include_collection(collection):
    if('*' in settings.include_collections):
        return True

    return collection in settings.include_collections


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

source_db_name = urlparse(settings.source_connection).path[1:]

remark('Included Collections:', settings.include_collections)
remark('Server Connection:', settings.source_connection)
remark('Source Database:', source_db_name)

source_db = MongoClient(settings.source_connection).get_database(source_db_name)

collections = get_collections(source_db, source_db_name)

indexes = get_indexes(source_db, collections)

for item in indexes:
    remark("********************************")
    remark("** Collection", item['name'])
    remark("********************************")
    for ix in item['indexes']:
        remark("   ==> Index:", ix['name'])
        field_def = ix.pop('key')
        options = ix
        statement = 'db.' + item['name'] + '.createIndex(' + json_util.dumps(
            field_def)+',' + json_util.dumps(options) + ');'

        print statement
