import time
#import json
import urllib.request
import io
import os
import numpy as np
import requests
import skvideo.io
import static_video_analyzer as video_analyzer
#import datetime



def load_video(path):
    #TODO: search metadata for timestamp
    PATH_TO_VIDEO = path
    metadata = skvideo.io.ffprobe(PATH_TO_VIDEO)
    frames = []
    fps = metadata['video']['@r_frame_rate']
    fps = fps.split(sep='/')
    fps = int(fps[0])/int(fps[1])
    #num_of_frames = int(metadata['video']['@nb_frames'])
    width = int(metadata['video']['@width'])
    height = int(metadata['video']['@height'])
    sequence = skvideo.io.vreader(PATH_TO_VIDEO)
    for f in sequence:
        frames += [f]
    return fps, width, height, frames

def download_from_storage(video_url):
    A = urllib.request.urlopen(video_url)
    data = A.read()
    vfile = open('temp.mp4', 'wb')
    vfile.write(data)
    vfile.close()
    fps, width, height, frames = load_video('temp.mp4')
    os.remove('temp.mp4')
    print("Printing video info: fps, width, height, frames.shape")
    print(fps, width, height, len(frames))
    return fps, width, height, frames

  



def call_analyzer(video_url,thresh_flag):
    timestamp=str(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
    fps, width, height, frames = download_from_storage(video_url)
    
    file_name=video_url.rsplit(sep='/')[-1].rsplit(sep='.', maxsplit=1)[0]
    file_type=video_url.rsplit(sep='.', maxsplit=1)[-1]
    print(file_type)
    #storage_link=URL_str.rsplit(sep='/', maxsplit=1)[-1]
    storage_link=video_url.rsplit(sep='/', maxsplit=1)[0]#in case the video is stored in a different subfolder
    
    
#    bjson_links, runtime_a, runtime_u = process_video(fps, width, height, frames, timestamp, file_name,storage_link,file_type)
    video_analyzer.analyze(frames, width, height, fps,storage_link, str(file_name+'.'+file_type), timestamp,thresh_flag)
#    return bjson_links, runtime_a, runtime_u
    