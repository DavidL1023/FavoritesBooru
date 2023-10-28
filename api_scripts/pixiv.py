from pixivpy3 import *
import asyncio

# I sadly cannot find a public API for pixiv, I think the only possible methods are scrapers, so if its slowing
# down your website, there is not much I can do to optimize it

REFRESH_TOKEN = ''
USER_ID = ''

api = AppPixivAPI()
api.auth(refresh_token=REFRESH_TOKEN)

async def get_bookmarks():
    total = 0
    results_len = -1
    next_qs = {'user_id': USER_ID, 'max_bookmark_id': None}

    while next_qs:
        json_result = api.user_bookmarks_illust(**next_qs)
        results_len = len(json_result.illusts)
        total += results_len
        next_qs = api.parse_qs(json_result.next_url)

    return total

async def main():
    total = await get_bookmarks()
    print("Pixiv: " + str(total) + " results")

if __name__ == "__main__":
    asyncio.run(main())
