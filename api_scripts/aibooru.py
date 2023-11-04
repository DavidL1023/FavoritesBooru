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

USERNAME = constants["AIBOORU_USERNAME"]
USER_ID = constants["AIBOORU_USER_ID"]
API_KEY = constants["AIBOORU_API_KEY"]
API_GET_LIMIT = 200
API_STARTING_PAGE = 1
BASE_URL = 'https://aibooru.online'
JSON_DIRECTORY = "api_json_output"

def user_fav_count():
    url = f'{BASE_URL}/users/{USER_ID}.json?login={USERNAME}&api_key={API_KEY}'
    response = requests.get(url)
    user_data = response.json()
    return user_data.get('favorite_count')

if USERNAME and USER_ID and API_KEY:
    total_pages = math.ceil(user_fav_count() / API_GET_LIMIT)

async def get_favorites(session, url):
    async with session.get(url) as resp:
        post_data = await resp.json()
        return post_data

async def main():
    # Early exit if required constants not provided
    if not USERNAME or not USER_ID or not API_KEY:
        output_data = {
            "images": [],
            "tag_set": []
        }
        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "aibooru_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)
        return

    # Main
    async with aiohttp.ClientSession() as session:

        tasks = []
        for page in range(API_STARTING_PAGE, total_pages + API_STARTING_PAGE):
            url = f'{BASE_URL}/posts.json?limit={API_GET_LIMIT}&page={page}&tags=ordfav%3A{USERNAME}&login={USERNAME}&api_key={API_KEY}'
            tasks.append(asyncio.ensure_future(get_favorites(session, url)))

        favorites_lists = await asyncio.gather(*tasks)
        
        # Use the returned api data
        aibooru_images = []
        aibooru_tag_set = set()
        for favorites_list in favorites_lists:
            for image in favorites_list:

                id = image.get('id')
                tags = image.get('tag_string')
                tag_list = tags.split()
                for tag in tag_list:
                    aibooru_tag_set.add(tag)
                is_animated = 'animated' in tag_list
                preview = image.get('preview_file_url')

                aibooru_images.append(
                    {
                        'imageboard': 'aibooru',
                        'site_redirect': f'{BASE_URL}/posts/{id}',
                        'img_preview': preview,
                        'tags': tag_list,
                        'is_animated': is_animated
                    }
                )

        # Create a JSON structure
        output_data = {
            "images": aibooru_images,
            "tag_set": list(aibooru_tag_set)
        }

        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "aibooru_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)


if __name__ == "__main__":
    asyncio.run(main())
