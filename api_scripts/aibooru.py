from pybooru import Danbooru

USERNAME = ''

aibooruClient = Danbooru(site_url='https://aibooru.online/')

# Retrieve all favorites
page = 1 #starts at 1
results_len = -1
total = 0
while results_len != 0:
    results = aibooruClient.post_list(tags="ordfav:" + USERNAME, page=page)
    results_len = len(results)
    total += results_len
    page += 1

# Do something with results
print(total)