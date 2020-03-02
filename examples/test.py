# from google python client
from googleapiclient.discovery import build
# key from console.developers.google.com project
api_key = ""
youtube = build('youtube', 'v3', developerKey=api_key)
print(type(youtube))
req = youtube.search().list(q='B-tree', part='snippet',
                            type='video', maxResults=10)

res = req.execute()
print('youtube.com/watch?v=' + res['items'][20]['id']['videoId'])
