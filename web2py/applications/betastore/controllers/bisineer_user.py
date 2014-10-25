# -*- coding: utf-8 -*-

import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_user")
logger.setLevel(logging.DEBUG)

# try something like
def index(): return dict(message="hello from bisineer_user.py")

# def register():
#     """
#     1. checks if the user already exists
#     2. if it is new user, then saves data to DB
#     input json - 
#     {
#         "first_name": "Manohar'",
#         "last_name": "Sangeetham Ramarao",
#         "email": "manohar@gmail.com",
#         "phone_number": "99-00-99-5840",
#         "password": "test1234",
#         "repeat_password": "test1234"
#     }
#     output jsons - 
#     {'result': 'success', 'message': 'user registered successfully'}
#     or
#     {'result': 'failure', 'message': 'user registration failed'}
#     """
#     result = {}
# 	# read post body
#     print "inside register"
# 	#print request.env.web2py_runtime_gae
#     response.headers['Access-Control-Allow-Headers'] = ['Content-Type']
#     json_string = request.body.read()
#     user = json.loads(json_string)
#     validate_user_result = validate_user(user)
#     if validate_user_result['result'] == "success":
#         # encrypt password if validation passed
#         my_crypt = CRYPT(key=auth.settings.hmac_key)
#         user['password'] = my_crypt(user['password'].encode('utf8'))[0]
#         user.pop('repeat_password')
#         # insert into db if validation passed
#         print "inserting user " + str(user)
#         row = db.auth_user.insert(**user).as_dict()
#         if bool(row):
#             result = {"result": "success", "msg": "Registration successful"}
#     else:
#         result = validate_user_result
#     return result

def register():
    """
    1. checks if the user already exists
    2. if it is new user, then saves data to DB
    input json - 
    {
        "first_name": "Manohar'",
        "last_name": "Sangeetham Ramarao",
        "email": "manohar@gmail.com",
        "phone_number": "99-00-99-5840",
        "password": "test1234",
        "repeat_password": "test1234"
    }
    output jsons - 
    {'result': 'success', 'message': 'user registered successfully'}
    or
    {'result': 'failure', 'message': 'user registration failed'}
    """
    json_string = request.body.read()
    user = json.loads(json_string)
    user['password'] = user['password'].encode('utf8')
    user = auth.register_bare(**user)
    if user:
        result = {"result": "success", "msg": "Registration successful"}
    else:
        result = {"result": "failure", "msg": "Registration failed"}
    return result

def validate_user(user):
    """
    1. checks if user already exists
    2. checks if passwords match
    """
    result={"result": "success"}
    row = db(db.auth_user.phone_number==user['phone_number']).select().as_dict()
    if bool(row):
        result = {"result":"failure", "msg":"user already exists"}
    
    if user['password'] != user['repeat_password']:
        result = {"result":"failure", "msg":"ಪಾಸ್ವರ್ಡ್ಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ"}
    return result

def login():
    json_string = request.body.read()
    user = json.loads(json_string)
    user['password'] = user['password'].encode('utf-8')
    user = auth.login_bare(user['email'], user['password']);
    if auth.is_logged_in():
        return dict(session.auth.user)
    return {"result": "failure", "msg": "email and password don't match"}

def logout():
    session.auth = None
    session.flash = auth.messages.logged_out
    return

@auth.requires_login()
def get_session_user():
    return dict(session.auth.user)