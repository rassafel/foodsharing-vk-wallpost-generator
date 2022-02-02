import vk_api


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
        print("List photos for loading is empty.")
        return
    assert album_id, "Album id cannot be None."

    photos = vk_api.VkUpload(api).photo(
        album_id=album_id,
        photos=photos,
        group_id=group_id
    )
    print("Start loading photos to VK.")
    photos = list(map(lambda photo: f"photo{photo['owner_id']}_{photo['id']}", photos))
    print("Finish loading photos to VK. Loaded photos:", photos)
    return ",".join(photos)


def upload_post(api,
                message,
                group_id,
                attachments=None,
                lat=None,
                long=None,
                **kwargs):
    post_id = api.wall.post(message=message,
                            owner_id=f"-{group_id}",
                            from_group=1,
                            lat=lat,
                            long=long,
                            mute_notifications=1,
                            attachments=attachments)
    print(f"Created post with id = {post_id} in group with id = {group_id}.")
