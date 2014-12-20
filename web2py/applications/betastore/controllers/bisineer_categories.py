import gluon.contrib.simplejson as json

if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth


def get_categories():
    try:
        result = {}
        query = db.bis_category.id > 0
        fields = ['name']
        sel = [db.bis_category[field] for field in fields]
        rows = db(query).select(*sel, projection=True)
        #rows = db(db.bis_category.ALL).select(*sel, projection=True).as_dict()
        result['categories'] = rows
        print str(result)
    except Exception, e:
        logger.error(str(e))
        result = {"result": "failure", "msg": "Something went wrong. Please try again"}
    return result