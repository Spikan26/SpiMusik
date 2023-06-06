import config
import vlc
import random
import re
from yt_dlp import YoutubeDL

playState = False
firstPlay = True


class VLC:

    def __init__(self):
        self.volumelevel = 50
        self.currentTitle = ""
        self.yt_url = ""
        self.playlist_id = self.getIDPlaylist(config.PLAYLIST_URL)
        self.playlist_count = self.getPlaylistCount(config.PLAYLIST_URL)
        self.mediaPlayer = vlc.MediaPlayer('--loop')
        self.mediaPlayer.audio_set_volume(50)
        self.queuelist = []
        self.memorylist = list(range(1, self.playlist_count))
        random.shuffle(self.memorylist)
        self.addFromPlaylist()
        self.event_vlc()

    def getIDPlaylist(self, playlistURL):
        # define the regex pattern
        pattern = r'list=([a-zA-Z0-9_-]+)'

        # extract the ID from the link using regex
        match = re.search(pattern, playlistURL)
        if match:
            playlist_id = match.group(1)
            return playlist_id
        else:
            return None

    def getPlaylistCount(self, playlistURL):
        playlist_info = YoutubeDL({'ignoreerrors': True, 'playlist_items': '1', 'quiet': True}).extract_info(
            url=playlistURL, download=False)
        playlist_count = playlist_info['playlist_count']
        return playlist_count

    def getRandomID(self):
        if len(self.memorylist) < 1:
            self.memorylist = list(range(1, self.playlist_count))
            random.shuffle(self.memorylist)
        return self.memorylist.pop()

    def addFromPlaylist(self):
        randid = self.getRandomID()
        print("randid is "+str(randid) + "/" + str(self.playlist_count))

        play_url = 'https://www.youtube.com/watch?v=gg&list=' + \
            self.playlist_id + '&index='+str(randid)
        with YoutubeDL({'ignoreerrors': True, 'playlist_items': str(randid), 'quiet': True}) as ydl:
            video_info = ydl.extract_info(
                play_url, download=False)

            url_yt = ""

            if video_info['entries'][0] is None:
                print("Video is private or unavailable")
                self.addFromPlaylist()
            else:
                # iterate through all of the available formats
                for entries in video_info['entries']:
                    for i, format in enumerate(entries['formats']):
                        try:
                            url_yt = format['audio_channels']
                            url_yt = format['url']
                            self.yt_url = "www.youtube.com/watch?v=" + \
                                entries['id']
                            self.currentDuration = entries['duration']
                            self.currentTitle = entries['title']
                            break
                        except:
                            pass

                self.mediaPlayer.set_mrl(url_yt, ":no-video")
                if firstPlay:
                    pass
                else:
                    self.mediaPlayer.play()

    def addFromQueuelist(self):
        # (link, title, user)
        obj_request = self.queuelist.pop(0)

        with YoutubeDL({'ignoreerrors': True, 'quiet': True}) as ydl:
            video_info = ydl.extract_info(
                obj_request["link"], download=False)
            url_yt = ""
            for i, format in enumerate(video_info['formats']):
                try:
                    url_yt = format['audio_channels']
                    url_yt = format['url']
                    self.yt_url = "www.youtube.com/watch?v=" + \
                        video_info['id']
                    self.currentTitle = video_info['title']
                    break
                except:
                    pass

            self.mediaPlayer.set_mrl(url_yt, ":no-video")
            self.mediaPlayer.play()
            print("Request from "+obj_request["user"])

    def updateTitle(self):
        with open('current_title_source.txt', 'w', encoding='utf-8') as f:
            f.write(str(self.currentTitle)+" - ")
        print(self.currentTitle)

    def play(self):
        global playState
        global firstPlay

        if(firstPlay):
            firstPlay = False

        if (playState):
            self.mediaPlayer.pause()
            playState = False
            return

        playState = True
        self.mediaPlayer.play()

    def next(self):
        self.mediaPlayer.stop()
        self.mediaPlayer = vlc.MediaPlayer('--loop')
        if len(self.queuelist) > 0:
            self.addFromQueuelist()
        else:
            self.addFromPlaylist()
        self.event_vlc()
        self.updateTitle()

    def pause(self):
        self.mediaPlayer.pause()

    def stop(self):
        global playState

        playState = False
        self.mediaPlayer.stop()

    def volume(self, volumelevel):
        self.volumelevel = int(volumelevel)
        self.mediaPlayer.audio_set_volume(int(volumelevel))

    def event_vlc(self):
        # Event for media stop
        self.mediaPlayer.event_manager().event_attach(
            vlc.EventType.MediaPlayerEndReached, self.media_player_on, 1)

    def media_player_on(self, event, arg):
        print("Music ended")
        self.mediaPlayer = vlc.MediaPlayer('--loop')
        if len(self.queuelist) > 0:
            self.addFromQueuelist()
        else:
            self.addFromPlaylist()
        self.event_vlc()
        self.updateTitle()

    def remove_from_playlist(self, selection):
        del self.queuelist[int(selection-1)]

    def test(self):
        print(self.yt_url)
        pass