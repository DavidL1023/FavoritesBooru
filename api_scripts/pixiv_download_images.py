# Purpose of this is to be able to change referer on http request of an image, pixiv for example has CORS enabled on their image server, so we have to download them
# locally bypassing it with header manipulation instead of spoofing which is too hard for the general user and im not making a proxy.. sorry!!!

import os
import requests
import multiprocessing

# Get the number of CPU cores
num_cores = os.cpu_count()

# Determine the number of cores to use based on conditions
if num_cores >= 16:
    use_cores = 12
elif num_cores >= 8:
    use_cores = 4
else:
    use_cores = 2

def download_file(save_path, url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Referer': 'https://www.pixiv.net/en'
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {url} to {save_path}")
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

def download_parallel(download_queue, num_processes=use_cores):
    pool = multiprocessing.Pool(processes=num_processes)
    pool.starmap(download_file, download_queue)
    pool.close()
    pool.join()
