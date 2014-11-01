# -*- coding: utf-8 -*-

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
