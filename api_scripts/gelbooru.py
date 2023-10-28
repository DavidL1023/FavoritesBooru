import asyncio
import aiohttp
import requests
import math 

USER_ID = ''
API_GET_LIMIT = 100
API_STARTING_PAGE = 0
BASE_URL = 'https://gelbooru.com'

def user_fav_count():
    url = f'{BASE_URL}/index.php?page=dapi&s=post&q=index&tags=fav%3a{USER_ID}&json=1'
    response = requests.get(url)
    user_data = response.json()
    att = user_data.get('@attributes')
    return att.get('count')

total_pages = math.ceil(user_fav_count() / API_GET_LIMIT)

async def get_favorites(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        post_data = data.get('post')
        return len(post_data)

async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []
        for page in range(API_STARTING_PAGE, total_pages + API_STARTING_PAGE):
            url = f'{BASE_URL}/index.php?page=dapi&s=post&q=index&limit={API_GET_LIMIT}&pid={page}&tags=fav%3a{USER_ID}&json=1'
            tasks.append(asyncio.ensure_future(get_favorites(session, url)))

        len_list = await asyncio.gather(*tasks)
        total = 0
        for len in len_list:
            total += len

        print("Gelbooru: " + str(total) + " results")

if __name__ == "__main__":
    asyncio.run(main())
