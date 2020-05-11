# from google python client
from googleapiclient.discovery import build
# key from console.developers.google.com project

api_key = open('youtubeAPIKey.txt', 'r').read()

youtube = build('youtube', 'v3', developerKey=api_key)

req = youtube.search().list(q='B-tree', part='snippet',
                            type='video', maxResults=10)

res = req.execute()
print(res['items'])
for entry in res['items']:
    print(entry['snippet']['title'])
    print(entry['snippet']['description'])
    print(entry['id']['videoId'])
    print(entry['snippet']['thumbnails']['high']['url'])
    print('_________')

print('youtube.com/watch?v=' + res['items'][9]['id']['videoId'])
