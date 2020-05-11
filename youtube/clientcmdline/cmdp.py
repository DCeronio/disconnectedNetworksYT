import click
import json
from zipfile import ZipFile
import tempfile
import shutil
import os
import sys
from pytube import YouTube

"""
Type 'python cmdp.py --help' for options
"""


class listParamType(click.ParamType):
    """
    In upload have tags parameter that is a list of strings, need to convert from String to list.
    """
    name = "list"

    def convert(self, value, param, ctx):
        try:
            return value.strip('[]').split(',')
        except AttributeError:
            self.fail(
                "Expected a String for strip method "
                f"{value!r} of type {type(value).__name__}",
                param,
                ctx,
            )


LIST_TYPE = listParamType()

file_name = "JsonAndVideosCLIENT.zip"


@click.group()
@click.pass_context
def main(ctx):
    """
    Main Method that runs before a command runs
    """
    usernameinput = input('Enter your Youtube username: ')

    try:
        with ZipFile(file_name, 'r') as zip:
            zip.printdir()
            with zip.open('queueDict.json', 'r') as f:
                try:
                    ftext = f.read()
                    queueDict = json.loads(ftext)
                    ctx.obj = {
                        'username': usernameinput,
                        'dict': queueDict,
                        'cmd': sys.argv[1]
                    }
                    f.close()
                    zip.close()
                except json.JSONDecodeError:
                    print('Empty QueueDict file')
                    ctx.obj = {
                        'username': usernameinput,
                        'dict': {},
                        'cmd': sys.argv[1]
                    }
                    zip.close()
    except (FileNotFoundError, KeyError):
        print('Error: Couldn\'t find zip file or Json File, Recreating Zip with Empty Json')
        jfile = open('queueDict.json', 'w')
        with ZipFile(file_name, 'w') as zip:
            zip.write('queueDict.json')
            zip.close()
        jfile.close()
        ctx.obj = {
            'username': usernameinput,
            'dict': {},
            'cmd': sys.argv[1]
        }


@click.pass_context
def updateJson(ctx):
    # saving dictionary outside of zip for viewing/debugging
    queueFile = open('queueDict.json', 'w')
    queueJson = json.dumps(ctx.obj['dict'])
    queueFile.write(queueJson)
    queueFile.close()

    # save videos folder
    with ZipFile(file_name, 'r') as zipr:
        for file in zipr.namelist():
            if file.startswith('youtube/'):
                zipr.extract(file, 'oldVideos')
        zipr.close()
    # Recreate Zip File
    with ZipFile(file_name, 'w') as zipw:
        zipw.write('queueDict.json')
        # Refinding Videos in upload section on Dict
        for user in ctx.obj['dict'].keys():
            print(user)
            try:
                uploadList = ctx.obj['dict'][user]['upload']['uploadDetails']
                for entry in uploadList:
                    print('     ', entry[0])
                    try:
                        videoDescriptor = open(entry[0], 'rb')
                        zipLocation = zipw.open(
                            'youtube/videos/' + os.path.basename(entry[0]), mode='w')
                        shutil.copyfileobj(videoDescriptor, zipLocation)
                        zipLocation.close()
                        videoDescriptor.close()
                        print('         added video: ',
                              os.path.basename(entry[0]))
                    except FileNotFoundError:
                        if(os.path.exists('oldvideos/youtube/videos/' + os.path.basename(entry[0]))):
                            print('     Adding file from oldvideos')
                            videoDescriptor = open(
                                'oldvideos/youtube/videos/' + os.path.basename(entry[0]), 'rb')
                            zipLocation = zipw.open(
                                'youtube/videos/' + os.path.basename(entry[0]), mode='w')
                            shutil.copyfileobj(videoDescriptor, zipLocation)
                            zipLocation.close()
                            videoDescriptor.close()
                        else:
                            print('         Video Not Found: ',
                                  os.path.basename(entry[0]))
            except KeyError:
                print('     ' + user + ' no upload section')
            print('------------------')
        zipw.close()


@main.command()
@click.argument('videoid')
@click.argument('outputpath')
def download(videoid, outputpath):
    """
    Uses PyTube to download a given videoid.

    videoid: id of a youtube vidoe obtained from serverReply.zip search section

    outputpath: Where you would like the video to be saved to
    """
    urlString = 'http://youtube.com/watch?v=' + videoid
    yt = YouTube(urlString)
    yt.streams.filter(progressive=True, file_extension='mp4').order_by(
        'resolution')[-1].download(output_path=outputpath)
    print(yt.title + ' downlaoded to ' + outputpath)


