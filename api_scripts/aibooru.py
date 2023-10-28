import asyncio
import aiohttp
import requests
import math 

USERNAME = ''
USER_ID = ''
API_KEY = ''
API_GET_LIMIT = 200
API_STARTING_PAGE = 1
BASE_URL = 'https://aibooru.online'

def user_fav_count():
    url = f'{BASE_URL}/users/{USER_ID}.json?login={USERNAME}&api_key={API_KEY}'
    response = requests.get(url)
    user_data = response.json()
    return user_data.get('favorite_count')

total_pages = math.ceil(user_fav_count() / API_GET_LIMIT)

async def get_favorites(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        return len(data)

async def main():
    async with aiohttp.ClientSession() as session:

        tasks = []
        for page in range(API_STARTING_PAGE, total_pages+1):
            url = f'{BASE_URL}/posts.json?limit=200&page={page}&tags=ordfav%3A{USERNAME}'
            tasks.append(asyncio.ensure_future(get_favorites(session, url)))

        len_list = await asyncio.gather(*tasks)
        total = 0
        for len in len_list:
            total += len

        print("AIBooru: " + str(total) + " results")

if __name__ == "__main__":
    asyncio.run(main())
