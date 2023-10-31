import os
import json
import asyncio
import platform
import aiohttp
import requests
import math

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

USERNAME = ''
USER_ID = ''
API_KEY = ''
API_GET_LIMIT = 200
API_STARTING_PAGE = 1
BASE_URL = 'https://danbooru.donmai.us'
JSON_DIRECTORY = "api_json_output"

def user_fav_count():
    url = f'{BASE_URL}/users/{USER_ID}.json?login={USERNAME}&api_key={API_KEY}'
    response = requests.get(url)
    user_data = response.json()
    return user_data.get('favorite_count')

total_pages = math.ceil(user_fav_count() / API_GET_LIMIT)

async def get_favorites(session, url):
    async with session.get(url) as resp:
        post_data = await resp.json()
        return post_data

async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []
        for page in range(API_STARTING_PAGE, total_pages + API_STARTING_PAGE):
            url = f'{BASE_URL}/posts.json?limit={API_GET_LIMIT}&page={page}&tags=ordfav%3A{USERNAME}&login={USERNAME}&api_key={API_KEY}'
            tasks.append(asyncio.ensure_future(get_favorites(session, url)))

        favorites_lists = await asyncio.gather(*tasks)

        # Use the returned api data
        danbooru_images = []

        for favorites_list in favorites_lists:
            for image in favorites_list:

                id = image.get('id')
                tags = image.get('tag_string')
                tag_list = tags.split()
                is_animated = 'animated' in tag_list
                preview = image.get('preview_file_url')

                danbooru_images.append(
                    {
                        'imageboard': 'danbooru',
                        'site_redirect': f'{BASE_URL}/posts/{id}',
                        'img_preview': preview,
                        'tags': tag_list,
                        'is_animated': is_animated
                    }
                )

        # Folder path for the JSON output
        os.makedirs(JSON_DIRECTORY, exist_ok=True)

        # Write to json file
        output_file_path = os.path.join(JSON_DIRECTORY, "danbooru_images.json")
        with open(output_file_path, 'w') as json_file:
            json.dump(danbooru_images, json_file, indent=4)

if __name__ == "__main__":
    asyncio.run(main())
