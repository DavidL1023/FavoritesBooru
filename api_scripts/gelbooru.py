import asyncio
from pygelbooru import Gelbooru

USER_ID = ''

async def fetch_favorites():
    gelbooru = Gelbooru()

    page = 0 #starts at 0
    results_len = -1
    total = 0
    while results_len != 0:
        results = await gelbooru.search_posts(tags=['fav:' + USER_ID], page=page)
        results_len = (len(results))
        total += results_len
        page += 1
    
    # Do something with the results
    print(total)

async def main():
    await fetch_favorites()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred within gelbooru.py: {e}")
