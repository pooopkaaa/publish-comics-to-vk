import json

import requests


def get_response(url):
    response = requests.get(url)
    response.raise_for_status()
    return response


def download_comics_to_file(filename, comic_json):
    with open(filename, 'w') as file:
        json.dump(comic_json, file, indent=4)


def download_comic_image(filename, url):
    response = get_response(url)
    with open(filename, 'wb') as file:
        file.write(response.content)


def main():
    url = 'https://xkcd.com/353/info.0.json'
    response = get_response(url)

    comic_json = response.json()

    comic_name = comic_json['safe_title']
    comic_filename = comic_name + '.json'
    comic_image_filename = comic_name + '.png'
    comic_image_url = comic_json['img']
    author_comment = comic_json['alt']
    print(author_comment)
    
    download_comics_to_file(comic_filename, comic_json)
    download_comic_image(comic_image_filename, comic_image_url)


if __name__ == '__main__':
    main()