import vk_api

from config import VK_TOKEN, VK_APP_ID, LOGIN, PSW, VK_CLIENT_SECRET
from constants import VK_PERMISSIONS


def captcha_handler(captcha):
    pass


session = vk_api.VkApi(token=VK_TOKEN, client_secret=VK_CLIENT_SECRET, app_id=VK_APP_ID, scope=VK_PERMISSIONS,
                       captcha_handler=captcha_handler, login=LOGIN, password=PSW)  # token=VK_TOKEN, app_id=VK_APP_ID,
session.auth(token_only=True)
api = session.get_api()
