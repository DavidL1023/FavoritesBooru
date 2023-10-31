# Purpose of this is to be able to change referer on http request of an image, pixiv for example has CORS enabled on their image server, so we have to download them
# locally bypassing it with header manipulation instead of spoofing which is too hard for the general user and im not making a proxy.. sorry!!!

import os
import requests

def download_image_with_custom_headers(image_url: str, image_name: str, referer: str, output_folder: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Referer': referer
    }

    # Send an HTTP GET request to the image URL
    response = requests.get(image_url, headers=headers)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Get the binary content of the image
        image_data = response.content

        # Folder path for output
        os.makedirs(output_folder, exist_ok=True)
        
        # Save image to path
        output_file_path = os.path.join(output_folder, image_name)
        with open(output_file_path, 'wb') as file:
            file.write(image_data)
            print('Successfully downloaded image to: ' + output_file_path)
            return output_file_path

    else:
        print('Failed to download the image. HTTP status code:', response.status_code)
