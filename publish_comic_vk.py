import os

import requests

from dotenv import load_dotenv

from download_random_comic import (
    get_last_comic_number,
    download_comic_image,
    fetch_comic
)


def get_upload_url(group_id, access_token, vk_api_version):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    params = {
        'group_id': group_id,
        'access_token': access_token,
        'v': vk_api_version
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    upload_url = response.json()['response']['upload_url']
    return upload_url


def upload_image(filename, upload_url):
    with open(filename, 'rb') as file:
        url = upload_url
        files = {
            'photo': file,
        }
        response = requests.post(url, files=files)
        response.raise_for_status()
        uploaded_image = response.json()
        return uploaded_image


def save_vk_image(group_id, vk_token, uploaded_image, vk_api_version):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'

    params = {
        'group_id': group_id,
        'access_token': vk_token,
        'v': vk_api_version,
        'server': uploaded_image['server'],
        'photo': uploaded_image['photo'],
        'hash': uploaded_image['hash']
    }
    response = requests.post(url, params=params)
    response.raise_for_status()
    saved_image = response.json()['response']
    for params in saved_image:
        owner_id = params['owner_id']
        image_id = params['id']
        return owner_id, image_id


def publish_comic(comic_comment, group_id,
                  vk_token, vk_api_version,
                  owner_id, image_id):
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
    response.raise_for_status()


if __name__ == '__main__':
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    group_id = os.environ['VK_GROUP_ID']
    filename = 'comic.jpg'
    vk_api_version = '5.131'

    last_comic_number = get_last_comic_number()
    comic_link, comic_comment = fetch_comic(last_comic_number)
    download_comic_image(filename, comic_link)

    upload_url = get_upload_url(group_id, vk_token, vk_api_version)
    uploaded_image = upload_image(filename, upload_url)
    owner_id, image_id = save_vk_image(
        group_id, vk_token,
        uploaded_image, vk_api_version
    )
    publish_comic(
        comic_comment, group_id,
        vk_token, vk_api_version,
        owner_id, image_id
    )
    os.remove(filename)
