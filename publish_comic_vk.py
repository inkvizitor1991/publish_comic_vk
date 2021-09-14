import os

import requests

from dotenv import load_dotenv

from download_random_comic import (
    get_last_comic_number,
    download_comic_image,
    fetch_comic
)


def check_vk_response(response):
    response.raise_for_status()
    response = response.json()
    if 'error' in response:
        raise requests.HTTPError(response['error']['error_msg'])
    return response


def get_upload_url(group_id, access_token, vk_api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': vk_api_version
    }
    response = requests.post(url, params=params)
    response = check_vk_response(response)
    upload_url = response['response']['upload_url']
    return upload_url


def upload_vk_image(filename, upload_url):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = requests.post(upload_url, files=files)
    response = check_vk_response(response)
    server = response['server']
    image = response['photo']
    image_hash = response['hash']
    return server, image, image_hash


def save_vk_image(group_id, vk_token, vk_api_version,
                  server, image, image_hash):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'group_id': group_id,
        'access_token': vk_token,
        'v': vk_api_version,
        'server': server,
        'photo': image,
        'hash': image_hash
    }
    response = requests.post(url, params=params)
    response = check_vk_response(response)
    saved_image = response['response'][0]
    owner_id = saved_image['owner_id']
    image_id = saved_image['id']
    return owner_id, image_id


def publish_comic(comic_comment, group_id, vk_token,
                  vk_api_version, owner_id, image_id):
    url = 'https://api.vk.com/method/wall.post'
    params = {
        'owner_id': -int(group_id),
        'access_token': vk_token,
        'v': vk_api_version,
        'from_group': 1,
        'message': comic_comment,
        'attachments': f'photo{owner_id}_{image_id}'
    }
    response = requests.post(url, params=params)
    check_vk_response(response)


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    filename = 'comic.jpg'
    vk_api_version = '5.131'

    last_comic_number = get_last_comic_number()
    comic_link, comic_comment = fetch_comic(last_comic_number)
    download_comic_image(filename, comic_link)
    try:
        upload_url = get_upload_url(group_id, vk_token, vk_api_version)
        server, image, image_hash = upload_vk_image(filename, upload_url)
        owner_id, image_id = save_vk_image(
            group_id, vk_token, vk_api_version,
            server, image, image_hash
        )
        publish_comic(
            comic_comment, group_id,
            vk_token, vk_api_version,
            owner_id, image_id
        )
    except requests.HTTPError as error:
        print(error)
    finally:
        os.remove(filename)
