import os
import json
from pixivpy3 import *
import asyncio
import platform
import pixiv_download_images

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load constants from the JSON file
with open('user_config.json', 'r') as config_file:
    constants = json.load(config_file)
    
REFRESH_TOKEN = constants["PIXIV_REFRESH_TOKEN"]
USER_ID = constants["PIXIV_USER_ID"]
BASE_URL = 'https://www.pixiv.net/en'
LOCAL_IMAGE_DIRECTORY = os.path.join('api_local_output', "pixiv")
JSON_DIRECTORY = "api_json_output"

# Ensure local directory is created
os.makedirs(LOCAL_IMAGE_DIRECTORY, exist_ok=True)

api = AppPixivAPI()
api.auth(refresh_token=REFRESH_TOKEN)

async def fetch_bookmarks():
    next_qs = {'user_id': USER_ID, 'max_bookmark_id': None}

    bookmarks_lists = []
    while next_qs:
        json_result = api.user_bookmarks_illust(**next_qs)
        results = json_result.illusts
        next_qs = api.parse_qs(json_result.next_url) # the api uses pagination, so it can't truly be async :/
        bookmarks_lists.append(results)

    return bookmarks_lists

async def main():
    # Early exit if required constants not provided
    if not REFRESH_TOKEN or not USER_ID:
        output_data = {
            "images": [],
            "tag_set": []
        }
        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "pixiv_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        return

    # Main
    bookmarks_lists = await fetch_bookmarks()
    
    # Use the returned api data
    pixiv_images = []
    efficient_download_queue = []

    # Retreive already stored images
    cache = os.listdir(LOCAL_IMAGE_DIRECTORY)
    cache = set(cache) # O(1) lookup

    # Used to remove any images that are no longer in user bookmark list
    user_bookmark_validate = set()

    pixiv_tag_set = set()
    for bookmarks_list in bookmarks_lists:
        for image in bookmarks_list:
 
            id = image.get('id')
            tags = image.get('tags')
            tag_list = []

            for tag in tags:
                translated_name = tag.get('translated_name')
                if translated_name is not None:
                    translated_name = translated_name.replace(' ', '_')
                    tag_list.append(translated_name)
                    pixiv_tag_set.add(translated_name)

            image_type = image.get('type')
            is_animated = image_type == 'ugoira'
            image_urls = image.get('image_urls')
            preview_url = image_urls.get('square_medium')

            # Previews are only accessable from pixiv domain as referer, must locally download
            file_name = f"{id}.jpg"
            user_bookmark_validate.add(file_name)
            save_path = os.path.join(LOCAL_IMAGE_DIRECTORY, file_name)
            if file_name not in cache:
                efficient_download_queue.append( (save_path, preview_url) )

            pixiv_images.append(
                {
                    'imageboard': 'pixiv',
                    'site_redirect': f'{BASE_URL}/artworks/{id}',
                    'img_preview': save_path, # local image
                    'tags': tag_list,
                    'is_animated': is_animated
                }
            )

    # Download any images that arent stored that are in cache
    pixiv_download_images.download_parallel(efficient_download_queue)
    
    # Remove any images that are stored that are no longer in user bookmarks
    for filename in cache:
        if filename not in user_bookmark_validate:
            file_path = os.path.join(LOCAL_IMAGE_DIRECTORY, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Removed unbookmarked file: {file_path}")
            else:
                print(f"File to be removed not found: {file_path}")

    # Create a JSON structure
        output_data = {
            "images": pixiv_images,
            "tag_set": list(pixiv_tag_set)
        }

    # Folder path for the JSON output
    os.makedirs(JSON_DIRECTORY, exist_ok=True)

    # Write to json file
    output_file_path = os.path.join(JSON_DIRECTORY, "pixiv_images.json")
    with open(output_file_path, 'w') as json_file:
        json.dump(output_data, json_file, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
