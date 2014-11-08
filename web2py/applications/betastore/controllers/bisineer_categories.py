import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_categories")
logger.setLevel(logging.DEBUG)

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
		logging.error(str(e))
		result = {"result": "failure", "msg": "Something went wrong. Please try again"}
	return result