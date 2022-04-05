# -*- coding: utf-8 -*-
import logging

import vk_api

log = logging.getLogger(__name__)


def captcha_handler(captcha):
    key = input("Enter captcha code {0}: ".format(captcha.get_url())).strip()
    return captcha.try_again(key)


def init_api(login,
             password=None,
             config_filename="resources/config.v2.json",
             api_version='5.131',
             **kwargs):
    session = vk_api.VkApi(login,
                           password,
                           api_version=api_version,
                           captcha_handler=captcha_handler,
                           config_filename=config_filename
                           )
    session.auth()
    return session.get_api()


def upload_photo(api,
                 album_id,
                 group_id,
                 photos=None,
                 **kwargs):
    if not photos:
        log.info("List photos for loading is empty")
        return
    assert album_id, "Album id cannot be None"

    photos = vk_api.VkUpload(api).photo(
        album_id=album_id,
        photos=photos,
        group_id=group_id
    )
    log.info("Start loading photos to VK")
    photos = list(
        map(lambda photo: f"photo{photo['owner_id']}_{photo['id']}", photos))
    log.info("Finish loading photos to VK. Loaded photos: %s", photos)
    return ",".join(photos)


def upload_post(api,
                message,
                group_id,
                attachments=None,
                lat=None,
                long=None,
                **kwargs):
    result = post_id = api.wall.post(message=message,
                                     owner_id=f"-{group_id}",
                                     from_group=1,
                                     lat=lat,
                                     long=long,
                                     mute_notifications=1,
                                     attachments=attachments)
    log.info("Created post with id = %s in group with id = %s",
             result["post_id"], group_id)
