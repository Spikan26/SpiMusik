# Installation

### **Install VLC (x64)**

[VLC Media Player](https://www.videolan.org/vlc/)

### **Install Python**

[Python Website](https://www.python.org/downloads/)

You can check if Python is correctly installed by opening a command prompt (cmd in the search bar) and type : **`python --version`** or **`py --version`**

Once Python is installed, navigate to the SpiMusik directory using the command prompt.
You can type **`cd C:/<YOUR_DIRECTORY_PATH>/`**

Then, use the following command  :

```
pip install -r requirements.txt
```

# Config File
Create a file named **`config.py`** with the following inside:

```py
PLAYLIST_URL = "<YOUR_YOUTUBE_PLAYLIST>"   # ex: https://www.youtube.com/playlist?list=...

TWITCH_CLIENT_ID = "<YOUR_CLIENT_ID>"
TWITCH_AUTH_TOKEN = "<YOUR_OAUTH_TOKEN>"


BROADCASTER_USER_NAME = "<YOUR_TWITCH_USERNAME>"   # ex: spikan

MUSIC_REWARD_NAME = "<YOUR_CHANNEL_REWARD_NAME>"   # ex: SpiMusik
```

- **`[WTF is TWITCH_CLIENT_ID] ?`**

You can get it by creating an application with this link [dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps). This is the client_id of your application.

In the "Redirect url" section, add the following URL : 

```
https://twitchapps.com/tokengen/
```

- **`[WTF is TWITCH_AUTH_TOKEN] ?`**

To get your OAuth Token, you must go to this link by replacing <CLIENT_ID> with your TWITCH_CLIENT_ID :

```
https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=<CLIENT_ID>&redirect_uri=https://twitchapps.com/tokengen/&scope=channel%3Aread%3Aredemptions+channel%3Amanage%3Aredemptions+chat%3Aread+chat%3Aedit+moderation%3Aread
```

# How To Use ?

Simply launch **`SpiMusik.py`**. A console command wil open before the application. This console contain all the log for the application, including error, information about the song and who requested it, new song added, etc..

To update the program, launch **`SpiUpdate.py`**

# Twitch chat command

Once connected, you can use command inside the twitch chat by taping **`!spimusik`** with the wanted command

|Who can use it ?|Command|Description|
|--|--|--|
|![Everyone](https://img.shields.io/badge/-Everyone-brightgreen)|**`help`**|Show all available commands. You can have more details by using **`!spimusik help [command]`**|
|![Everyone](https://img.shields.io/badge/-Everyone-brightgreen)|**`url`**|Show the title and URL of the playing song|
|![Everyone](https://img.shields.io/badge/-Everyone-brightgreen)|**`check`**|Show how many song are in the queue, and how many songs remains before the user's next request. You can use **`!spimusik check [index]`** to check a song in the queue at a specific position (ex: !spimusik check 2)|
|![Moderator](https://img.shields.io/badge/-Moderator-blue)|**`add`**|Add a song to the queue. (ex: **`!spimusik add www.youtube.com/watch?v=...`** )|
|![Moderator](https://img.shields.io/badge/-Moderator-blue)|**`remove`**|Remove the song at the corresponding index. You can use **Check + [index]** command before to get the song (ex: **`!spimusik remove 2`** )|
|![Moderator](https://img.shields.io/badge/-Moderator-blue)|**`next`** / **`skip`**|Skip the current song.|