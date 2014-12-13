# -*- coding: utf-8 -*-
from gluon.storage import Storage
import gluon.contrib.simplejson as json
from bisineer_http_status_codes import HTTPStatusCodes
# try something like
def index(): return dict(message="hello from bisineer_user.py")

def register():
    """
    registers user by using auth.bare_register method
    """
    try:
        msg = 'Ouch!! something went wrong. Please try again later'
        input_json = request.body.read()
        user = Storage(json.loads(input_json))
        result = Storage()
        user.password = user.password.encode('utf8')
        user.code = str(user.email) + "-" + str(user.phone_number)
        user = auth.register_bare(**user)
        if user is not None:
            default_group = db(db.auth_group.role=="default").select().first().as_dict()
            current.logger.debug("group is " + str(default_group))
            current.logger.debug("user is " + str(user))
            auth.add_membership(default_group['id'], user.id) # add user to default user group
            logger.debug("user returned is " + str(user))
            result.msg = "Registration success"
            return result
        else:
            msg="Registration failed"
            raise HTTP(500, msg)
    except Exception, e:
        logger.error(str(e))
        raise HTTP(500, msg)
        

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
        input_json = request.body.read()
        user = Storage(json.loads(input_json))
        user.password = user.password.encode('utf-8')
        user = auth.login_bare(user.email, user.password);
    except Exception, e:
        logger.error(e)
        raise HTTP(500, "Ouch!! something went wrong. Please try again later")
    if auth.is_logged_in():
        return dict(session.auth.user);
    else:
        raise HTTP(510, "email and password don't match")
    
def is_logged_in():
    if auth.is_logged_in():
        return dict(session.auth.user)
    else:
        raise HTTP(401, 'anonymous user')


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
