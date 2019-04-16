import socket
import sys
from threading import Lock, Thread
import time
import json
import urllib.request
import io
import os
import numpy as np
import requests
import skvideo.io
import static_video_analyzer as video_analyzer
import datetime
#import stream2
import stream_final
import video_loader

#get lock object
lock = Lock()

#open logger
f = open('log.txt', 'a')

HOST = ''   # Symbolic name meaning all available interfaces
PORT = 9997 # Arbitrary non-privileged port

home_storage_link = 'https://beaware-1.eu-de.containers.appdomain.cloud/object-store'

def call_stream():
    timelapse=1#min
    
    global dead
    while not dead:
        print("Streaming started")
        #stream2.run_stream()
        stream_final.run_stream()
        time.sleep(timelapse*60)
        #if stop():
            #print("Stopping Streaming loop.")
            #break
    print("Stopping Streaming loop.")





    
def save_to_storage(bobj,storage_link, filename,headers):
    r = requests.post(storage_link+'/'+filename, bobj, headers=headers)
    print(storage_link+'/'+filename)
    if not r.ok:
        print('Didn\'t happen')

def send_to_certh_hub(bjson_links, conn):
    conn.send(bjson_links)

def handle_message(bmsg, conn):
    global dead
    dead=False#Maybe I could set it True here, in order to stop streaming everytime I call another instance
    
    
    msg = bmsg.decode()
    mydict = json.loads(msg)
    task = mydict['message']['task']
    
#    start = time.time()
    if task=="alarm1":
        #1.94m
        video_url = "https://beaware-1.eu-de.containers.appdomain.cloud/object-store/bacchiglione_firstVideo.mp4"
        #bjson_links, runtime_a, runtime_u=video_loader.call_analyzer(video_url)
        video_loader.call_analyzer(video_url,'mockup')
    if task=="alarm2":
        #3.30m
        video_url = "https://beaware-1.eu-de.containers.appdomain.cloud/object-store/bacchiglione_secondVideo.mp4"
#        bjson_links, runtime_a, runtime_u=video_loader.call_analyzer(video_url)
        video_loader.call_analyzer(video_url,'mockup')
    if task=="alarm3":
        #4.06m
        video_url = "https://beaware-1.eu-de.containers.appdomain.cloud/object-store/bacchiglione_thirdVideo.mp4"
#        bjson_links, runtime_a, runtime_u=video_loader.call_analyzer(video_url)
        video_loader.call_analyzer(video_url,'mockup')
    if task=="start_streaming":
        dead=False
        stream_thread = Thread(target=call_stream)
        stream_thread.start()        
        #bjson_links, runtime_a, runtime_u=
               
    if task=="stop_streaming":
        dead=True
        print("Stop streaming requested...")
        #bjson_links, runtime_a, runtime_u=
        
    if task not in ["alarm1", "alarm2", "alarm3","start_streaming","stop_streaming"]:
        print('Wrong Task name provided')
        return
    
    
#    end = time.time()   
#    runtime_d=end-start
    
    
    dict_to_send = {"message":"finished"}
    bjson_links = json.dumps(dict_to_send).encode()
    send_to_certh_hub(bjson_links, conn)
    #os.remove('./output/'+file_name+'_output.avi')
    #os.remove('./output/'+file_name+'_output.json')
#    return runtime_d, runtime_a, runtime_u

#Function for handling connections. This will be used to create threads
def clientthread(conn):
    #global f
    lock.acquire()
#    f = open('log.txt', 'a')
    while 1:
        bmsg = conn.recv(1024)
        msg = bmsg.decode()
#        f.write("Hub says: "+msg+'\n')
        if(msg=="Msg from VRS received"):
            #to_send = "Bye hub!"
            #conn.sendall(to_send.encode())
            break
        else:
            to_send = "Msg received from Hub"
            conn.sendall(to_send.encode())
            start = time.time()
    #try:
#        run_d, run_a, run_u = handle_message(bmsg, conn)
        handle_message(bmsg, conn)

#        end = time.time()
#        runtime = end - start
#        f.write("Download complete. Runtime: {0}\n".format(run_d))
#        f.write("Video analysis done. Runtime: {0}\n".format(run_a))
#        f.write("Upload complete. Runtime: {0}\n".format(run_u))
#        f.write("Message handling done. Runtime: {0}\n".format(runtime))
#    #except:
#        #print("A problem occured, please check the url link or the signal format")
#        #f.write("Unknown error occured\n")
#        #break

    conn.close()
#    f.write('Connection closed\n')
#    f.write(time.strftime('%X %x %Z')+'\n')
#    f.close()
#    blog = open('log.txt', 'rb')
##    save_to_storage(blog, "video-analysis.log")
#    save_to_storage(blog,home_storage_link, "vrs-analysis.log", headers = {'Content-Type':"text/plain"})  #na allaxthei

    lock.release()
    return

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#f.write('Socket created\n')
 
#Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
#    f.write('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1] + '\n')
    sys.exit()    
#f.write('Socket bind complete\n')

#Start listening on socket
s.listen(10)
f.write('Socket now listening\n')
f.close()
t = []
#now keep talking with the client
while 1:
    #wait to accept a connection - blocking call
    print('Ready for a new connection...\n')
    #f.write('Waiting for a new connection...')
    conn, addr = s.accept()
    f = open('log.txt', 'a')
    f.write('Connected with ' + addr[0] + ':' + str(addr[1]) + '\n')
    f.close()
    #start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
    t += [Thread(target=clientthread , args=(conn,))]
    t[-1].start()

s.close()
