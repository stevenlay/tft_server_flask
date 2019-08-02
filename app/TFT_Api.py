import requests
import json
import cv2 
import app.image_conversion as image_conversion

class TFT_Api:
    def __init__(self):
        self.url = 'https://api.twitch.tv/kraken/streams?game=Teamfight%20Tactics&broadcaster_language=en'
        self.headers = {
        'Client-ID': 'q07uubs3hamg484jor8gh4sspy1onu'
        }

    def get_top_streams(self):
        r = requests.get(self.url, headers=self.headers)
        y = json.loads(r.text)
        y = y['streams']
        res = []
        for stream in y:
            channel = stream['channel']
            streamer = {}
            streamer['_id'] = stream['_id']
            streamer['viewers'] = stream['viewers']
            streamer['language'] = channel['broadcaster_language']
            streamer['display_name'] = channel['display_name']
            streamer['logo'] = channel['logo']
            streamer['status'] = channel['status']
            streamer['url'] = channel['url']
            streamer['preview'] = stream['preview']['template'].replace('{width}', '1920').replace('{height}', '1080')
            streamer['stage'] = image_conversion.img_pipeline(streamer['preview'], streamer['display_name'])
            res.append(streamer)
        return res
