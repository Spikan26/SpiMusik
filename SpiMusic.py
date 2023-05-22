import tkinter as tk
import concurrent.futures
import re
import vlc
import random
import time
import socket
import json
import websocket as wsapp
import requests
import threading
from yt_dlp import YoutubeDL
import config

# Global Variable
playState = True
firstPlay = True
MAX_TIME_TO_WAIT_FOR_LOGIN = 3
BROADCASTER_ID = ""
MODERATORS_LIST = set()
MESSAGE_RATE = 0.5
MAX_QUEUE_LENGTH = 20
MAX_WORKERS = 100
last_time = time.time()

message_queue = []

thread_pool = concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS)

active_tasks = []


##################### VLC #####################

class VLC:

    def __init__(self):
        self.volumelevel = 50
        self.currentTitle = ""
        self.playlist_id = self.getIDPlaylist(config.playlistURL)
        self.playlist_count = self.getPlaylistCount(config.playlistURL)
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
                            self.currentDuration = entries['duration']
                            self.currentTitle = entries['title']
                            break
                        except:
                            pass

                self.mediaPlayer.set_mrl(url_yt, ":no-video")
                self.mediaPlayer.play()

    def addFromQueuelist(self):
        # (link, title, user)
        obj_request = self.queuelist.pop(0)
        app.vlclistbox.delete(0)

        with YoutubeDL({'ignoreerrors': True, 'quiet': True}) as ydl:
            video_info = ydl.extract_info(
                obj_request["link"], download=False)
            url_yt = ""
            for i, format in enumerate(video_info['formats']):
                try:
                    url_yt = format['audio_channels']
                    url_yt = format['url']
                    self.currentTitle = video_info['title']
                    break
                except:
                    pass

            self.mediaPlayer.set_mrl(url_yt, ":no-video")
            self.mediaPlayer.play()
            print("Request from "+obj_request["user"])

    def updateTitle(self):
        global app
        app.current_play.config(text=str(self.currentTitle))
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

    def volume(self):
        self.mediaPlayer.audio_set_volume(int(self.volumelevel))

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

    def remove_from_playlist(self):
        tupl = app.vlclistbox.curselection()
        for selection in tupl:
            app.vlclistbox.delete(selection)
            del self.queuelist[int(selection)]

    def test(self):
        user_request = "Spikan"
        link = "https://www.youtube.com/watch?v=LFFazcHOj5Y"
        with YoutubeDL({'ignoreerrors': True, 'quiet': True}) as ydl:
            video_info = ydl.extract_info(url=link, download=False)
            with open('aaaaa.txt', 'w', encoding='utf-8') as f:
                f.write(str(video_info))

            self.queuelist.append(
                {"link": link, "title": video_info['title'], "user": user_request})
            print("ADDED TO QUEUELIST")
            app.vlclistbox.insert(tk.END, str(video_info['title']))


##################### Tkinter #####################

