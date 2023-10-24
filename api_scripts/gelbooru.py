import asyncio
from pygelbooru import Gelbooru

USER_ID = ''

async def search_gelbooru():
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
    await search_gelbooru()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()  # Create a new event loop
    asyncio.set_event_loop(loop)  # Set it as the current event loop
    loop.run_until_complete(main())  # Run the main coroutine
