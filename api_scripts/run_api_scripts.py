import threading
import asyncio
import platform
import time

if platform.system() == 'Windows':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Import async functions and modules here
import danbooru, aibooru, gelbooru, pixiv

def fetch_favorites_danbooru():
    asyncio.run(danbooru.main())

def fetch_favorites_aibooru():
    asyncio.run(aibooru.main())

def fetch_favorites_gelbooru():
    asyncio.run(gelbooru.main())

def fetch_favorites_pixiv():
    asyncio.run(pixiv.main())

def main():
    start_time = time.time()  # Record the start time

    # Create separate threads for each asynchronous function
    threads = [
        threading.Thread(target=fetch_favorites_danbooru),
        threading.Thread(target=fetch_favorites_aibooru),
        threading.Thread(target=fetch_favorites_gelbooru),
        threading.Thread(target=fetch_favorites_pixiv)
    ]

    # Start all the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    end_time = time.time()  # Record the end time
    execution_time = end_time - start_time  # Calculate execution time
    print(f"Execution time: {execution_time} seconds")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"An error occurred within run_api_scripts.py: {e}")
