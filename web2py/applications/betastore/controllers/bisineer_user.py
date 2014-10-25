# -*- coding: utf-8 -*-

import logging
import gluon.contrib.simplejson as json

logger = logging.getLogger("bisineer_user")
logger.setLevel(logging.DEBUG)

# try something like
def index(): return dict(message="hello from bisineer_user.py")

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
    # read post body
    print "inside register"
    result={"result":"failure"}
    response.headers['Access-Control-Allow-Headers'] = ['Content-Type']
    json_string = request.body.read()
#     print "print request body" + request.body.read()
#     logger.debug("raw json is " + request.body.read())
    user = json.loads(json_string)
    validate_user_result = validate_user(user)
    logger.debug("user validation result " + str(validate_user_result))
    if validate_user_result['result'] == "success":
        # encrypt password if validation passed
        my_crypt = CRYPT(key=auth.settings.hmac_key)
        user['password'] = my_crypt(user['password'].encode('utf8'))[0]
        user.pop('repeat_password')
        # insert into db if validation passed
        print "inserting user " + str(user)
        result = db.auth_user.insert(**user)
        print result
    else:
        result = validate_user_result
        print result
    return dict(result)

def validate_user(user):
    """
    1. checks if user already exists
    2. checks if passwords match
    """
    result={"result": "success"}
    row = db(db.auth_user.phone_number==user['phone_number']).select()
    if bool(row):
        result = {"result":"failure", "error_msg":"user already exists"}
    
    if user['password'] != user['repeat_password']:
        result = {"result":"failure", "error_msg":"ಪಾಸ್ವರ್ಡ್ಗಳು ಹೊಂದಿಕೆಯಾಗುತ್ತಿಲ್ಲ"}
    return result
