import click
import json
from zipfile import ZipFile
import tempfile
import shutil
import os
import sys

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

file_name = "JsonAndVideos.zip"

# https://stackoverflow.com/questions/4653768/overwriting-file-in-ziparchive


def remove_from_zip(zipfname, *filenames):
    tempdir = tempfile.mkdtemp()
    try:
        tempname = os.path.join(tempdir, 'new.zip')
        with ZipFile(zipfname, 'r') as zipread:
            with ZipFile(tempname, 'w') as zipwrite:
                for item in zipread.infolist():
                    if item.filename not in filenames:
                        data = zipread.read(item.filename)
                        zipwrite.writestr(item, data)
        shutil.move(tempname, zipfname)
    finally:
        shutil.rmtree(tempdir)


@click.group()
@click.pass_context
def main(ctx):
    """
    Main Method that runs before a command runs
    """
    usernameinput = input('Enter your Youtube username: ')

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
            except json.JSONDecodeError:
                ctx.obj = {
                    'username': usernameinput,
                    'dict': {},
                    'cmd': sys.argv[1]
                }
        zip.close()


@click.pass_context
def updateJson(ctx):
    if ctx.obj['cmd'] == 'upload':
        uploadDetails = ctx.obj['dict'][ctx.obj['username']
                                        ]['upload']['uploadDetails']
        # getting video path that needs to be zipped

        if(len(uploadDetails) == 6):
            videoFileToAdd = uploadDetails[0]
        else:
            videoFileToAdd = uploadDetails[len(uploadDetails) - 1][0]
        print(os.path.basename(videoFileToAdd))

    # updating the queueJson adding video
    queueFile = open('queueDict.json', 'w')
    queueJson = json.dumps(ctx.obj['dict'])
    queueFile.write(queueJson)
    queueFile.close()
    remove_from_zip(file_name, 'queueDict.json')
    with ZipFile(file_name, 'a') as zip:
        zip.write('queueDict.json')
        if ctx.obj['cmd'] == 'upload':
            try:
                zip.write(os.path.basename(videoFileToAdd))
            except FileNotFoundError:
                print('Error: Couldnt Find File, video not zipped')
        zip.close()


def countList(x):
    count = 0
    for el in x:
        if isinstance(el, list):
            count += 1
    return count


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
    Queues a video the user wants uploaded.

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
                    'uploadDetails': [videopath, title, description,
                                      tags, category, privacystatus]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'upload': {
                'uploadDetails': [videopath, title, description,
                                  tags, category, privacystatus]
            }
        }
        print(ctx.obj['dict'])
    # first time upload but user entry exists
    elif not ctx.obj['dict'][ctx.obj['username']].get('upload'):
        ctx.obj['dict'][ctx.obj['username']]['upload'] = {
            'uploadDetails': [videopath, title, description,
                              tags, category, privacystatus]
        }
        print(ctx.obj['dict'])
    # updating user subscribe entry
    else:
        currentEntry = ctx.obj['dict'][ctx.obj['username']
                                       ]['upload']['uploadDetails']
        print('current entry is: ', currentEntry)
        # single entry
        if countList(currentEntry) == 1:
            ctx.obj['dict'][ctx.obj['username']
                            ]['upload']['uploadDetails'] = [currentEntry, [videopath, title, description, tags, category, privacystatus]]
            print(ctx.obj['dict'])
        # multiple entry
        else:
            ctx.obj['dict'][ctx.obj['username']
                            ]['upload']['uploadDetails'].append([videopath, title, description, tags, category, privacystatus])
            print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('channelName')
