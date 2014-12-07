# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
#from gluon.contrib.gql import GQLDB
#db=GQLDB()


import logging

logger = logging.getLogger("web2py.app.betastore")
logger.setLevel(logging.DEBUG) # remove this when you go live


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite',pool_size=1,check_reserved=['all'], lazy_tables=True)
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb', lazy_tables=True)
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
#response.generic_patterns = ['*'] if request.is_local else []
response.generic_patterns = ['json']

## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

# edited by team
auth.settings.extra_fields['auth_user'] = [
    #Field('phone_number', requires=IS_MATCH('\d{2}\-\d{2}\-\d{2}\-\d{4}')),
    Field('phone_number', 'string', required=True),
    Field('code', represent=lambda p,r: '%s-%s' %(r.email, r.phone_number))
]
auth.define_tables()
# TODO add secure=True to the above argument so that login is done only on https

## create all tables needed by auth if not custom tables
#auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.janrain_account import use_janrain
use_janrain(auth, filename='private/janrain.key')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

# db.define_table(
#     'catalog',
#     Field('name'),
#     Field('description'),
#     format='%(name)s'
# )

# # category table
# db.define_table(
#     'category',
#     Field('name'),
#     Field('description'),
#     Field('catalogs', 'list:string', default='default')
# )

# # product table
# db.define_table(
#     'product',
#     Field('categories', 'list:string'),
#     Field('name', required=True),
#     Field('description_short', 'text'),
#     Field('description_long', 'text'),
#     Field('unit_price', 'double'),
#     Field('on_sale', 'boolean'),
#     Field('rating', 'double'),
#     Field('image_urls', 'list:string'),
#     Field('in_stock', 'integer'),
#     Field('tax_rate', 'double'),
#     Field('volume', 'list:integer'),
#     Field('weight', 'double'),
#     Field('variant_products', 'list:string'),
#     format='%(name)s'
# )
