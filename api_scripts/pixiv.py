from pixivpy3 import *

REFRESH_TOKEN = ''
USER_ID = ''

# Initialize the API with your authentication token
api = AppPixivAPI()
api.auth(refresh_token=REFRESH_TOKEN)

# get all bookmarks
next_qs = {'user_id': USER_ID, 'max_bookmark_id': None}
x=0
while next_qs:
    json_result = api.user_bookmarks_illust(**next_qs)
    for illust in json_result.illusts:
        x+=1
    next_qs = api.parse_qs(json_result.next_url)
print(x)