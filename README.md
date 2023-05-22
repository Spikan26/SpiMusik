(I'll make a guide later on how to install it, but for now, just ask me on discord)

**Install VLC (x64)**

**Install Python**

**Install at least the following** (a few other packages are needed):
- pip install websocket-client
- pip install yt_dlp
- pip install python-vlc
- pip install json


# Config File
Create a config file with the following :

```py
playlistURL = "<YOUR_YOUTUBE_PLAYLIST>"

TWITCH_CLIENT_ID = "<YOUR_CLIENT_ID>"
TWITCH_AUTH_TOKEN = "<YOUR_OAUTH_TOKEN>"


BROADCASTER_USER_NAME = "<YOUR_TWITCH_USERNAME>"

MUSIC_REWARD_NAME = "<YOUR_CHANNEL_REWARD_NAME>"
```

- **[WTF is TWITCH_CLIENT_ID] ?**

You can get it by creating an application with this link [dev.twitch.tv/console/apps](https://dev.twitch.tv/console/apps). This is the client_id of your application.

In the "Redirect url" section, add the following URL : 

```
https://twitchapps.com/tokengen/
```

- **[WTF is TWITCH_AUTH_TOKEN] ?**

To get your OAuth Token, you must go to this link by replacing <CLIENT_ID> with your TWITCH_CLIENT_ID :

```
https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=<CLIENT_ID>&redirect_uri=https://twitchapps.com/tokengen/&scope=channel%3Aread%3Aredemptions+channel%3Amanage%3Aredemptions+chat%3Aread+chat%3Aedit+moderation%3Aread
```