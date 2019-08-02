import streamlink
from threading import Thread
import subprocess as sp
import cv2
from TFT_Api import TFT_Api
import image_conversion

import time

class StreamShotter:
    def __init__(self, resolution='1080p60'):
        self.res = resolution
        self.active_streams = set()
        self.streamer_to_m3u8 = {}
        self.stream_t_dict = {}
        self.pipe = None
    
    def call_sp(self, streamer_name):
        sp.call(['ffmpeg','-y', '-i', self.streamer_to_m3u8[streamer_name], '-r', '0.1', '-f', 'image2', '-vframes',  '1', 'images/output_%s.jpg' % streamer_name])

    def update_streams_streamlink(self, urls):
        updated_set = set()
        for url in urls:
            streamer_name = url.split("/")[3]
            updated_set.add(streamer_name)
            try:
                # new stream
                if streamer_name not in self.active_streams:
                    session = streamlink.Streamlink()
                    streams = session.streams(url)
                    if streams and self.res in streams:
                        self.streamer_to_m3u8[streamer_name] = streams[self.res].url
                        self.active_streams.add(streamer_name)
                        
                    else:
                        print("Either offline or resolution not supported for: " + streamer_name)
                # ffmpeg -y -i pipe:0 -r 0.1 -f image2 -vframes  1  output_dog1.jpg
                t1 = Thread(target=self.call_sp, args=(streamer_name,))
                self.stream_t_dict[streamer_name] = t1
                t1.start()
                
                # self.call_sp(streamer_name)
        
            except:
                print("Error: " + streamer_name)
        # remove inactive streams in the list: either offline or no longer top 25
        for stream in self.active_streams:
            if stream not in updated_set:
                self.active_streams.remove(stream)
                self.streamer_to_m3u8.pop(stream)

                # TODO
                # need to get rid of streamlink for this particular stream
                self.stream_t_dict[stream]

    def update_streams_preview(self, urls):
        pass

    def process_images(self):
        print(self.active_streams)
        for streamer in self.active_streams:
            img = cv2.imread("images/output_imaqtpie.jpg")
            cv2.imshow("cropped", img)
            cv2.waitKey()
                

def main():
    start = time.time()


    api = TFT_Api()
    top = api.get_top_streams()
    print(top)




    end = time.time()
    print(end - start)
    # print(stream_shotter.streamer_to_m3u8)
    # print(stream_shotter.active_streams)

if __name__ == "__main__":
    main()

# streamlink https://twitch.tv/DisguisedToast 1080p60 -O | ffmpeg -i pipe:0 -r 0.1 -f image2 -update 1 output_toast.jpg