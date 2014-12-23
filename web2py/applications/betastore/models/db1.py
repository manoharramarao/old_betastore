# -*- coding: utf-8 -*-
from gluon.custom_import import track_changes;
track_changes(True)  # this is used to reload modules during import, if they are changed
from gluon import current
from gluon.storage import Storage
import uuid
from datetime import datetime
import logging


if False:
    from gluon import *
    from db import *
# if False:
#     from gluon import *
#     request = current.request
#     response = current.response
#     session = current.response
#     cache = current.cache
#     db = current.db
#     auth = current.auth

logger = logging.getLogger("web2py.app.betastore")
logger.setLevel(logging.DEBUG) # remove this when you go live
current.logger = logging.getLogger("web2py.app.betastore")
current.logger.setLevel(logging.DEBUG) # remove this when you go live
current.db = db
auth.settings.create_user_groups = False
current.betastore_current = Storage()

# GAE_NOTE uuid did not work so code is defined in each and every table

# catalog table
db.define_table(
    'bis_catalog',
    Field('name', required=True),
    Field('description', required=True),
    Field('code', represent=lambda p,r: '%s' %(r.name)),
    Field('uuid', length=64, default=lambda:str(uuid.uuid4())),
    format='%(name)s'
)

# category table
db.define_table(
    'bis_category',
    Field('name', required=True),
    Field('description', required=True),
    Field('catalogs', 'list:string'),
    Field('categories', 'list:string'),
    Field('code', represent=lambda p,r: '%s' %(r.name)),
    format='%(name)s'
)

# product table
db.define_table(
    'bis_product',
    Field('categories', 'list:string'),
    Field('name', required=True),
    Field('display_name', 'string'),
    Field('description_short', 'string', required=True),
    Field('description_long', 'text'),
    Field('unit_price', 'double'),
    Field('on_sale', 'boolean'),
    Field('rating', 'double'),
    Field('image_urls', 'list:string'),
    Field('in_stock', 'integer'),
    Field('tax_rate', 'double'),
    Field('volume', 'list:integer'),
    Field('weight', 'double'),
    Field('variant_products', 'list:string'),
    Field('composit_products', 'list:string'),
    Field('product_attributes', 'json'),
    Field('specifications', 'text'),
    Field('code', represent=lambda p,r: '%s' %(r.name)),
    format='%(name)s'
)

db.define_table(
    'bis_price_type',
    Field('name', required=True),
    Field('price_description'),
    Field('code', represent=lambda p,r: '%s' %(r.name)),
    format='%(name)s'
)

db.define_table(
    'bis_price',
    Field('product_code'),
    Field('price_type_code'),
    Field('amount', 'double', required=True),
    Field('user_group_code'),
    Field('code'),
    format=lambda r: '%s-%s-%s' % (r.product, r.user_group, r.price_type)
)

# db.define_table(
#     'bis_price',
#     Field('product', 'reference bis_product'),
#     Field('price_type', 'reference bis_price_type'),
#     Field('amount', 'double', required=True),
#     Field('user_group', 'reference auth_group'),
#     Field('code', represent=lambda p,r: '%s-%s-%s' %(r.product.name, r.user_group.role, r.price_type.name)),
#     format=lambda r: '%s-%s-%s' %(r.product.name, r.user_group.role, r.price_type.name)
# )

# cart and order - same table is being used
db.define_table(
    'bis_cart_order',
    Field('user_code'), # GAE_NOTE didn't specify represent attribute so no dropdown will be shown in admin tool
    Field('billing_code'),
    Field('shipping_code'),
    Field('created_on', 'datetime', default=request.now),
    Field('modified_on', 'datetime', default=datetime.now()),
    Field('status'),
    Field('product_cost', 'double'),
    Field('total_amount', 'double'),
    Field('discount', 'double'),
    Field('tax', 'double'),
    Field('shipping_cost', 'double'),
    Field('amount_due', 'double'),
    Field('amount_paid', 'double'),
    Field('line_items', 'list:string'),
    Field('code', length=64, default=lambda: str(uuid.uuid4()))
)

# order line items - 1 line item per product in the order
db.define_table(
    'bis_line_item',
    Field('order_code'),  # not creating actual reference because no.of order might grow very large and admin app might
    # fail in preparing dropdown
    Field('product_code'),
    Field('quantity', 'integer'),
    Field('unit_price', 'double'),
    Field('total_amount', 'double'),
    Field('discount', 'double'),
    Field('tax', 'double'),
    Field('created_on', 'datetime', default=request.now),
    Field('modified_on', 'datetime', default=datetime.now()),  # TODO give the default value
    Field('description_short', 'string', required=True),
    Field('name', required=True),
    Field('code', length=64, default=lambda: str(uuid.uuid4()))
)

