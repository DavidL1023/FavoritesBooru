import os
import json
import asyncio
import platform
import aiohttp
import requests
import math 

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Load constants from the JSON file
with open('user_config.json', 'r') as config_file:
    constants = json.load(config_file)

USER_ID = constants["GELBOORU_USER_ID"]
API_KEY = constants["GELBOORU_API_KEY"]
API_GET_LIMIT = 100
API_STARTING_PAGE = 0
BASE_URL = 'https://gelbooru.com'
JSON_DIRECTORY = "api_json_output"

def user_fav_count():
    url = f'{BASE_URL}/index.php?page=dapi&s=post&q=index&tags=fav%3a{USER_ID}&json=1&api_key={API_KEY}&user_id={USER_ID}'
    response = requests.get(url)
    user_data = response.json()
    att = user_data.get('@attributes')
    return att.get('count')

if USER_ID and API_KEY:
    total_pages = math.ceil(user_fav_count() / API_GET_LIMIT)

async def get_favorites(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        post_data = data.get('post')
        return post_data

async def main():
    # Early exit if required constants not provided
    if not USER_ID or not API_KEY:
        output_data = {
            "images": [],
            "tag_set": []
        }
        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "gelbooru_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        return

    # Main
    async with aiohttp.ClientSession() as session:

        tasks = []
        for page in range(API_STARTING_PAGE, total_pages + API_STARTING_PAGE):
            url = f'{BASE_URL}/index.php?page=dapi&s=post&q=index&limit={API_GET_LIMIT}&pid={page}&tags=fav%3a{USER_ID}&json=1&api_key={API_KEY}&user_id={USER_ID}'
            tasks.append(asyncio.ensure_future(get_favorites(session, url)))

        favorites_lists = await asyncio.gather(*tasks)

        # Use the returned api data
        gelbooru_images = []
        gelbooru_tag_set = set()
        for favorites_list in favorites_lists:
            for image in favorites_list:

                id = image.get('id')
                tags = image.get('tags')
                tag_list = tags.split()
                for tag in tag_list:
                    gelbooru_tag_set.add(tag)
                is_animated = 'animated' in tag_list
                preview = image.get('preview_url')

                gelbooru_images.append(
                    {
                        'imageboard': 'gelbooru',
                        'site_redirect': f'{BASE_URL}/index.php?page=post&s=view&id={id}',
                        'img_preview': preview,
                        'tags': tag_list,
                        'is_animated': is_animated
                    }
                )

        # Create a JSON structure
        output_data = {
            "images": gelbooru_images,
            "tag_set": list(gelbooru_tag_set)
        }

        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "gelbooru_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)

        

if __name__ == "__main__":
    asyncio.run(main())
