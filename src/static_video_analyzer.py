#ONly the first frame will be analyzed
import numpy as np
import json   
import cv2
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import io
import os
import skvideo.io
import send_topic
import requests
from PIL import Image
import uuid

import urllib.request

real_sensor_thresholds=[3.0,4.6,5.4]
real_rod_thresholds=[3.12,4.72,5.52]

#modified thresholds
mockup_sensor_thresholds=[1.9,3.0,3.8]
mockup_rod_thresholds=[2.02,3.12,4.01]



def calculate_ydiff(mask,img,threshold):
    #How to find co-ordinates of lowest pixel in thresholded image

    # Generate random data
    #img = 10000 * np.random.rand(10, 10)
    #print(img.shape)
    # Find indices where the condition is met
    indices = np.where(mask > threshold)

    if indices[0].size==0:
        print('Empty indices')
        mask = cv2.Canny(img,300,100,apertureSize = 3)
        indices = np.where(mask > 0)
        #input("Press Enter to continue...")
        if indices[0].size==0:
            #input("Press Enter to continue...")
            mask = cv2.Canny(img,300,50,apertureSize = 3)
            indices = np.where(mask > 0)
            if indices[0].size==0:
                #input("Press Enter to continue...")
                mask = cv2.Canny(img,300,10,apertureSize = 3)
                indices = np.where(mask > 0)
                if indices[0].size==0:
                    #input("Press Enter to continue...")
                    mask = cv2.Canny(img,100,50,apertureSize = 3)
                    indices = np.where(mask > 0)
                    if indices[0].size==0:
                        #input("Press Enter to continue...")
                        mask = cv2.Canny(img,50,50,apertureSize = 3)
                        indices = np.where(mask > 0)


    
    #print(indices)
    #max_ind=0
    #for i,y in enumerate(indices[0]):#indices[0] contains y values
    #    if y>max_ind:
    #        max_ind=y
    #        pid=i
    #highest_p=(indices[0][pid],indices[1][pid])
    #lowest_p=[0,0]
    
    
    ymin=min(indices[0])
    ymax=max(indices[0])
    ydiff=ymax-ymin+1
    
    print(ydiff)
    #print(len(indices))
    ## sort by y first then x
    #sorted_indices = sorted((tpl for tpl in zip(*indices)), 
    #                    key=lambda x: (x[1], x[0]))
    #print(len(sorted_indices))
    #highest_p = sorted_indices[0]
    #lowest_p = sorted_indices[-1]
    return ydiff, mask
    