db.bis_line_item.created_on.readable = db.bis_line_item.created_on.writable = False
db.bis_cart_order.created_on.readable = db.bis_cart_order.created_on.writable = False

# for future, when you use mongoDB, probably you can merge these
db.define_table(
    'bis_delivery',
    Field('order_code'),
    Field('delivered_on' 'datetime'),
    Field('invoice_code'),
    Field('code')
)

# for future
db.define_table(
    'bis_invoice',
    Field('invoice_item_code'),
    Field('code')
)

# for future
db.define_table(
    'bis_invoice_item',
    Field('product_code'),
    Field('quantity'),
    Field('amount'),
    Field('code')
)

# product features table
db.define_table(
    'product_features',
    Field('product_code', 'list:string'),
    Field('feature', 'text'),
    Field('code')
)

# products list table
db.define_table(
    'bis_products_list',
    Field('products', 'json'),
    Field('code')
)

# address table
db.define_table(
    'bis_address',
    Field('name'),
    Field('street_address'),
    Field('landmark'),
    Field('city'),
    Field('bis_state'),
    Field('country'),
    Field('pincode'),
    Field('phone_number'),
    Field('bis_type'),
    Field('user_code'),
    Field('user_group_code'),
    Field('order_code'),
    Field('created_on','datetime'),
    Field('modified_on', 'datetime'),
    Field('code')
)





####################################################################################################

# TODO The below statements should be executed if someone is accessing admin application. Because, these
#models are executed for each and every request. But you really don't want to run this on every request

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
# TODO gae-note - get the value of code directly and not from name. This did not work with GAE. so doing it with name
global_temp_bis_catalog_codes = db(db['bis_catalog']).select(db['bis_catalog'].name).as_list()
global_bis_catalog_codes = []
for catalog_code in global_temp_bis_catalog_codes:
    global_bis_catalog_codes.append(dict(catalog_code)['name'])

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
global_temp_bis_category_codes = db(db['bis_category']).select(db['bis_category'].name).as_list()
global_bis_category_codes = []
for category_code in global_temp_bis_category_codes:
    global_bis_category_codes.append(dict(category_code)['name'])

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
global_temp_bis_product_codes = db(db['bis_product']).select(db['bis_product'].name, db['bis_product'].id).as_list()
global_bis_product_codes = []
for product_code in global_temp_bis_product_codes:
    product_code = dict(product_code)
    global_bis_product_codes.append(product_code['name'])

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
global_temp_bis_price_type_codes = db(db['bis_price_type']).select(db['bis_price_type'].name, db['bis_price_type'].id).as_list()
global_bis_price_type_codes = []
for price_type_code in global_temp_bis_price_type_codes:
    price_type_code = dict(price_type_code)
    global_bis_price_type_codes.append(price_type_code['name'])

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
global_temp_auth_group_codes = db(db['auth_group']).select(db['auth_group'].role, db['auth_group'].id).as_list()
global_auth_group_codes = []
for auth_group_code in global_temp_auth_group_codes:
    auth_group_code = dict(auth_group_code)
    global_auth_group_codes.append(auth_group_code['role'])

db['bis_category'].catalogs.requires = IS_IN_SET(global_bis_catalog_codes,multiple=True)
db['bis_product'].variant_products.requires = IS_IN_SET(global_bis_product_codes, multiple=True)
db['bis_product'].categories.requires=requires = IS_IN_SET(global_bis_category_codes, multiple=True)
db['bis_price'].product_code.requires = IS_IN_SET(global_bis_product_codes)
db['bis_price'].price_type_code.requires = IS_IN_SET(global_bis_price_type_codes)
db['bis_price'].user_group_code.requires = IS_IN_SET(global_auth_group_codes)
db['bis_price'].code.represent = lambda p,r: '%s-%s-%s' %(r.product_code, r.user_group_code, r.price_type_code)
db['bis_line_item'].product_code.requires = IS_IN_SET(global_bis_product_codes)
#db['bis_line_item'].code.represent=lambda p,r: '%s-%s' %(r.product_code, r.id)

# GAE_NOTE attribute default on code doesn't populate value. So using attribute represent
#db['bis_cart_order'].code.represent=lambda p,r: '%s-%s' %(r.user_code, r.id)

# below ones will change. They are yet to implement
db['bis_delivery'].code.represent=lambda p,r: '%s' %(r.id)
db['bis_invoice'].code.represent=lambda p,r: '%s' %(r.id)
db['bis_invoice_item'].code.represent=lambda p,r: '%s' %(r.id)
db['product_features'].code.represent=lambda p,r: '%s' %(r.id)
db['bis_products_list'].code.represent=lambda p,r: '%s' %(r.id)
db['bis_address'].code.represent=lambda p,r: '%s' %(r.id)

db['product_features'].product_code.requires=IS_IN_SET(global_bis_product_codes)