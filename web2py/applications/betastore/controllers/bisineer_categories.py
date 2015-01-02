import gluon.contrib.simplejson as json
import traceback
from v1.catalog.service import CatalogServices
from gluon.storage import Storage


if False:
    from gluon import *
    request = current.request
    response = current.response
    session = current.response
    cache = current.cache
    db = current.db
    auth = current.auth
    logger = current.logger


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


def get_child_categories():
    """
    input: {parent_category: "<db.bis_category.code>"}
    :return:
    """
    try:
        input_json = Storage(json.loads(request.body.read()))
        logger.debug("input is " + str(input_json))
        parent_category = input_json.parent_category
        catalog_services = CatalogServices()
        child_categories = catalog_services.get_child_categories(parent_category)
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTP(500, 'Ouch!! something went wrong. Please try again')
    return child_categories.as_json()