import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_products")
logger.setLevel(logging.DEBUG)

def get_products():
	try:
		json_string = request.body.read()
		logging.info(json_string)
		category = json.loads(json_string)
		logging.info("category name sent is " + category['categoryName'])
		result = {}
		query1 = db.bis_product.id > 0
		query2 = db.bis_product.categories.contains(category['categoryName'])
		fields = ['name','unit_price', 'description_short', 'rating', 'image_urls','id']
		none_fields = ['categories', 'specifications', 'weight', 'product_attributes', 'volume', 'variant_products', 'description_long', 'tax_rate', 'in_stock']
		sel = [db.bis_product[field] for field in fields]
		#rows = db(query1 & query2).select(*sel, projection=True).sort(lambda row:row.name) # when we use project=True, it is giving each production 4 times
		rows = db(query1 & query2).select().sort(lambda row:row.name)
		#rows = db().select(db.bis_product.ALL, cache=(cache.ram,60), cacheable=True, orderby=db.bis_product.id, limitby=(0,20))
		#pages = count/20
		# this for loop is because of gae with web2py. If we have to select specific fields, 
		#then we need to use projection=True in the query. But if we use projection=True, it doesn't allow to use limitby
		if bool(rows):
			for row in rows:
				for field in none_fields:
					# TODO Fix me. It is complaining categories attribute doesn't exist
					del row[field]
		#rows = db().select(*sel, projection=True, cache=(cache.ram,60), cacheable=True) # use this for caching
		logging.info(rows)
		if bool(rows):
			result['products'] = rows
			#result['pages'] = pages
		else:
			result = {"result": "failure", "msg": "no products available"}
	except Exception, e:
		logging.error(str(e))
		result = {"result": "failure", "msg": "Something went wrong. Please try again"}
	return result




def get_product():
    try:
        row = db(db.bis_product.name=='Solar Water Heater1').select().as_dict()
        print row
        if bool(row):
            result = row
        else:
            result = {"result": "failure", "msg": "Something went wrong. Please try again"}
    except Exception, e:
        logging.error(str(e))
        result = {"result": "failure", "msg": "Something went wrong. Please try again"}
    return result	