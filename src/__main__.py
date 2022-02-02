from generator_util import *
from vk_util import *


def load_env():
    login = os.getenv("LOGIN")
    if login:
        login = input("Input VK login: ")
    assert login, "LOGIN cannot be empty."

    group_id = os.getenv("GROUP_ID")
    if group_id:
        group_id = input("Input VK group id: ")
    assert group_id, "GROUP_ID cannot be empty."
    group_id = abs(int(group_id))

    password = os.getenv("PASSWORD")

    album_id = os.getenv("ALBUM_ID")
    if album_id:
        album_id = input()

    lat, long = None, None
    if bool(random.getrandbits(1)):
        lat, long = 53.2127536, 50.1324342
        print("Post point: ", lat, long)
    else:
        print("Post point is None.")
    return \
        {
            "login": login,
            "password": password,
            "group_id": group_id,
            "album_id": album_id,
            "lat": lat,
            "long": long
        }


resources_path = "./resources/"
templates_path = f"{resources_path}templates"
products_path = f"{resources_path}products.txt"
names_path = f"{resources_path}names.csv"
places_path = f"{resources_path}places.csv"
images_path = f"{resources_path}img/"

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
