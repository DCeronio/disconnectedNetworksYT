# disconnectedNetworksYT
cs 180h senior project

This is one sentence on one line.
This is another sentence on another line.

# Project Explanation

The project is setup as a server and client. The client queues the actions the user would
like to take in a zipped JSON file along with the .mp3's of videos they would also like to upload.
The server will read the JSON full of actions and service each action. It will return confirmations 
and other needed data to the client to be displayed to the user.

## google project setup
Since the project uses the youtube data api we will need a api key. This is retrieved through
**console.developers.google.com** where you create a project. 

After you have to say what API the project will use, in this case search for the youtube data API and
enable it.

Then in your project on hte APIs and Services Youtube Data API page that you should be brought to click on
credentials in the side tab. There at the top of the page you can click create credentials and API Key.

An API Key is generated and this can be used in the server program where youtube data api functions are called.

For using function's like rating a video or commenting a Client Secret file is needed due to the function acting 
on the behalf of a user. 

On the credentials tab click create credentials and OAuth client ID. You can give it a name and then download it as
a JSON and use the file as clien_secret_file. 

These request user consent so that the app can access the users data, this is down through the terminal when using the 
program. It will take the user to a google login where they can give consent to the program acting on their behalf. 

## Client
The cmdp.py file is the commandline prompt that will act as a simple commandline client. The 
user can type
```
python cmdp.py --help
```
for options. The basic functions is that the client will queue an action for the user. The
Youtube username is taken at the begginning of the program and the actions include:
```
  comment    Queues a comment a user would like to leave on a video.
  rate       Queues what a user would rate a video.              
  search     Queues what a user wants to search.
  subscribe  Queues a channel a user wants to subscribe to.
  upload     Queues a video the user wants uploaded
```

An example of a JSON file would be:
```
{
	‘Dylan’:
	{
		rate:
		{
			 rating: ‘like’
			videoname: ‘intro to python part one’
			channelname: ‘#1pythonchannel’
		}
		comment: 
		{
			videoname: ‘intro to python part one’
			channelname: ‘#1pythonchannel’
			commenttext: ‘This is a good video’
		}

		etc..
	}
	
	**another user here**
}

```
The file uses the **click api** to help with the command line interface. That can be found
here: **https://click.palletsprojects.com/en/7.x/** In the file the click ctx functionality
is used to pass the JSON file as a dictionary between the functions. 


