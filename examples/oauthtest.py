from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
CLIENT_SECRET_FILE = 'client_secret_file.json'
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
credentials = flow.run_console()
youtube = build('youtube', 'v3', credentials=credentials)


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
