# from gluon.storage import Storage
from gluon import *
# from daos import auth_user_dao
import uuid

logger = current.logger


def _validate_before_save(address):
    """
    Validate address before saving it to the DB

    :param address:
    :return:
    """
    return True


def save_address(address):
    """
    updates if found else inserts new address into the DB. Returns the same address after populating id and code

    :param address: db.bis_address
    :return: db.bis_address - newly saved address if successfully saved or else None
    :input json:
    {"name": "home address", "street_address": "1st A main road, samrat layout, Arekere",
    "landmark": "opposite to Reliance Mart", "city": "Bangalore", "state": "Karnataka", "country": "India",
    "pincode": "560076", "phone_number": "9900995001"}
    """
    if address.code is not None:
        existing_address = current.db(current.db.bis_address.code == address.code).select().first()
    elif address.id is not None:
        existing_address = current.db(current.db.bis_address.id == address.id).select().first()
    if existing_address is not None:
        address.code = existing_address.code
        if _validate_before_save(address):
            address = current.db(current.db.bis_address.code == existing_address.code).update(**address)
    else:
        address.code = str(uuid.uuid4())
        address.id = current.db.bis_address.insert(**address)
    return address


def get_address(id):
    """
    Returns address by id

    :param id: id of the address
    :return: db.bis_address - address for the ID given
    """
    pass


def delete_address(id):
    """
    Deletes address from the system based on the id

    :param id: id of the address to be deleted
    :return: Boolean - true if successfully deleted else false
    """
    pass


def update_address(address):
    """
    Updates address in the DB

    :param address: db.bis_address - address to be updated
    :return: db.bis_address - updated address if successfully updated or else None
    """


def get_addresses(user):
    """
    Returns addresses for the user

    :param user: db.bis_auth_user - user for whom addresses has to be retrieved
    :return: db.bis_address - array of addresses for the specified user
    """
    pass