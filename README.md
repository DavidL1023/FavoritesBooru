# Image Board
FavoritesBooru is a tool to display all of your favorites and bookmarks between Danbooru, Gelbooru, AIBooru, and Pixiv in one place. I was asked to make it and I thought the experience would be good I'm definitely not a gooning weeb.

# Dependencies 
[pixivpy3](https://github.com/upbit/pixivpy)

[aiohttp](https://pypi.org/project/aiohttp/)

[pixivOAuth](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362)

# How to
Enter your profile data into user_config.json in the root directory. API keys and user IDs can be found from the site's profile page. Note that the user ID is different than the username and should instead be a number.

Pixiv specifically requires a refresh token. Follow the guide [here](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362) to get a Pixiv refresh token for your account.

With Node.js and Python3 installed, run npm ci from the root directory to install dependencies, and then run server.mjs to start the server on port 3000.

First run of the retrieve images button will take longer than subsequent runs if using Pixiv. This is because images for that site need to be locally downloaded and cached.

Important: If you're using this for the first time, run the retrieve button twice in a row to ensure you aren't missing images (check console to make sure it's all good)

Side note: If you want to use the site from another device like a phone, you can run it on your computer or a raspberry pi or something, and then find the devices IP. While the server is running, type the device ip into your browser followed by the port which should be 3000. Example - 192.168.0.1:3000

https://github.com/DavidL1023/FavoritesBooru/assets/80372643/d1e9701b-6f43-4a76-bb04-4eeeaf8439c0
