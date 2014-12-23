from gluon import *


logger = current.logger

unwanted_attributes = ["id", "type", "user_id", "user_group_id", "order_id", "created_on", "modified_on"]


def clean(addresses):
    logger.debug("inside clean()")
    for address in addresses:
        logger.debug(address)
        for key in unwanted_attributes:
            if key in address:
                del address[key]
