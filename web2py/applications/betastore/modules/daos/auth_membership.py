from gluon.storage import Storage
from gluon import *

from daos import auth_group_dao


def get_memberships(user_id):
    # right now assuming all user will be in default group and prices will be fetched only for this group
    # as soon as we decide on what should happen when user belong to multiple groups, this method will return results for all groups
    rows = current.db((current.db.auth_membership.user_id == user_id) & (current.db.auth_membership.group_id==auth_group_dao.get_default_group_id())).select().as_dict()
    memberships = Storage(rows)
    return rows