@main.command()
@click.pass_context
@click.argument('videopath')
@click.argument('title')
@click.argument('description')
@click.argument('tags', type=LIST_TYPE)
@click.argument('category')
@click.argument('privacystatus')
def upload(ctx, videopath, title, description, tags, category, privacystatus):
    """
    Queues a video the user wants uploaded, stores as list of lists.

    file: File path to the video to upload

    title: Title of the video.

    description: Description for the video.

    tags: Python List of words associated with the video when searched.

    category: The category ID for the YouTube video category associated with the video.

    privacystatus: The privacy status of the video, 'private', 'public', 'unlisted'.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'upload': {
                    'uploadDetails': [[videopath, title, description,
                                       tags, category, privacystatus]]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'upload': {
                'uploadDetails': [[videopath, title, description,
                                   tags, category, privacystatus]]
            }
        }
        print(ctx.obj['dict'])
    # first time upload but user entry exists
    elif not ctx.obj['dict'][ctx.obj['username']].get('upload'):
        ctx.obj['dict'][ctx.obj['username']]['upload'] = {
            'uploadDetails': [[videopath, title, description,
                               tags, category, privacystatus]]
        }
        print(ctx.obj['dict'])
    # updating user subscribe entry
    else:
        currentEntry = ctx.obj['dict'][ctx.obj['username']
                                       ]['upload']['uploadDetails']
        # multiple entry
        if [videopath, title, description, tags, category, privacystatus] not in currentEntry:
            ctx.obj['dict'][ctx.obj['username']
                            ]['upload']['uploadDetails'].append([videopath, title, description, tags, category, privacystatus])
        else:
            print('Entry Exists, not queueing')
    updateJson()


@main.command()
@click.pass_context
@click.argument('channelid')
def subscribe(ctx, channelid):
    """
    Queues a channel a user wants to subscribe to. Stores in JSON as list of strings.

    channelid: id of the channel the user wants to subscribe to.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'subscribe': {
                    'channelname': [channelid]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'subscribe': {
                'channelname': [channelid]
            }
        }
        print(ctx.obj['dict'])
    # first time subscribing but user entry exists
    elif not ctx.obj['dict'][ctx.obj['username']].get('subscribe'):
        ctx.obj['dict'][ctx.obj['username']]['subscribe'] = {
            'channelname': [channelid]
        }
        print(ctx.obj['dict'])
    # updating user subscribe entry
    else:
        ctx.obj['dict'][ctx.obj['username']
                        ]['subscribe']['channelname'].append(channelid)
        print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('query')
@click.argument('resultnumber')
def search(ctx, query, resultnumber):
    """
    Queues what a user wants to search. Stores in JSON as a list of lists.

    query: What the user wants searched.

    resultnumber: Number of results the user would like.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'search': {
                    'query': [[query, resultnumber]]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'search': {
                'query': [[query, resultnumber]]
            }
        }
        print(ctx.obj['dict'])
    # first time searching but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('search'):
        ctx.obj['dict'][ctx.obj['username']]['search'] = {
            'query': [[query, resultnumber]]
        }
        print(ctx.obj['dict'])
    # updating user search entry
    else:
        ctx.obj['dict'][ctx.obj['username']
                        ]['search']['query'].append([query, resultnumber])
        print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('rating')
@click.argument('videoid')
def rate(ctx, rating, videoid):
    """
    Queues what a user would rate a video. Stores in Json as list of lists.

    rating: if a user rates like, dislike, or neutral (unlike/dislike).

    videoid: id of the video you want to rate, found in SERVERreply for search
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'rate': {
                    'rating': [[rating, videoid]]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'rate': {
                'rating': [[rating, videoid]]
            }
        }
        print(ctx.obj['dict'])
    # first time rating but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('rate'):
        ctx.obj['dict'][ctx.obj['username']]['rate'] = {
            'rating': [[rating, videoid]]
        }
        print(ctx.obj['dict'])
    # updating user rate entry
    else:
        ctx.obj['dict'][ctx.obj['username']
                        ]['rate']['rating'].append([rating, videoid])
        print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('videoid')
@click.argument('channelid')
@click.argument('commenttext')
def comment(ctx, videoid, channelid, commenttext):
    """
    Queues a comment a user would like to leave on a video. Stores in JSON as List of Lists

    videoid: id of the video.

    channelid: id of the channel.

    commenttext: text of the comment the user would like to leave.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'comment': {
                    'commententries': [[videoid, channelid, commenttext]]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'comment': {
                'commententries': [[videoid, channelid, commenttext]]
            }
        }
        print(ctx.obj['dict'])
    # first time commenting but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('comment'):
        ctx.obj['dict'][ctx.obj['username']]['comment'] = {
            'commententries': [[videoid, channelid, commenttext]]
        }
        print(ctx.obj['dict'])
    # updating user comment entry
    else:
        ctx.obj['dict'][ctx.obj['username']
                        ]['comment']['commententries'].append([videoid, channelid, commenttext])
        print(ctx.obj['dict'])
    updateJson()


if __name__ == '__main__':
    main()
