from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from pytube import YouTube
from zipfile import ZipFile
import json
from googleapiclient.http import MediaFileUpload
import urllib
import os

client_zip = 'JsonAndVideosCLIENT.zip'
server_zip = 'SERVERreply.zip'
CLIENT_SECRET_FILE = 'client_secret_file.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()


def windowsAdjust(fix):
    remove = '<>:"/\|?*'
    for letter in remove:
        fix = fix.replace(letter, '')
    return fix


def comment(youtube, videoid, channelid, commenttext):
    """
    Comments on a video
    """
    body = {
        "snippet": {
            "channelId": channelid,
            "videoId": videoid,
            "topLevelComment": {
                "snippet": {
                    "textOriginal": commenttext
                }
            }
        }
    }
    youtube.commentThreads().insert(part='snippet', body=body).execute()


def rate(youtube, rating, videoid):
    """
    Rates a video.
    """
    youtube.videos().rate(rating=rating,
                          id=videoid).execute()


def search(youtube, q, resultNumber):
    """
    Does a Youtube Search and returns a list of dictionaries of info{title, description, videoid, jpgURL} for each video.
    """
    req = req = youtube.search().list(q=q, part='snippet',
                                      type='video', maxResults=resultNumber)
    res = req.execute()
    searchList = []
    for entry in res['items']:
        searchList.append({'title': entry['snippet']['title'], 'description': entry['snippet']
                           ['description'], 'videoid': entry['id']['videoId'], 'channelId': entry['snippet']['channelId'], 'thumbnailUrl': entry['snippet']['thumbnails']['high']['url']})
    return searchList


def subscribe(youtube, channelid):
    youtube.subscriptions().insert(
        part="snippet",
        body={
            "snippet": {
                "resourceId": {
                    "kind": "youtube#channel",
                    "channelId": channelid
                }
            }
        }
    ).execute()


def upload(youtube, title, description, tags, category, privacyStatus, basename):
    request = youtube.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": category,
                "description": description,
                "title": title
            },
            "status": {
                "privacyStatus": privacyStatus
            }
        },
        media_body=MediaFileUpload(basename)
    )
    response = request.execute()


def main():
    # setup
    api_key = os.environ.get('YTAPIKEY')
    searchyoutube = build('youtube', 'v3', developerKey=api_key)
    behalfyoutube = build('youtube', 'v3', credentials=credentials)
    with ZipFile(client_zip, 'r') as zip:
        with zip.open('queueDict.json', 'r') as f:
            ftext = f.read()
            queueDict = json.loads(ftext)
        f.close
        zip.close()
    responseDict = {}

    # servicing requests
    for user in queueDict.keys():
        print('servicing:', user)
        responseDict[user] = {}
        for entry in queueDict[user]:

            if entry == 'comment':
                usercomments = queueDict[user][entry]['commententries']
                responseDict[user][entry] = {}
                responseDict[user][entry]['success'] = []
                responseDict[user][entry]['failure'] = []
                for el in usercomments:
                    try:
                        comment(behalfyoutube, el[0], el[1], el[2])
                        responseDict[user][entry]['success'].append(
                            [el[0], el[1], el[2]])
                    except Exception:
                        print('Couldn\'t rate video: ' + el[1])
                        responseDict[user][entry]['failure'].append(
                            [el[0], el[1], el[2]])
                        continue

            elif entry == 'rate':
                userRatings = queueDict[user][entry]['rating']
                responseDict[user][entry] = {}
                responseDict[user][entry]['success'] = []
                responseDict[user][entry]['failure'] = []
                for el in userRatings:
                    try:
                        rate(behalfyoutube, el[0], el[1])
                        responseDict[user][entry]['success'].append(
                            [el[0], el[1]])
                    except Exception:
                        print('Couldn\'t rate video: ' + el[1])
                        responseDict[user][entry]['failure'].append(
                            [el[0], el[1]])
                        continue

            elif entry == 'search':
                userQueries = queueDict[user][entry]['query']
                queryResponse = []
                for el in userQueries:
                    queryResponse.append(search(searchyoutube, el[0], el[1]))
                responseDict[user][entry] = queryResponse
                for query in queryResponse:
                    for iq in query:
                        if not os.path.exists('youtube/' + user + '/thumbnails/'):
                            os.makedirs('youtube/' + user + '/thumbnails/')
                        ret = urllib.request.urlretrieve(
                            iq['thumbnailUrl'], 'youtube/' + user + '/thumbnails/' + windowsAdjust(iq['title']) + '.jpg')

            elif entry == 'subscribe':
                userSubscriptions = queueDict[user][entry]['channelname']
                responseDict[user][entry] = {}
                responseDict[user][entry]['success'] = []
                responseDict[user][entry]['failure'] = []
                for el in userSubscriptions:
                    try:
                        subscribe(behalfyoutube, el)
                        responseDict[user][entry]['success'].append(
                            el)
                    except Exception:
                        print('Couldn\'t subscribe video: ' + el)
                        responseDict[user][entry]['failure'].append(
                            el)
                        continue

            elif entry == 'upload':
                userVideos = queueDict[user][entry]['uploadDetails']
                responseDict[user][entry] = {}
                responseDict[user][entry]['success'] = []
                responseDict[user][entry]['failure'] = []
                for el in userVideos:
                    try:
                        with ZipFile(client_zip, 'r') as czip:
                            czip.extract('youtube/videos/' +
                                         os.path.basename(el[0]))
                            czip.close()
                        current = os.getcwd()
                        os.chdir('youtub/videos/')
                        upload(behalfyoutube, el[1], el[2],
                               el[3], el[4], el[5], el[1])
                        os.chdir(current)
                        responseDict[user][entry]['success'].append(
                            [el[0], el[1]])
                    except Exception:
                        print('Couldn\'t rate video: ' + el[1])
                        responseDict[user][entry]['failure'].append(
                            [el[0], el[1]])
                        continue

            else:
                print('ERROR: Unrecognized cmd ', entry)
                pass

    # saving dictionary outside of zip for viewing/debugging
    replyFile = open('replyDict.json', 'w')
    replyJson = json.dumps(responseDict)
    replyFile.write(replyJson)
    replyFile.close()

    # zip youtube folder with jpgs and replyDict.json
    with ZipFile(server_zip, 'w') as szip:
        for folderName, subfolders, filenames in os.walk('youtube'):
            if folderName == 'youtube\\videos':
                continue
            for filename in filenames:
                filePath = os.path.join(folderName, filename)
                szip.write(filePath)
        szip.write('replyDict.json')
        szip.close()


if __name__ == '__main__':
    main()
