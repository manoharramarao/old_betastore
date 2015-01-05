import gluon.contrib.simplejson as json
import traceback
from v1.catalog.service import CatalogServices
from gluon.storage import Storage

# TODO use the following codes for different errors

# 400 - Bad request - This means, service could not understand the input at all.
# if input is not valid. So all is_valid methods inside controllers should throw this exception

# 422 - you can use this as well if data is invalid. It means, you understood the input and input is invalid.

# 401 - if secured resources are accessed by non authenticated users

# 403 - if users try to get the resources for which they don't have access to

# 500 - Any error apart from above ones

# 502 - Bad Gateway

# 503 - Service unavailable

#

# 200 - OK

# 201 - Created

# 202 - Accepted

# 203 - Non Authoritative information

# 204 - No Content

# 205 - Reset Content

# 206 - Partial Content

# 207 - Multi Status

# also check, you might want to consider vnd.error - But this would respond back with http 200OK every time.
# https://github.com/blongden/vnd.error/blob/master/README.md

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
        # rows = db(db.bis_category.ALL).select(*sel, projection=True).as_dict()
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
        logger.debug("number of child categories are " + str(len(child_categories)))
        logger.debug("child categories are " + child_categories.as_json())
    # TODO: remove this. catch specific exceptions
    except Exception, e:
        logger.error(str(e))
        traceback.print_exc()
        raise HTTP(500, 'Ouch!! something went wrong. Please try again')
    return child_categories.as_json()