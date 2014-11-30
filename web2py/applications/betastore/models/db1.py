# -*- coding: utf-8 -*-
import logging
from gluon import current

logger = logging.getLogger("web2py.app.betastore")
logger.setLevel(logging.DEBUG) # remove this when you go live
current.db = db

# catalog table
db.define_table(
    'bis_catalog',
    Field('name'),
    Field('description'),
    format='%(name)s'
)

# category table
db.define_table(
    'bis_category',
    Field('name'),
    Field('description'),
    Field('catalogs', 'list:string', default='default')
)

# product table
db.define_table(
    'bis_product',
    Field('categories', 'list:string'),
    Field('name', required=True),
    Field('description_short', 'string'),
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
    format='%(name)s'
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
    Field('modified_on', 'datetime')
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
    Field('state'),
    Field('country'),
    Field('pincode'),
    Field('phone_number'),
    Field('type'),
    Field('user_id'),
    Field('user_group_id'),
    Field('order_id'),
    Field('created_on','datetime'),
    Field('modified_on', 'datetime')
)