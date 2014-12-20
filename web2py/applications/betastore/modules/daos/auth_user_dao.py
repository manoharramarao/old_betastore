from gluon.storage import Storage
from gluon import *


def get_user_code(id):
    row = current.db(current.db.auth_user.id == id).select().first().as_dict()
    return row['code']