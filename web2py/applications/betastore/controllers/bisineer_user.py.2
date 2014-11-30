# -*- coding: utf-8 -*-

import gluon.contrib.simplejson as json

# try something like
def index(): return dict(message="hello from bisineer_user.py")

def register():
    json_string = request.body.read()
    user = json.loads(json_string)
    user['password'] = user['password'].encode('utf8')
    user = auth.register_bare(**user)
    print str(user)
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
    try:
        json_string = request.body.read()
        user = json.loads(json_string)
        user['password'] = user['password'].encode('utf-8')
        user = auth.login_bare(user['email'], user['password']);
        if auth.is_logged_in():
            result = dict(session.auth.user);
        else:
            result = {"result": "failure", "msg": "email and password don't match"}
    except Exception, e:
        logger.error(str(e))
        result = {"result": "failure", "msg": "Ouch!! something went wrong. Please try again"}
    return result

def logout():
    try:
        session.auth = None
        session.flash = auth.messages.logged_out
        result = {"result": "success", "msg": "successfully logged out"}
    except Exception, e:
        logger.error(str(e))
        result = {"result": "failure", "msg": "Ouch!! something went wrong. Please try again"}
    print result
    return result

@auth.requires_login()
def get_user():
    try:
        result = dict(session.auth.user);
    except Exception, e:
        logger.error(str(e));
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
        logger.error(str(e))
        result = {"result": "failure", "msg": "Something went wrong. Please try again"}
    return result
