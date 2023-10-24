import asyncio
from pybooru import Danbooru

USERNAME = ''

async def fetch_favorites():
    aibooruClient = Danbooru(site_url='https://aibooru.online/')
    
    page = 1  # starts at 1
    results_len = -1
    total = 0
    while results_len != 0:
        results = aibooruClient.post_list(tags="ordfav:" + USERNAME, page=page)
        results_len = len(results)
        total += results_len
        page += 1

    return total

async def main():
    total = await fetch_favorites()
    print(total)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred within aibooru.py: {e}")
