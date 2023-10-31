import os
import json
from pixivpy3 import *
import asyncio
import platform
import retrieve_image
import shutil

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

REFRESH_TOKEN = ''
USER_ID = ''
BASE_URL = 'https://www.pixiv.net/en'
LOCAL_IMAGE_DIRECTORY = os.path.join('api_local_output', "pixiv")
JSON_DIRECTORY = "api_json_output"

api = AppPixivAPI()
api.auth(refresh_token=REFRESH_TOKEN)

async def fetch_bookmarks():
    next_qs = {'user_id': USER_ID, 'max_bookmark_id': None}

    bookmarks_lists = []
    while next_qs:
        json_result = api.user_bookmarks_illust(**next_qs)
        results = json_result.illusts
        next_qs = api.parse_qs(json_result.next_url)
        bookmarks_lists.append(results)

    return bookmarks_lists

async def main():
    # Delete the local folder before restarting
    try:
        shutil.rmtree(LOCAL_IMAGE_DIRECTORY)
    except FileNotFoundError:
        pass  # Ignore if the folder doesn't exist

    bookmarks_lists = await fetch_bookmarks()
    
    # Use the returned api data
    pixiv_images = []
    c = 0
    for bookmarks_list in bookmarks_lists:
        for image in bookmarks_list:
 
            id = image.get('id')
            tags = image.get('tags')
            tag_list = []

            for tag in tags:
                translated_name = tag.get('translated_name')
                if translated_name is None:
                    name = tag.get('name')
                    tag_list.append(name)
                else:
                    tag_list.append(translated_name)

            type = image.get('type')
            is_animated = type == 'ugoira'
            image_urls = image.get('image_urls')
            preview = image_urls.get('square_medium')

            # Previews are only accessable from pixiv domain as referer, must locally download
            local_image_name_asc = str(c) + '.jpg'
            preview = retrieve_image.download_image_with_custom_headers(preview, local_image_name_asc, BASE_URL, LOCAL_IMAGE_DIRECTORY)
            c += 1

            pixiv_images.append(
                {
                    'imageboard': 'pixiv',
                    'site_redirect': f'{BASE_URL}/artworks/{id}',
                    'img_preview': preview,
                    'tags': tag_list,
                    'is_animated': is_animated
                }
            )

        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "pixiv_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(pixiv_images, json_file, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