class SpiMusik:
    def __init__(self):
        global player
        # Create a new window
        self.root = tk.Tk()

        # Set the title of the window
        self.root.title("SpiMusik")

        # Set the size of the window
        self.root.geometry("600x400")

        # Create a function to handle slider updates
        self.titlePlayingBox = tk.Frame(self.root, name="currentplay")
        self.controlBox = tk.Frame(self.root, name="volume")
        self.controlBtnBox = tk.Frame(self.root, name="bouton")
        self.playerProgress = tk.Frame(self.root, name="progress")
        self.playlistBox = tk.Frame(self.root, name="queue")

        # Create a label for the slider
        self.current_play = tk.Label(
            self.titlePlayingBox, name="current_play", text="...", background="light blue")
        self.current_play.grid(column=0, row=0)

        self.titlePlayingBox.pack()

        # Create a label for the slider
        self.volume_label = tk.Label(
            self.controlBox, name="volume_label", text="Volume: 0")
        self.volume_label.grid(column=1, row=1)

        # Create a slider
        self.volume_slider = tk.Scale(self.controlBox, name="volume_slider", from_=0, to=100, orient=tk.HORIZONTAL, length=200,
                                      command=lambda value: self.slider_update(value))
        self.volume_slider.grid(column=2, row=1)

        self.controlBox.pack()

        # Create buttons
        self.play_button = tk.Button(self.controlBtnBox, name="play_button", text="Play",
                                     command=lambda: player.play())
        self.play_button.grid(column=0, row=2)

        self.stop_button = tk.Button(self.controlBtnBox, name="stop_button", text="Stop",
                                     command=lambda: player.stop())
        self.stop_button.grid(column=1, row=2)

        self.next_button = tk.Button(self.controlBtnBox, name="next_button", text="Next",
                                     command=lambda: player.next())
        self.next_button.grid(column=2, row=2)

        # self.test_button = tk.Button(self.controlBtnBox, name="test_button", text="TEST",
        #                              command=lambda: player.test())
        # self.test_button.grid(column=3, row=2)

        self.connect_button = tk.Button(self.controlBtnBox, name="connect_button", text="Connect",
                                        command=lambda: on_connect())
        self.connect_button.grid(column=4, row=2)

        self.controlBtnBox.pack()

        self.player_progress = tk.Label(
            self.playerProgress, name="player_progress", text="0:00 / 0:00")
        self.player_progress.grid(column=0, row=0)

        self.playerProgress.pack()

        self.vlclistbox = tk.Listbox(self.playlistBox, width=40,
                                     height=15, name="queuelistbox")

        self.vlclistbox.insert(tk.END, *player.queuelist)
        self.vlclistbox.select_set(1)
        self.vlclistbox.grid(column=0, row=0)

        self.remove_button = tk.Button(self.playlistBox, name="remove_button", text="Remove from playlist",
                                       command=lambda: player.remove_from_playlist())
        self.remove_button.grid(column=0, row=1)

        self.playlistBox.pack()

    def slider_update(self, value):
        self.volume_label.config(text=f"Volume: {value}")
        player.volumelevel = value
        player.volume()

    def current_player_time(self):
        current_time_min = (player.mediaPlayer.get_time() // 1000) // 60
        current_time_sec = (player.mediaPlayer.get_time() // 1000) % 60
        total_time_min = player.currentDuration // 60
        total_time_sec = player.currentDuration % 60

        actual_time = f"{current_time_min:02d}:{current_time_sec:02d} / {total_time_min:02d}:{total_time_sec:02d}"
        self.player_progress.config(text=actual_time)
        self.root.after(1000, self.current_player_time)

    def twitch_get_messages(self):
        get_twitch_tchat()
        self.root.after(1000, self.twitch_get_messages)


##################### Websocket Twitch : Custom Reward #####################

def eventsub_add_music(data):
    user_name = data["payload"]["event"]["user_name"]
    user_input = data["payload"]["event"]["user_input"]
    print(user_name+': '+user_input)
    x = re.findall(
        "http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)[\w\=]*)?", user_input)
    if len(x) > 0:
        request_url = "https://www.youtube.com/watch?v="+x[0][0]

        with YoutubeDL({'ignoreerrors': True, 'quiet': True}) as ydl:
            video_info = ydl.extract_info(url=request_url, download=False)

            player.queuelist.append(
                {"link": request_url, "title": video_info['title'], "user": user_name})
            print("ADDED TO QUEUELIST : "+video_info['title'])
            app.vlclistbox.insert(tk.END, str(video_info['title']))


def eventsub_subscription(data):
    global BROADCASTER_ID
    session_id = data["payload"]["session"]["id"]

    print("subscribing to event listener...")
    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": "Bearer "+config.TWITCH_AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    payload = {
        "type": "channel.channel_points_custom_reward_redemption.add",
        "version": "1",
        "condition": {
            "broadcaster_user_id": BROADCASTER_ID
        },
        "transport": {
            "method": "websocket",
            "session_id": session_id
        }
    }
    rsp = requests.post(url, headers=headers, json=payload)
    print(rsp.text)
    print("subscription done")


def eventsub_clean():
    url = 'https://api.twitch.tv/helix/eventsub/subscriptions'
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": "Bearer "+config.TWITCH_AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)

    data = json.loads(response.content)
    for old_eventsub in data['data']:
        url_delete = 'https://api.twitch.tv/helix/eventsub/subscriptions?id=' + \
            str(old_eventsub['id'])
        headers_delete = {
            "Client-ID": config.TWITCH_CLIENT_ID,
            "Authorization": "Bearer "+config.TWITCH_AUTH_TOKEN,
            "Content-Type": "application/json"
        }
        requests.delete(url=url_delete, headers=headers_delete)


def eventsub_get_broadcast_id():
    url = 'https://api.twitch.tv/helix/users?login=' + \
        config.BROADCASTER_USER_NAME.lower()
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": "Bearer "+config.TWITCH_AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    return data['data'][0]['id']


def eventsub_get_moderators(broad_id):
    url = 'https://api.twitch.tv/helix/moderation/moderators?broadcaster_id=' + broad_id
    headers = {
        "Client-ID": config.TWITCH_CLIENT_ID,
        "Authorization": "Bearer "+config.TWITCH_AUTH_TOKEN,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.content)
    mod_list = set()
    mod_list.add(config.BROADCASTER_USER_NAME)
    for mod in data['data']:
        mod_list.add(mod['user_name'].lower())
    return mod_list


def event_notification(data):

    match data["payload"]["event"]["reward"]["title"]:
        case config.MUSIC_REWARD_NAME:
            eventsub_add_music(data)
        case _:
            # print(data)
            pass


##################### Websocket Twitch : Read/Write Tchat #####################

class Twitch:
    re_prog = None
    sock = None
    partial = b''
    login_ok = False
    channel = config.BROADCASTER_USER_NAME.lower()
    login_timestamp = 0

    def twitch_connect(self, channel):
        if self.sock:
            self.sock.close()
        self.sock = None
        self.partial = b''
        self.login_ok = False
        self.channel = channel

        # Compile regular expression
        self.re_prog = re.compile(
            b'^(?::(?:([^ !\r\n]+)![^ \r\n]*|[^ \r\n]*) )?([^ \r\n]+)(?: ([^:\r\n]*))?(?: :([^\r\n]*))?\r\n', re.MULTILINE)

        # Create socket
        print('Connecting to Twitch...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Attempt to connect socket
        self.sock.connect(('irc.chat.twitch.tv', 6667))

        # Log in
        user = 'spibot'
        print('Connected to Twitch. Logging in...')
        self.sock.send(
            ('PASS oauth:'+config.TWITCH_AUTH_TOKEN+'\r\nNICK %s\r\n' % user).encode())

        self.sock.settimeout(1.0/60.0)

        self.login_timestamp = time.time()

    # Attempt to reconnect after a delay
    def reconnect(self, delay):
        time.sleep(delay)
        self.twitch_connect(self.channel)

    # Returns a list of irc messages received
    def receive_and_parse_data(self):
        buffer = b''
        while True:
            received = b''
            try:
                received = self.sock.recv(4096)
            except socket.timeout:
                break
            # except OSError as e:
            #     if e.winerror == 10035:
            #         # This "error" is expected -- we receive it if timeout is set to zero, and there is no data to read on the socket.
            #         break

            except Exception as e:
                print('Unexpected connection error. Reconnecting in a second...', e)
                self.reconnect(1)
                return []

            if not received:
                print('Connection closed by Twitch. Reconnecting in 5 seconds...')
                self.reconnect(5)
                return []

            buffer += received

        if buffer:
            # Prepend unparsed data from previous iterations
            if self.partial:
                buffer = self.partial + buffer
                self.partial = []

            # Parse irc messages
            res = []
            matches = list(self.re_prog.finditer(buffer))

            for match in matches:
                res.append({
                    'name':     (match.group(1) or b'').decode(errors='replace'),
                    'command':  (match.group(2) or b'').decode(errors='replace'),
                    'params':   list(map(lambda p: p.decode(errors='replace'), (match.group(3) or b'').split(b' '))),
                    'trailing': (match.group(4) or b'').decode(errors='replace'),
                })

            # Save any data we couldn't parse for the next iteration
            if not matches:
                self.partial += buffer
            else:
                end = matches[-1].end()
                if end < len(buffer):
                    self.partial = buffer[end:]

                if matches[0].start() != 0:
                    # If we get here, we might have missed a message.
                    print(
                        'oops, i think we missed a message....')

            return res

        return []

    def twitch_receive_messages(self):
        privmsgs = []
        for irc_message in self.receive_and_parse_data():
            cmd = irc_message['command']
            if cmd == 'PRIVMSG':
                privmsgs.append({
                    'username': irc_message['name'],
                    'message': irc_message['trailing'],
                })
            elif cmd == 'PING':
                self.sock.send(b'PONG :tmi.twitch.tv\r\n')
            elif cmd == '001':
                print('Successfully logged in. Joining channel %s.' %
                      self.channel)
                self.sock.send(('JOIN #%s\r\n' % self.channel).encode())
                self.login_ok = True
            elif cmd == 'JOIN':
                print('Successfully joined channel %s' %
                      irc_message['params'][0])
            elif cmd == 'NOTICE':
                print('Server notice:',
                      irc_message['params'], irc_message['trailing'])
            elif cmd == '002':
                continue
            elif cmd == '003':
                continue
            elif cmd == '004':
                continue
            elif cmd == '375':
                continue
            elif cmd == '372':
                continue
            elif cmd == '376':
                continue
            elif cmd == '353':
                continue
            elif cmd == '366':
                continue
            else:
                print('Unhandled irc message:', irc_message)

        if not self.login_ok:
            # We are still waiting for the initial login message. If we've waited longer than we should, try to reconnect.
            if time.time() - self.login_timestamp > MAX_TIME_TO_WAIT_FOR_LOGIN:
                print('No response from Twitch. Reconnecting...')
                self.reconnect(0)
                return []

        return privmsgs

    def bruh(self):
        self.sock.send(b'PRIVMSG #spikan :This is a text message\r\n')


def get_twitch_tchat():
    global active_tasks
    global MAX_QUEUE_LENGTH
    global messages_to_handle
    global last_time
    global MESSAGE_RATE
    global message_queue

    active_tasks = [t for t in active_tasks if not t.done()]

    # Check for new messages
    new_messages = twirc.twitch_receive_messages()

    if new_messages:
        message_queue += new_messages  # New messages are added to the back of the queue
        # Shorten the queue to only the most recent X messages
        message_queue = message_queue[-MAX_QUEUE_LENGTH:]

    messages_to_handle = []

    if not message_queue:
        # No messages in the queue
        last_time = time.time()
    else:
        # Determine how many messages we should handle now
        r = 1 if MESSAGE_RATE == 0 else (
            time.time() - last_time) / MESSAGE_RATE
        n = int(r * len(message_queue))
        if n > 0:
            # Pop the messages we want off the front of the queue
            messages_to_handle = message_queue[0:n]
            del message_queue[0:n]
            last_time = time.time()

    if not messages_to_handle:
        pass
    else:
        for message in messages_to_handle:
            if len(active_tasks) <= MAX_WORKERS:
                active_tasks.append(
                    thread_pool.submit(handle_message, message))
            else:
                print(
                    f'WARNING: active tasks ({len(active_tasks)}) exceeds number of workers({MAX_WORKERS}). ({len(message_queue)} messages in the queue)')


def handle_message(message):
    try:
        msg = message['message'].lower()
        username = message['username'].lower()
        # print("Got this message from " + username + ": " + msg)

        if msg.startswith("!spimusik") and (username in MODERATORS_LIST):
            msg_split = msg.split(' ')
            try:
                print(msg_split[1])
                match msg_split[1]:
                    case 'help':
                        pass
                    case 'add':
                        print("Adding song to queue")
                        datajson = "{\"payload\":{\"event\":{\"user_name\":\"" + \
                            username+"\",\"user_input\":\"" + \
                            message['message']+"\"}}}"
                        data = json.loads(datajson)
                        eventsub_add_music(data)
                    case 'remove':
                        try:
                            app.vlclistbox.delete(int(msg_split[2])-1)
                            del player.queuelist[int(msg_split[2]-1)]
                        except:
                            pass
                    case 'check':
                        print(player.queuelist[int(msg_split[2])])
                        twirc.sock.send(('PRIVMSG #'+config.BROADCASTER_USER_NAME.lower() +
                                         ' :Song in position '+str(msg_split[2])+' - '+str(player.queuelist[int(msg_split[2])-1]["title"])+' - Request by '+str(player.queuelist[int(msg_split[2])]["user"])+'\r\n').encode())
                    case 'next':
                        player.next()
                        pass
                    case _:
                        pass
            except:
                pass

            # twirc.sock.send(('PRIVMSG #'+config.BROADCASTER_USER_NAME +
            #                ' :Current song - '+str(player.currentTitle)+'\r\n').encode())
            #print("OH !! UNE COMMANDE !!")

    except Exception as e:
        print("Encountered exception: " + str(e))

##################### Websocket Twitch : Connexion #####################


def on_message(ws, message):
    # print(message)
    data = json.loads(message)

    match data["metadata"]["message_type"]:
        case 'session_welcome':
            eventsub_subscription(data)
        case 'notification':
            event_notification(data)
        case 'session_keepalive':
            print('.', end="")


def on_error(ws, error):
    # print(error)
    print('Error Websocket')
    print(str(error))


def on_close(ws, reason, details):
    print(str(reason))
    print(str(details))
    print('Websocket: closed')


def on_open(ws):
    global BROADCASTER_ID
    global MODERATORS_LIST

    print("Connexion with twitch")
    eventsub_clean()
    BROADCASTER_ID = eventsub_get_broadcast_id()
    MODERATORS_LIST = eventsub_get_moderators(BROADCASTER_ID)
    print('Broadcast ID:', BROADCASTER_ID)


def connect_to_websocket():
    ws = wsapp.WebSocketApp("wss://eventsub-beta.wss.twitch.tv/ws",
                            on_message=on_message, on_error=on_error, on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()
    return


def on_connect():
    thr = threading.Thread(target=connect_to_websocket)
    thr.start()
    twirc.twitch_connect(config.BROADCASTER_USER_NAME.lower())
    app.root.after(2000, app.twitch_get_messages)


############################################################################################################

player = VLC()
app = SpiMusik()
twirc = Twitch()
# Run the window
app.root.after(1000, player.updateTitle())
app.root.after(2000, app.current_player_time())
app.root.mainloop()