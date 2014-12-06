from gluon.storage import Storage
import gluon.contrib.simplejson as json
import traceback

def login():
    try:
        print("reading body " + str(request.body.read()))
        print("variables are " + str(request.post_vars))
        input_json = request.body.read()
        # user = Storage(json.loads(input_json))
        user = request.post_vars
        user.password = user.password.encode('utf-8')
        user = auth.login_bare(user.email, user.password);
    except Exception, e:
        #current.logger.error(e)
        traceback.print_exc()
        raise HTTP(500, "Ouch!! something went wrong. Please try again later")
    if auth.is_logged_in():
        return dict(session.auth.user);
    else:
        raise HTTP(510, "email and password don't match")