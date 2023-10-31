import threading
import asyncio
import time

# Import async functions and modules here
import danbooru, aibooru, gelbooru, pixiv

def fetch_favorites_danbooru():
    start_time = time.time()
    asyncio.run(danbooru.main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Danbooru Execution Time: {execution_time} seconds")

def fetch_favorites_aibooru():
    start_time = time.time()
    asyncio.run(aibooru.main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Aibooru Execution Time: {execution_time} seconds")

def fetch_favorites_gelbooru():
    start_time = time.time()
    asyncio.run(gelbooru.main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Gelbooru Execution Time: {execution_time} seconds")

def fetch_bookmarks_pixiv():
    start_time = time.time()
    asyncio.run(pixiv.main())
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Pixiv Execution Time: {execution_time} seconds")

def main():
    threads = [
        threading.Thread(target=fetch_favorites_danbooru),
        threading.Thread(target=fetch_favorites_aibooru),
        threading.Thread(target=fetch_favorites_gelbooru),
        threading.Thread(target=fetch_bookmarks_pixiv)
    ]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred within run_api_scripts.py: {e}")
