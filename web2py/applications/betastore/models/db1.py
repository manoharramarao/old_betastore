# -*- coding: utf-8 -*-
from gluon.custom_import import track_changes; track_changes(True) # this is used to reload modules during import, if they are changed
from gluon import current
from gluon.storage import Storage

logger = logging.getLogger("web2py.app.betastore")
logger.setLevel(logging.DEBUG) # remove this when you go live
current.logger = logging.getLogger("web2py.app.betastore")
current.logger.setLevel(logging.DEBUG) # remove this when you go live
current.db = db
auth.settings.create_user_groups = False
current.betastore_current = Storage()

# catalog table
db.define_table(
    'bis_catalog',
    Field('name', required=True),
    Field('description', required=True),
    Field('code', compute=lambda r: '%s' %(r.name)),
    format='%(name)s'
)

# category table
db.define_table(
    'bis_category',
    Field('name', required=True),
    Field('description', required=True),
    Field('catalogs', 'list:string'),
    Field('code', compute=lambda r: r.name),
    format='%(name)s'
)

# product table
db.define_table(
    'bis_product',
    Field('categories', 'list:string'),
    Field('name', required=True),
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
    Field('product_attributes', 'json'),
    Field('specifications', 'text'),
    Field('code', compute=lambda r: r.name),
    format='%(name)s'
)

db.define_table(
    'bis_price_type',
    Field('name', required=True),
    Field('price_description'),
    Field('code', compute=lambda r: r.name),
    format='%(name)s'
)

# db.define_table(
#     'bis_price',
#     Field('product'),
#     Field('price_type'),
#     Field('amount', 'double', required=True),
#     Field('user_group'),
#     Field('code', represent=lambda p,r: '%s-%s-%s' %(r.product, r.user_group, r.price_type)),
#     format=lambda r: '%s-%s-%s' %(r.product, r.user_group, r.price_type)
# )

db.define_table(
    'bis_price',
    Field('product', 'reference bis_product'),
    Field('price_type', 'reference bis_price_type'),
    Field('amount', 'double', required=True),
    Field('user_group', 'reference auth_group'),
    Field('code', represent=lambda p,r: '%s-%s-%s' %(r.product.name, r.user_group.role, r.price_type.name)),
    format=lambda r: '%s-%s-%s' %(r.product.name, r.user_group.role, r.price_type.name)
)

# cart and order - same table is being used
db.define_table(
    'bis_cart_order',
    Field('email'), # TODO need to change this relation to be based on user_id than email
    Field('billing_id'),
    Field('shipping_id'),
    Field('created_on','datetime'),
    Field('status'),
    Field('product_cost', 'double'),
    Field('total_amount', 'double'),
    Field('discount', 'double'),
    Field('tax', 'double'),
    Field('shipping_cost', 'double'),
    Field('amount_due', 'double'),
    Field('amount_paid', 'double'),
    Field('line_items', 'list:string')
)

# order line items - 1 line item per product in the order
db.define_table(
    'bis_line_item',
    Field('order_id'),
    Field('product_id'),
    Field('quantity', 'integer'),
    Field('total_amount', 'double'),
    Field('discount', 'double'),
    Field('tax', 'double'),
    Field('created_on','datetime'),
    Field('modified_on', 'datetime'),
    Field('description_short', 'string', required=True),
    Field('name', required=True),
)

# for future, when you use mongoDB, probably you can merge these
db.define_table(
    'bis_delivery',
    Field('order_id'),
    Field('delivered_on' 'datetime'),
    Field('invoice_id')
)

# for future
db.define_table(
    'bis_invoice',
    Field('invoice_item_id')
)

# for future
db.define_table(
    'bis_invoice_item',
    Field('product_id'),
    Field('quantity_id'),
    Field('amount'),
)

# product features table
db.define_table(
    'product_features',
    Field('product', 'reference bis_product'),
    Field('feature', 'text')
)

# products list table
db.define_table(
    'bis_products_list',
    Field('products', 'json')
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
    Field('user_id'),
    Field('user_group_id'),
    Field('order_id'),
    Field('created_on','datetime'),
    Field('modified_on', 'datetime')
)





####################################################################################################

# this part is just because of the GAE. looking at performance impact, we might have to remove this.
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

db['bis_category'].catalogs.requires=IS_IN_SET(global_bis_catalog_codes,multiple=True)
db['bis_product'].variant_products.requires=IS_IN_SET(global_bis_product_codes, multiple=True)
db['bis_product'].categories.requires=requires=IS_IN_SET(global_bis_category_codes, multiple=True)
# db['bis_price'].product.requires=IS_IN_SET(global_bis_product_codes, multiple=True)
# db['bis_price'].price_type.requires=IS_IN_SET(global_bis_price_type_codes, multiple=True)
# db['bis_price'].user_group.requires=IS_IN_SET(global_auth_group_codes, multiple=True)