def calibrate_camera():
    #fps, width, height, frames = load_video('ponte1.mp4')
    #metadata = skvideo.io.ffprobe('bacchiglione.20160229_091951_part1.mp4')
    sequence = skvideo.io.vreader('ponte1.webm')#ponte1 is the beggining of bacchiglione.20160229_091951
    frames = []
    for f in sequence:
        frames += [f]


    frame_np = frames[0]
   # print(frame_np.shape)
    #values=frame_np[100][400][0]
    #print(values)
    frames=None

    #    write_on = frame_np.copy()
    height = frame_np.shape[0]
    width = frame_np.shape[1]
    
    
    
    
    
    #img = cv2.imread('./frames/image0.jpg',0)


    values=frame_np[134:206,474:497,0:3]#[481,134,15,57]
    #values.shape
    #print(values)
    #values = values.reshape((57*14,3))
    #values.shape
    #print(values)


    gray = cv2.cvtColor(values,cv2.COLOR_BGR2GRAY)

    #thresh=[50,100,150,200]
    #edges = cv2.Canny(values,100,200)
    edges = cv2.Canny(gray,300,150,apertureSize = 3)

    ydiff,edges=calculate_ydiff(edges,gray,0)
    print(ydiff)
    #print(highest_p)
    #gray[res1]=(255)
    #print(edges.all)
    #max(edges)

   


    
    
    plt.subplot(121),plt.imshow(gray,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.plot(122),plt.imshow(edges)
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    plt.show()
   
    
   
    
    
    
    #rod_length=abs(highest_p[0]-lowest_p[0])
    #print(rod_length)

    #The whole Rod~=5m
    #This is wrong
    #At ponte1.mp4: Sensor=4.06m, so Rod=4.18m (+0.12m). Rodmax=5.86m. Resolution is 360*640. 
    #So, the visual part of the rod in this picture is 5.86-4.18=1.68m.
    #So ydiff corresponds to 1.68m in reality
    #This means that one distance of Y corresponds to X=Y*(1.68/ydiff)
    
    #This is right:
    #At ponte1.mp4: Sensor~=3.33m, so Rod=3.45m (+0.12m). Rodmax=5.86m. Resolution is 360*640. 
    #So, the visual part of the rod in this picture is 5.86-3.45=2.41m.
    #So ydiff  corresponds to 2.41m in reality
    #This means that one distance of Y corresponds to X=Y*(2.41/ydiff)
    
    
    coeff=2.41/ydiff

    
    return coeff




def calculate_water_level(frame_np,coeff):
    #fps, width, height, frames = load_video('ponte1.mp4')
    #metadata = skvideo.io.ffprobe('bacchiglione.20160229_091951_part1.mp4')
    #sequence = skvideo.io.vreader('ponte1.webm')#ponte1 is the beggining of bacchiglione.20160229_091951
    #frames = []
    #for f in sequence:
    #    frames += [f]


    #frame_np = frames[0]
    #print(frame_np.shape)
    #values=frame_np[100][400][0]
    #print(values)
    #frames=None

    #    write_on = frame_np.copy()
    #height = frame_np.shape[0]
    #width = frame_np.shape[1]
    
    
    
    
    
    #img = cv2.imread('./frames/image0.jpg',0)


   # values=frame_np[134:206,474:497]#[481,134,15,57]
    
    min_y=134
    max_y=230
    min_x=474
    max_x=497
    values=frame_np[min_y:max_y,min_x:max_x]#[481,134,15,57]

    #values.shape
    #print(values)
    #values = values.reshape((57*14,3))
    #values.shape
    #print(values)


    #gray = cv2.cvtColor(values,cv2.COLOR_BGR2GRAY)
    gray=values
    #thresh=[50,100,150,200]
    #edges = cv2.Canny(values,100,200)
    
    edges = cv2.Canny(gray,300,140,apertureSize = 3)
   # print(edges.size)
   # if edges.size==0: #if edges is empty
   #     print('Edges is empty')
   #     edges = cv2.Canny(gray,300,120,apertureSize = 3)
        
    ydiff,edges=calculate_ydiff(edges,gray,0)
    print(ydiff)
    #print(lowest_p)
    #print(highest_p)
    #gray[res1]=(255)
    #print(edges.all)
    #max(edges)

   

    #    rod_length=abs(highest_p[0]-lowest_p[0])
    rod_length=ydiff
    real_length=rod_length*coeff
    water_level=5.86-real_length
   # print(water_level)


    
           
    #water_level=np.random.random_sample()*6
    #water_level=round(water_level,1)
    water_level_sensor=round(water_level-0.12,1)
    water_level=round(water_level,1)
    
    print('Water level (Rod)='+str(water_level)+'m')
    print('Water level (Sensor)='+str(water_level_sensor)+'m')
    
       
    
    
    plt.imshow(frame_np)
    plt.axis('off')
    if water_level_sensor<sensor_thresholds[0]:
        alert=0
        severity="Minor"
        plt.suptitle('Water Level= '+str(water_level_sensor)+'m', fontsize=14,color='black')
    if water_level_sensor>=sensor_thresholds[0]:
        alert=1
        severity="Moderate"
        #plt.suptitle('Alert: 1st threshold exceeded (Water Level= '+str(water_level_sensor)+'m)', fontsize=14,color='orange')
        plt.suptitle('Alert: 1st threshold exceeded!', fontsize=14,color='orange')
    if water_level_sensor>=sensor_thresholds[1]:
        alert=2
        severity="Severe"
        #color='red'
        #plt.suptitle('Alert: 2nd threshold exceeded (Water Level= '+str(water_level_sensor)+'m)', fontsize=14,color='red')        
        plt.suptitle('Alert: 2nd threshold exceeded!', fontsize=14,color='red')        

    if water_level_sensor>=sensor_thresholds[2]:
        alert=3
        severity="Extreme"
        #color='red'
        #plt.suptitle('Alert: 3rd threshold exceeded. River overtopping! (Water Level= '+str(water_level_sensor)+'m)',color='red')      
        plt.suptitle('Alert: 3rd threshold exceeded!',color='red')      

    plt.show()
    plt.savefig("output.jpg")
    plt.close()
    
    
    
    
    
    
    
    plt.subplot(121),plt.imshow(gray,cmap = 'gray')
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    #plt.text(0.5, 0.5, 'matplotlib', horizontalalignment='center',
    #      verticalalignment='center', transform=ax.transAxes)
   # plt.figtext(1, 1, 'Hello', fontsize=14)
   # plt.suptitle('Water Level:      '+str(round(water_level,2)-0.12)+'m', fontsize=14)
      
    plt.show()
    plt.close()
#    plt.savefig('myfig')
    #plt.savefig("foo.png")
   
    
    print(alert)
    print(severity) 
    
    
 
    
    
     
        
    return rod_length, real_length, water_level,water_level_sensor, alert, severity

    


    
    
    
    
    
    
    
    

def analyze(frames, width, height, fps, storage_link,file_name, timestamp,thresh_flag):
    global sensor_thresholds, rod_thresholds 
    if thresh_flag=='real':
        sensor_thresholds=real_sensor_thresholds
        rod_thresholds=real_rod_thresholds
    else:
        sensor_thresholds=mockup_sensor_thresholds
        rod_thresholds=mockup_rod_thresholds
        
    
    
    
#  I work with 720p (1280×720). If it has different resolution it will be converted               
# bbx at 13:00:  [481,134,15,57]

#   for idf, f in enumerate(tqdm(frames)):
       #frame = Image.open(image_path)
       # the array based representation of the image will be used later in order to prepare the
       # result image with boxes and labels on it.
    frame_np = frames[0]
    #print(frame_np.size)
    #values=frame_np[0:2][0:2]
    #print(values)
    #frames=None

#    write_on = frame_np.copy()
    height = frame_np.shape[0]
    width = frame_np.shape[1]
    
    coeff=0.04228070175438597
    #coeff was estimated once, by using this function:  coeff=calibrate_camera()
    #print(coeff)

    #testing image
    #frame_np = cv2.imread('./frames2/image0.jpg',cv2.IMREAD_GRAYSCALE)#bacchiglione.20160229_130015_part1.mp4 (Rod length: 4.18m)
    #frame_np[134:206,474:497]
    #print(frame_np.shape)
    rod_length, real_length, water_level,water_level_sensor, alert, severity=calculate_water_level(frame_np,coeff)
   # print('Water level: '+str(water_level)+'m')
   # print('Rod length in pixels: '+str(rod_length)+'p')
   # print('Real Rod length: '+str(real_length)+'m')
    

    
    
    #“Extreme” - Extraordinary threat to life or property; “Severe” - Significant threat to life or property; “Moderate” - Possible threat to life or property; “Minor” – Minimal to no known threat to life or property; “Unknown” - Severity unknown. 
    
    
    
    
    if alert==0:
        print('Streaming video was analyzed. Water level below thresholds')
    if alert>0:
        img_timestamp=timestamp
        img_filename=str(file_name.split(sep='.', maxsplit=1)[0]+'_output.jpeg')
        print(img_filename)
        img_URL=storage_link+'/'+img_filename
        print(img_URL)
        
        
        #    bvid_output = open('./output/'+file_name+'_output.mp4', 'rb')
        
        #to_write = Image.fromarray(frame_np)
        #to_write.save('output.jpg')
        bimg_output = open('output.jpg', 'rb')
        #to_write.close
        r = requests.post(img_URL,bimg_output,headers = {'Content-Type':"image/jpeg"})
            
        if not r.ok:
            print('Image was not uploaded')
            img_URL=""

            
            
        inc_id = 'INC_VRS_'+uuid.uuid4().hex    
        topic=send_topic.send_alert(water_level_sensor,alert,severity,img_filename,img_timestamp,img_URL,inc_id)
        print(topic)
        
        vid_filename=file_name
        vid_URL=storage_link+'/'+vid_filename
        vid_timestamp=timestamp
        topic=send_topic.send_update(water_level_sensor,alert,severity,vid_filename,vid_timestamp,vid_URL,inc_id)
        print(topic)
        

    
