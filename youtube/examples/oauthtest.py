from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload
import os

CLIENT_SECRET_FILE = 'client_secret_file.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
#SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)

os.chdir('E:/SJSU/Spring2020/cs180h/')
request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "categoryId": "22",
            "description": "Description of uploaded video.",
            "title": "Test video upload."
        },
        "status": {
            "privacyStatus": "public"
        }
    },

    # TODO: For this request to work, you must replace "YOUR_FILE"
    #       with a pointer to the actual file you are uploading.
    media_body=MediaFileUpload('raspPiVideo.mp4')
)
response = request.execute()

"""
request = youtube.subscriptions().insert(
    part="snippet",
    body={
        "snippet": {
            "resourceId": {
                "kind": "youtube#channel",
                "channelId": "UCO6q_rhb1vl5GeE6Qr_M0FQ"
            }
        }
    }
)
response = request.execute()

print(response)
# liking/disliking a video
youtube.videos().rate(rating='like',
                      id='Nr-gYadj5dw').execute()

# commenting
request = youtube.commentThreads().insert(
    part="snippet",
    body={
        "snippet": {
            "channelId": "UCkUq-s6z57uJFUFBvZIVTyg",
            "videoId": "Nr-gYadj5dw",
            "topLevelComment": {
                "snippet": {
                    "textOriginal": "Commented With Code :D"
                }
            }
        }
    }
)
response = request.execute()
"""
