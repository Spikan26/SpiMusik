(I'll make a guide later on how to install it, but for now, just ask me on discord)

**Install VLC (x64)**

**Install Python**

**Install at least the following**:
- `pip install websocket-client`
- `pip install yt_dlp`
- `pip install python-vlc`
- `pip install requests`


# Config File
Create a file named **`config.py`** with the following inside:

```py
PLAYLIST_URL = "<YOUR_YOUTUBE_PLAYLIST>"

TWITCH_CLIENT_ID = "<YOUR_CLIENT_ID>"
TWITCH_AUTH_TOKEN = "<YOUR_OAUTH_TOKEN>"


BROADCASTER_USER_NAME = "<YOUR_TWITCH_USERNAME>"

MUSIC_REWARD_NAME = "<YOUR_CHANNEL_REWARD_NAME>"
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