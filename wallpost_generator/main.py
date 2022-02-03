# -*- coding: utf-8 -*-
from generator_util import *
from vk_util import *

log = logging.getLogger(__name__)


def load_env():
    login = os.getenv("LOGIN") or input("Input VK login: ")
    if not login:
        log.error("Login cannot be empty")
        raise RuntimeError("Login cannot be empty")

    group_id = os.getenv("GROUP_ID") or input("Input VK group id: ")
    if not group_id:
        log.error("Group id cannot be empty")
        raise RuntimeError("Group id cannot be empty")
    group_id = abs(int(group_id))

    password = os.getenv("PASSWORD")

    album_id = os.getenv("ALBUM_ID") or input("Input VK album id: ")

    lat, long = None, None
    if bool(random.getrandbits(1)):
        lat, long = 53.2127536, 50.1324342
        log.info("Post point: %s %s", lat, long)
    else:
        log.info("Post point is None")
    return \
        {
            "login": login,
            "password": password,
            "group_id": group_id,
            "album_id": album_id,
            "lat": lat,
            "long": long
        }


def main(templates_path,
         products_path,
         names_path,
         places_path,
         images_path):
    env = load_env()
    api = init_api(**env)
    photos = get_photos(images_path=images_path,
                        min_count=1,
                        max_count=10)

    attachments = upload_photo(api=api,
                               photos=photos,
                               **env)

    message = load_and_render(templates_path=templates_path,
                              products_path=products_path,
                              names_path=names_path,
                              places_path=places_path)
    upload_post(api=api,
                message=message,
                attachments=attachments,
                **env)
