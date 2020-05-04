from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pytube import YouTube
from zipfile import ZipFile
import json


client_zip = 'JsonAndVideosCLIENT.zip'
server_zip = 'SERVERreply.zip'

# comment

# rate

# search


def search(youtube, q, resultNumber):
    """
    Does a Youtube Search and returns a list with a dictionary of info{title, description, videoid} for each video.
    """
    req = req = youtube.search().list(q=q, part='snippet',
                                      type='video', maxResults=resultNumber)
    res = req.execute()
    searchList = []
    for entry in res['items']:
        searchList.append({'title': entry['snippet']['title'], 'description': entry['snippet']
                           ['description'], 'videoid': entry['id']['videoId']})
    print(searchList)
    return searchList
# subscribe

# upload


def main():
    api_key = open('youtubeAPIKey.txt', 'r').read()
    youtube = build('youtube', 'v3', developerKey=api_key)
    with ZipFile(client_zip, 'r') as zip:
        zip.printdir()
        with zip.open('queueDict.json', 'r') as f:
            ftext = f.read()
            queueDict = json.loads(ftext)
        f.close
        zip.close()
    for user in queueDict.keys():
        print('servicing:', user)
        for entry in queueDict[user]:
            if entry == 'comment':
                pass
            elif entry == 'rate':
                pass
            elif entry == 'search':
                search(youtube, )
            elif entry == 'subsribe':
                pass
            elif entry == 'upload':
                pass
            else:
                print('ERROR: Unrecognized cmd ', entry)
                pass


if __name__ == '__main__':
    main()
