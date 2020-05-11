# disconnectedNetworksYT
cs 180h senior project

# Project Explanation

The project is setup as a server and client. 
The client queues the actions the user would like to take in a zipped JSON file along with the .mp3's of videos they would also like to upload.
The server will read the JSON full of actions and service each action. 
It will return confirmations and other needed data.


Diagrams:

## google project setup
Since the project uses the youtube data api we will need a api key. 
This is retrieved through [Google Dev Website](console.developers.google.com) where you can create a project. 
After, you have to say what API the project will use. 
In this case search for the youtube data API and enable it.

Then in your project on the APIs and Services Youtube Data API page click on credentials in the side tab. 
There at the top of the page you can click create credentials and API Key.
An API Key is generated and this can be used in the server program where you build a youtube object.

For using function's like rating a video or commenting a Client Secret file is needed due to the function acting on the behalf of a user. 
On the credentials tab click create credentials and OAuth client ID. 
You can give it a name and then download it as a JSON. 
These types of functions will request user consent, this is down through the terminal when using the program. 
It will take the user to a google OAuth where they can allow the program to make changes and access to their information.
A string will then be generated that can be pasted in the terminal and the program will continue. 

## Client
The cmdp.py file in the clientcommandline folder is a commandline interface that will act as a client.
The User will type individual commands and provide arguments that satisfy that specific command.
The client will then record the command and arguments for the user in **queueDict.json**

The user can type `python cmdp.py --help` for options.
 
The Youtube username is taken at the begginning of the program so that actions for multiple users can be recorded.

Actions that can be taken:
```
  comment    Queues a comment a user would like to leave on a video.
  download   Uses PyTube to download a given videoid.
  rate       Queues what a user would rate a video.
  search     Queues what a user wants to search.
  subscribe  Queues a channel a user wants to subscribe to.
  upload     Queues a video the user wants uploaded, stores as list of...

**Comment**

Usage: cmdp.py comment [OPTIONS] VIDEOID CHANNELID COMMENTTEXT

  Queues a comment a user would like to leave on a video. Stores in JSON as
  List of Lists

  videoid: id of the video.

  channelid: id of the channel.

  commenttext: text of the comment the user would like to leave.

**Download**

Usage: cmdp.py download [OPTIONS] VIDEOID OUTPUTPATH

  Uses PyTube to download a given videoid.

  videoid: id of a youtube vidoe obtained from serverReply.zip search
  section

  outputpath: Where you would like the video to be saved to

**Rate**

Usage: cmdp.py rate [OPTIONS] RATING VIDEOID

  Queues what a user would rate a video. Stores in Json as list of lists.

  rating: if a user rates like, dislike, or neutral (unlike/dislike).

  videoid: id of the video you want to rate, found in SERVERreply for search

**Search**

Usage: cmdp.py search [OPTIONS] QUERY RESULTNUMBER

  Queues what a user wants to search. Stores in JSON as a list of lists.

  query: What the user wants searched.

  resultnumber: Number of results the user would like.

**Subscribe**

Usage: cmdp.py subscribe [OPTIONS] CHANNELID

  Queues a channel a user wants to subscribe to. Stores in JSON as list of
  strings.

  channelname: Name of the channel the user wants to subscribe to.

**Upload**

Usage: cmdp.py upload [OPTIONS] VIDEOPATH TITLE DESCRIPTION TAGS CATEGORY
                      PRIVACYSTATUS

  Queues a video the user wants uploaded, stores as list of lists.

  file: File path to the video to upload

  title: Title of the video.

  description: Description for the video.

  tags: Python List of words associated with the video when searched.

  category: The category ID for the YouTube video category associated with
  the video.

  privacystatus: The privacy status of the video, 'private', 'public',
  'unlisted'.
```
Download is the only function that does not get recorded in queueDict.json as no data is being passed to the server.

An example of a filled out queueDict.json would look like:
```
{
    "firstUser": {
        "upload": {
            "uploadDetails": [
                [
                    "E:\\SJSU\\Spring2020\\cs180h\\raspPiVideo.mp4",
                    "title",
                    "description",
                    [
                        "tag1",
                        "tag2"
                    ],
                    "22",
                    "private"
                ]
            ]
        },
        "comment": {
            "commententries": [
                [
                    "123",
                    "456",
                    "comment text"
                ]
            ]
        },
        "rate": {
            "rating": [
                [
                    "like",
                    "videoid"
                ]
            ]
        },
        "search": {
            "query": [
                [
                    "search text",
                    "5"
                ]
            ]
        },
        "subscribe": {
            "channelname": [
                "channelid"
            ]
        }
    },
    "SecondUser": {
        "subscribe": {
            "channelname": [
                "channelid"
            ]
        }
    }
}

```
The file uses the [click api](https://click.palletsprojects.com/en/7.x/)to help with the command line interface. 
The main function is a click group and each function that is ment to be called on the command line is a click command of the main click group. 
This provides the easy help functionality and each function can be called directly from thte command line.

There is a listParamType that I created for click since the search command requires a list of tags.
With this custom type you can enter `'[tag1,tag2]` into the command line and it will be accepted and parsed correctly.

There is a ctx parameter that is also passed around.
This is built into click and acts as a dictionary of what username, the queue dictionary, and current cmd to each function.
If a function uses the ctx parameter it has a pass_context click decorator on it as well.

Going through the program it starts in main.
Here the JsonAndVideos.zip is opened and the queueDict.json is read.
If the queueDict.json file is empty a empty dictionary will be used
If either the or the json don't exist a zip will be created with a empty dictionary.

Next the corresponding command that was typed will be executed.
Most of the functions are the same in structure.
If there is a empty dictionary an entry for the user will be created with the command and arguments recorded.
If there is a dictionary but no user entry, the user and comamand and arguments will be recorded.
if there is a dictionary, user but not the specific command section, that section will be recorded with the needed arguments.
Finally if the dictionary, user, and command section exist the entry will be updated.
All the entries are lists of lists, so the new one can just be appended. 

At the end of each function there is a call to the updateJson function.
This function updates the JSON file and makes the JsonAndVideos.zip.
First it will open the queueDict.json file and write the updated dictionary.
This is done using the JSON library, dumps() will make a python dictionary a JSON string, and loads() will make a JSON string a python dictionary.
It is also used in the main function.
Then the youtube/videos folder in the zip will be extracted to the current directory into the oldVideos folder.
This is done for debugging and for the next step.
That being the zip file will be recreated.
Each video that needs to be uploaded will be found and zipped.
This is done using Shutil.copyfileobj().
The function takes a file descriptor for a video and a file descriptor for a location in the zip.
The video will then be copied over to the zip file.
If the video cannot be found again, the program will use the video in the oldVideos folder.



 


