import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_products")
logger.setLevel(logging.DEBUG)

def get_products():
	"""
	result: {
		count: 1000,


	}
	"""
	try:
		result = {}
		query = db.bis_product.id > 0
		fields = ['name','unit_price', 'description_short']
		none_fields = ['categories', 'specifications', 'weight', 'product_attributes', 'volume', 'bis_category', 'variant_products', 'description_long', 'tax_rate', 'in_stock', '']
		sel = [db.bis_product[field] for field in fields]
		rows = db().select(db.bis_product.ALL, cache=(cache.ram,60), cacheable=True, orderby=db.bis_product.name, limitby=(0,20))
		# this for loop is because of gae with web2py. If we have to select specific fields, 
		#then we need to use projection=True in the query. But if we use projection=True, it doesn't allow to use limitby
		if bool(rows):
			for row in rows:
				for field in none_fields:
					row[field] = None
		#rows = db().select(*sel, projection=True, cache=(cache.ram,60), cacheable=True) # use this for caching
		print rows
		if bool(rows):
			result['products'] = rows
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