def subscribe(ctx, channelname):
    """
    Queues a channel a user wants to subscribe to. Stores in JSON as string of list of strings.

    channelname: Name of the channel the user wants to subscribe to.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'subscribe': {
                    'channelname': channelname
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'subscribe': {
                'channelname': channelname
            }
        }
        print(ctx.obj['dict'])
    # first time subscribing but user entry exists
    elif not ctx.obj['dict'][ctx.obj['username']].get('subscribe'):
        ctx.obj['dict'][ctx.obj['username']]['subscribe'] = {
            'channelname': channelname
        }
        print(ctx.obj['dict'])
    # updating user subscribe entry
    else:
        currentEntry = ctx.obj['dict'][ctx.obj['username']
                                       ]['subscribe']['channelname']
        print('current entry is: ', currentEntry)
        print(type(currentEntry))
        # single entry
        if isinstance(currentEntry, str):
            ctx.obj['dict'][ctx.obj['username']
                            ]['subscribe']['channelname'] = [currentEntry, channelname]
            print(ctx.obj['dict'])
        # multiple entry
        else:
            ctx.obj['dict'][ctx.obj['username']
                            ]['subscribe']['channelname'].append(channelname)
            print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('query')
@click.argument('resultnumber')
def search(ctx, query, resultnumber):
    """
    Queues what a user wants to search. Stores in JSON as a list or list of lists.

    query: What the user wants searched.

    resultnumber: Number of results the user would like.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'search': {
                    'query': [query, resultnumber]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'search': {
                'query': [query, resultnumber]
            }
        }
        print(ctx.obj['dict'])
    # first time searching but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('search'):
        ctx.obj['dict'][ctx.obj['username']]['search'] = {
            'query': [query, resultnumber]
        }
        print(ctx.obj['dict'])
    # updating user search entry
    else:
        currentquery = ctx.obj['dict'][ctx.obj['username']
                                       ]['search']['query']
        print('current entry is: ', currentquery)
        # single entry
        if not any(isinstance(el, list) for el in currentquery):
            ctx.obj['dict'][ctx.obj['username']
                            ]['search']['query'] = [currentquery, [query, resultnumber]]
            print(ctx.obj['dict'])
        # multiple entry
        else:
            ctx.obj['dict'][ctx.obj['username']
                            ]['search']['query'].append([query, resultnumber])
            print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('rating')
@click.argument('videoname')
@click.argument('channelname')
def rate(ctx, rating, videoname, channelname):
    """
    Queues what a user would rate a video. Stores in Json at list or list of lists.

    rating: if a user rates like, dislike, or neutral (unlike/dislike).

    videoname: name of the video.

    channelname: name of the channel.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'rate': {
                    'rating': [rating, videoname, channelname]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'rate': {
                'rating': [rating, videoname, channelname]
            }
        }
        print(ctx.obj['dict'])
    # first time rating but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('rate'):
        ctx.obj['dict'][ctx.obj['username']]['rate'] = {
            'rating': [rating, videoname, channelname]
        }
        print(ctx.obj['dict'])
    # updating user rate entry
    else:
        currentrating = ctx.obj['dict'][ctx.obj['username']
                                        ]['rate']['rating']
        print('current entry is: ', currentrating)
        # single entry
        if not any(isinstance(el, list) for el in currentrating):
            ctx.obj['dict'][ctx.obj['username']
                            ]['rate']['rating'] = [currentrating, [rating, videoname, channelname]]
            print(ctx.obj['dict'])
        # multiple entry
        else:
            ctx.obj['dict'][ctx.obj['username']
                            ]['rate']['rating'].append([rating, videoname, channelname])
            print(ctx.obj['dict'])
    updateJson()


@main.command()
@click.pass_context
@click.argument('videoname')
@click.argument('channelname')
@click.argument('commenttext')
def comment(ctx, videoname, channelname, commenttext):
    """
    Queues a comment a user would like to leave on a video.

    videoname: name of the video.

    channelname: name of the channel.

    commenttext: text of the comment the user would like to leave.
    """
    # empty dict file
    if not ctx.obj['dict']:
        ctx.obj['dict'] = {
            ctx.obj['username']: {
                'comment': {
                    'commententries': [videoname, channelname, commenttext]
                }
            }
        }
        print(ctx.obj['dict'])
    # first time user entry
    elif not ctx.obj['dict'].get(ctx.obj['username']):
        ctx.obj['dict'][ctx.obj['username']] = {
            'comment': {
                'commententries': [videoname, channelname, commenttext]
            }
        }
        print(ctx.obj['dict'])
    # first time commenting but other user entries exist
    elif not ctx.obj['dict'][ctx.obj['username']].get('comment'):
        ctx.obj['dict'][ctx.obj['username']]['comment'] = {
            'commententries': [videoname, channelname, commenttext]
        }
        print(ctx.obj['dict'])
    # updating user comment entry
    else:
        currentcomment = ctx.obj['dict'][ctx.obj['username']
                                         ]['comment']['commententries']
        print('current entry is: ', currentcomment)
        # single entry
        if not any(isinstance(el, list) for el in currentcomment):
            ctx.obj['dict'][ctx.obj['username']
                            ]['comment']['commententries'] = [currentcomment, [videoname, channelname, commenttext]]
            print(ctx.obj['dict'])
        # multiple entry
        else:
            ctx.obj['dict'][ctx.obj['username']
                            ]['comment']['commententries'].append([videoname, channelname, commenttext])
            print(ctx.obj['dict'])
    updateJson()


if __name__ == '__main__':
    main()
