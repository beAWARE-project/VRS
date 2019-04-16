import numpy as np
import cv2
import skvideo.io
import urllib.request
import io
import requests
import os
import time
import datetime
import json
import socket
import sys
import static_video_analyzer  as video_analyzer
import video_loader



def run_stream():
    #timestamp = datetime.datetime.utcnow()
    #timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ', gmtime())
    timestamp= time.strftime('%Y%m%dT%H%M%S', time.gmtime())
    width=640
    height=360
    duration_vid=10 #seconds
    format_out='webm'
    frames=[]
    
    cap  = cv2.VideoCapture('http://195.31.128.29:8080/mjpg/1/video.mjpg')
    fps = cap.get(cv2.CAP_PROP_FPS);
    #cap.set(5,10)#fps
    #cap.set(3,640)#width
    #cap.set(4,360)#height
    
    
    print('Initial fps='+str(fps))
    
 
        

    # Capture frames----------------
    #f_count=0;
    start=time.time()
    while(cap.isOpened()):
        ret, frame = cap.read()

        #if ret==True:
        #if (f_count<duration_vid*fps):
        if (time.time()-start)<=duration_vid:
            #f_count=f_count+1
            
            frames.append(frame)
            
    
            #cv2.imshow('frame',frame)
            #if cv2.waitKey(1) & 0xFF == ord('q'):
            #    break
        else:
            break
    #-------------------------------
    cap.release()       
    cv2.destroyAllWindows()        
    end=time.time()
    start=time.time()
    print('Number of frames='+str(len(frames)))
    print("Streaming time="+str(end-start))
    # Release everything if job is finished
    #fps=round(len(frames)/duration_vid)
    fps=len(frames)/duration_vid
    print('New fps= '+str(fps))
    
    
    
    
    
    
    #Write frames to file~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    #fourcc = cv2.VideoWriter_fourcc(*'MPEG')   
    #writer = cv2.VideoWriter('output.mp4',fourcc, 1.0, (1920,1080))  #na to allaksw. Na valw height kai width
    #writer = cv2.VideoWriter('output.avi', -1, 20.0, (1920,1080))

    
    filename='bacchiglione'+str(timestamp)+'.'+format_out
    if format_out=='avi':
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #writer = cv2.VideoWriter('output.avi',fourcc, fps, (width,height))
        writer = cv2.VideoWriter(filename,fourcc, fps, (width,height))
        for i in range(len(frames)):
            frame_im = cv2.resize(frames[i],(width, height)) 
            writer.write(frame_im)
        writer.release()
  
    if format_out=='mp4':
        fourcc = cv2.VideoWriter_fourcc(*'MP4V')
        writer = cv2.VideoWriter(filename,fourcc, fps, (width,height))
        #writer = cv2.VideoWriter(self._name, self._fourcc, fps, (width,height))
        for i in range(len(frames)):
            frame_im = cv2.resize(frames[i],(width, height)) 
            writer.write(frame_im)
        writer.release()
    
    
    if format_out=='webm':
        #filename_storage=file_name+'_output.'+format_out
        #to_write = np.array(buffer)
        writer = skvideo.io.FFmpegWriter(filename,
                                 inputdict={'-r': str(fps)},
                                 outputdict={'-vcodec': 'libvpx', '-b': '500000', '-r': str(fps)})    
        for i in range(len(frames)):
            frame_im = cv2.resize(frames[i],(width, height)) 
            frame_im=cv2.cvtColor(frame_im, cv2.COLOR_RGB2BGR)
            writer.writeFrame(frame_im)   
        writer.close()
        
     #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    







    #Upload file to storage************************************

    headers = {'Content-Type':"video/"+format_out}
    data = open(filename, 'rb')
    #Upload to storage
    link = "https://beaware-1.eu-de.containers.appdomain.cloud/object-store/CCTV1/"+filename
    r = requests.post(link, data, headers=headers)
    if not r.ok:
        print('File was not uploaded to Storage. Retrying')
        while not r.ok:
            r = requests.post(link, data, headers=headers)
            print('File was not uploaded to Storage. Retrying')
		
    data.close()
    #**********************************************************

    #delete local file
    os.remove(filename)
    
    #analyze video
#    bjson_links, runtime_a, runtime_u=video_loader.call_analyzer(link)
    video_loader.call_analyzer(link,'real')
#    return bjson_links, runtime_a, runtime_u
    end=time.time()
    print(end-start)
    

'''
#call VRS

myjson = {"message": {"attachmentName":filename,"attachmentType":"video","attachmentFormat":format_out,"attachmentWidth":width,"attachmentHeight":height,"attachmentFrameRateFPS":fps,"URL":link, "attachmentTimeStampUTC":timestamp}}



   
mystr = json.dumps(myjson)
s = socket.socket()
s.connect(("160.40.49.111",9997))
s.send(mystr.encode())
msg = s.recv(1024)
print("VRS says:", msg.decode())
msg = s.recv(1024)
print("VRS says:", msg.decode())
mystr = "Msg from VRS received"
s.send(mystr.encode())



'''







#  From here it's rubbish







'''
fourcc = cv2.VideoWriter_fourcc(*'MPEG')           
        writer = cv2.VideoWriter(os.path.join(RESULTS_PATH+'/output.'+format_out),fourcc, 1.0, (width,height))  #na to allaksw. Na valw height kai width
           
        for i in range(to_write.shape[0]):
            write_img=cv2.cvtColor(to_write[i], cv2.COLOR_RGB2BGR)
            writer.write(write_img)
            
        writer.release()
        


'''



'''


import numpy as np
import cv2

stream  = cv2.VideoCapture('rtmp://195.31.128.29:8080/1')




while True:

    r, f = stream.read()
    print(f.size)
    cv2.imshow('IP Camera stream',f)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
'''