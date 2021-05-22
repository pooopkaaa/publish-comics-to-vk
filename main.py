import os
import random

import requests
from dotenv import load_dotenv
from requests.api import get


def get_response_get(url, payload=None):
    response = requests.get(url, payload)
    response.raise_for_status()
    return response


def get_response_post(url, files):
    response = requests.post(url, files=files)
    response.raise_for_status()
    return response


def get_comics_amount():
    url = 'https://xkcd.com/info.0.json'
    response = get_response_get(url).json()
    return response['num']


def download_comic(filename, url):
    response = get_response_get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_url_for_upload_image(**payload):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = get_response_get(url, payload)
    return response.json()['response']['upload_url']


def upload_image(url, filename):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = get_response_post(url, files)
        return response.json()


def lock_uploaded_image(**payload):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = get_response_get(url, payload).json()['response'][0]
    return response['id'], response['owner_id']


def publish_uploaded_image(**payload):
    url = 'https://api.vk.com/method/wall.post'
    response = get_response_get(url, payload)
    return response.json()['response']['post_id']


def main():
    load_dotenv()
    comics_amount = get_comics_amount()
    comic_number = random.randint(1, comics_amount)
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    try:
        response = get_response_get(url)

        comic_description = response.json()

        comic_name = comic_description['safe_title']
        comic_filename = f'{comic_name}.png'
        comic_url = comic_description['img']
        author_comment = comic_description['alt']

        download_comic(comic_filename, comic_url)

        VK_ACCESS_TOKEN = os.getenv('VK_ACCESS_TOKEN')
        VK_GROUP_ID = os.getenv('VK_GROUP_ID')
        VK_API_VERSION = os.getenv('VK_API_VERSION')

        assigned_url = get_url_for_upload_image(
            group_id=VK_GROUP_ID,
            access_token=VK_ACCESS_TOKEN,
            v=VK_API_VERSION
        )

        uploaded_foto_parameters = upload_image(assigned_url, comic_filename)

        media_id, owner_id = lock_uploaded_image(
            group_id=VK_GROUP_ID,
            **uploaded_foto_parameters,
            access_token=VK_ACCESS_TOKEN,
            v=VK_API_VERSION
        )
        publish_uploaded_image(
            owner_id=f'-{VK_GROUP_ID}',
            from_group=1,
            attachments=f'photo{owner_id}_{media_id}',
            access_token=VK_ACCESS_TOKEN,
            v=VK_API_VERSION,
            message=author_comment
        )

        os.remove(comic_filename)

    except requests.exceptions.HTTPError as http_error:
        print(f'Error -> {http_error}')


if __name__ == '__main__':
    main()
