from pixivpy3 import *
import asyncio

REFRESH_TOKEN = ''
USER_ID = ''

async def fetch_bookmarks(api, user_id, max_bookmark_id=None):
    total_count = 0
    next_qs = {'user_id': user_id, 'max_bookmark_id': max_bookmark_id}

    while next_qs:
        json_result = api.user_bookmarks_illust(**next_qs)
        total_count += len(json_result.illusts)
        next_qs = api.parse_qs(json_result.next_url)

    return total_count

async def main():
    api = AppPixivAPI()
    api.auth(refresh_token=REFRESH_TOKEN)

    total_count = await fetch_bookmarks(api, USER_ID)
    print(total_count)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"An error occurred within pixiv.py: {e}")
