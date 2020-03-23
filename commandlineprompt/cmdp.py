import click
import json


@click.group()
@click.pass_context
def main(ctx):
    """
    Main Method that runs before a command runs
    """
    usernameinput = input('Enter your Youtube username: ')
    f = open('queueDict.txt', 'r')
    ftext = f.read()
    f.close()
    queueDict = json.loads(ftext)
    print(queueDict)
    ctx.obj = {
        'username': usernameinput,
        'dict': queueDict
    }


@click.pass_context
def updateJson(ctx):
    f = open('queueDict.txt', 'w')
    queueJson = json.dumps(ctx.obj['dict'])
    f.write(queueJson)
    f.close()


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
