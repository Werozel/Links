import logging
from globals import api


def private_profile(exc, info=""):
    info = str(info)
    if info != "":
        logging.error("Profile \"" + info + "\" is private!")
    logging.error(exc)


def users_get_error(exc, info=""):
    info = str(info)
    if info != "":
        logging.error(info)
    logging.error(exc)


def get_mutual_error(exc, info=""):
    info = str(info)
    if info != "":
        logging.error(info)
    logging.error(exc)