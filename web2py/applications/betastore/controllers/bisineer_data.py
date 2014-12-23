import gluon.contrib.simplejson as json
import traceback

if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth


def import_data():
    """
    Imports data into the db from db_<arg>.csv file for all arguments in the same sequence it is sent
    :return:
    """
    try:
        for arg in request.args:
            db.import_from_csv_file(open('./static/data/db_'+arg+'.csv', 'r'))
    except Exception, e:
        traceback.print_exc()
        raise HTTP(500, str(e))
    return "success"


def delete_data():
    """
    Deletes data from DB for tables sent in request arguments in the sequence it is sent
    :return:
    """
    try:
        for arg in request.args:
            db(db[arg].id > 0).delete()
    except Exception, e:
        traceback.print_exc()
        raise HTTP(500, str(e))
    return "success"


#@auth.requires(requires_login=True, requires_membership='admin')
def export():
    db.export_to_csv_file(open('/tmp/bisineer_data_exported.csv', 'wb'))
    result = {"result": "success"}
    return result	
