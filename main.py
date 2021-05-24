import os
import random

import requests
from dotenv import load_dotenv


def get_response_get(url, payload=None):
    response = requests.get(url, payload)
    response.raise_for_status()
    return response


def get_response_post(url, files=None, payload=None):
    response = requests.post(url, files=files, data=payload)
    response.raise_for_status()
    converted_response = response.json()
    check_post_response(converted_response)
    return converted_response


def get_comic_description(comic_number):
    url = f'https://xkcd.com/{comic_number}/info.0.json'
    response = get_response_get(url)
    return response.json()


def check_post_response(response):
    if 'error' in response:
        raise requests.HTTPError(response['error']['error_code'])


def get_comics_amount():
    url = 'https://xkcd.com/info.0.json'
    response = get_response_get(url).json()
    return response['num']


def download_comic_image(filename, url):
    response = get_response_get(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def get_url_for_upload_image(**payload):
    url = 'https://api.vk.com/method/photos.getWallUploadServer'
    response = get_response_post(url, payload=payload)
    return response['response']['upload_url']


def upload_image(url, filename):
    with open(filename, 'rb') as file:
        files = {
            'photo': file,
        }
        response = get_response_post(url, files=files)
        return response


def lock_uploaded_image(**payload):
    url = 'https://api.vk.com/method/photos.saveWallPhoto'
    response = get_response_post(url, payload=payload)['response'][0]
    return response['id'], response['owner_id']


def publish_uploaded_image(**payload):
    url = 'https://api.vk.com/method/wall.post'
    response = get_response_post(url, payload=payload)
    return response['response']['post_id']


def main():
    load_dotenv()
    try:
        comics_amount = get_comics_amount()
        comic_number = random.randint(1, comics_amount)

        comic_description = get_comic_description(comic_number)

        comic_name = comic_description['safe_title']
        comic_filename = f'{comic_name}.png'
        comic_url = comic_description['img']
        author_comment = comic_description['alt']

        download_comic_image(comic_filename, comic_url)

        vk_access_token = os.getenv('VK_ACCESS_TOKEN')
        vk_group_id = os.getenv('VK_GROUP_ID')
        vk_api_version = os.getenv('VK_API_VERSION')

        assigned_url = get_url_for_upload_image(
            group_id=vk_group_id,
            access_token=vk_access_token,
            v=vk_api_version
        )

        uploaded_foto_parameters = upload_image(assigned_url, comic_filename)

        media_id, owner_id = lock_uploaded_image(
            group_id=vk_group_id,
            **uploaded_foto_parameters,
            access_token=vk_access_token,
            v=vk_api_version
        )
        publish_uploaded_image(
            owner_id=f'-{vk_group_id}',
            from_group=1,
            attachments=f'photo{owner_id}_{media_id}',
            access_token=vk_access_token,
            v=vk_api_version,
            message=author_comment
        )

    except requests.exceptions.HTTPError as http_error:
        print(f'Error -> {http_error}')
    finally:
        os.remove(comic_filename)


if __name__ == '__main__':
    main()
