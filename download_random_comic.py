import random

import requests


def get_last_comic_number():
    url = 'https://xkcd.com/info.0.json'
    response = requests.get(url)
    response.raise_for_status()
    last_comic_number = response.json()['num']
    return last_comic_number


def fetch_comic(last_comic_number):
    while True:
        number = random.randint(1, last_comic_number)
        url = f'https://xkcd.com/{number}/info.0.json'
        response = requests.get(url)
        if response.ok:
            break
    comic = response.json()
    comic_image_link = comic['img']
    comic_comment = comic['alt']
    return comic_image_link, comic_comment


def download_comic_image(filename, comic_image_link):
    response = requests.get(comic_image_link)
    response.raise_for_status()
    with open(filename, 'wb') as file:
        file.write(response.content)
