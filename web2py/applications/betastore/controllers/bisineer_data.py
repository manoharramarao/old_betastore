import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_data")
logger.setLevel(logging.DEBUG)

#@auth.requires(requires_login=True, requires_membership='admin')
def import_bisineer_data():
    db.import_from_csv_file(open('/home/manohar/work/bisineer_store/web2py/applications/betastore/beta_store_data.csv', 'r'))
    result = {"result": "success"}
    return result

#@auth.requires(requires_login=True, requires_membership='admin')
def export():
    db.export_to_csv_file(open('/tmp/bisineer_data_exported.csv', 'wb'))
    result = {"result": "success"}
    return result

def delete():
	#db(db.auth_permission.id > 0).delete()
	#db(db.auth_membership.id > 0).delete()
	#db(db.auth_group.id > 0).delete()
	#db(db.auth_user.id > 0).delete()
	db(db.bis_product.id > 0).delete()
	#db(db.bis_category.id > 0).delete()
	#db(db.bis_catalog.id > 0).delete()
	return