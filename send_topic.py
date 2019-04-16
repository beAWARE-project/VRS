import json
import requests
import uuid
import time





def send_alert(water_level,alert,severity,img_filename,img_timestamp,img_URL,inc_id):

    with open('./topic_021_alert.json', mode='r') as file:
        topic = json.load(file)
   
    msg_id = uuid.uuid4().hex
    inc_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


    topic['header']['sender'] = 'CCTV1'#??
    topic['header']['msgIdentifier'] = msg_id#msgIdentifier?
    topic['header']['sentUTC'] = inc_time
   # topic['header']['sentUTC'] = inc_time
    topic['header']['specificSender'] = 'CCTV1'#??


    if alert==1:
        alarm_str='1st'
        Severity='Moderate'
    if alert==2:
        alarm_str='2nd'
        Severity='Severe'
    if alert==3:
        alarm_str='3rd'
        Severity='Extreme'
        
    topic['body']['title'] = str('V.R.S.: Bacchiglione a Vicenza CAE, '+alarm_str+' alarm threshold')
    topic['body']['incidentID'] = inc_id
    topic['body']['startTimeUTC'] = inc_time
    topic['body']['incidentOriginator'] = 'VRS'#??
    topic['body']['incidentType'] = 'CCTV_alert'
    #topic['body']['uri'] = ''#??

    topic['body']['attachments'][0]['attachmentName'] = img_filename
    topic['body']['attachments'][0]['attachmentType'] = 'image'
    topic['body']['attachments'][0]['attachmentTimeStampUTC'] = str(img_timestamp)
    topic['body']['attachments'][0]['attachmentURL'] = img_URL
   
    topic['body']['position']['latitude'] = 45.550171
    topic['body']['position']['longitude'] = 11.550287
  
    topic['body']['description'] = str('Static camera: Bacchiglione a Vicenza CAE,Severity: '+Severity+', Water Level value: '+str(water_level))#??
    # "dataStreamID": "FLCR_1112_OWLm",
    #        "dataSeriesID": "47_167",
    #afta den yparxoun
    alert_for_post = {"topics": ["TOP021_INCIDENT_REPORT"], "message": json.dumps(topic)}

    
    r = requests.post(url='http://160.40.49.112:5003/produce', data=json.dumps(alert_for_post))
    if not r.ok:
        print('Topic 021 was not created')
    print(r)
            
    return topic
        
        
        
        
        
        
def send_update(water_level,alert,severity,vid_filename,vid_timestamp,vid_URL,inc_id):

    with open('./topic_021_media.json', mode='r') as file:
        topic = json.load(file)
    
    msg_id = uuid.uuid4().hex
    inc_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())


    topic['header']['sender'] = 'CCTV1'#??
    topic['header']['msgIdentifier'] = msg_id#msgIdentifier?
    topic['header']['sentUTC'] = inc_time
   # topic['header']['sentUTC'] = inc_time
    topic['header']['specificSender'] = 'CCTV1'#??


    if alert==1:
        alarm_str='1st'
        Severity='Moderate'
    if alert==2:
        alarm_str='2nd'
        Severity='Severe'
    if alert==3:
        alarm_str='3rd'
        Severity='Extreme'
        
    topic['body']['title'] = str('V.R.S.: Bacchiglione a Vicenza CAE, '+alarm_str+' alarm threshold')
    topic['body']['incidentID'] = inc_id
    topic['body']['startTimeUTC'] = inc_time
    topic['body']['incidentOriginator'] = 'VRS'#??
    topic['body']['incidentType'] = 'Traffic'#??
   # topic['body']['uri'] = ''#??

    topic['body']['attachments'][0]['attachmentName'] = vid_filename
    topic['body']['attachments'][0]['attachmentType'] = 'video'
    topic['body']['attachments'][0]['attachmentTimeStampUTC'] = str(vid_timestamp)
    topic['body']['attachments'][0]['attachmentURL'] = vid_URL
   
    topic['body']['position']['latitude'] = 45.550171
    topic['body']['position']['longitude'] = 11.550287
  
    topic['body']['description'] = str('Static camera: Bacchiglione a Vicenza CAE,Severity: '+Severity+', Water Level value: '+str(water_level))#??
    # "dataStreamID": "FLCR_1112_OWLm",
    #        "dataSeriesID": "47_167",
    #afta den yparxoun
    alert_for_post = {"topics": ["TOP021_INCIDENT_REPORT"], "message": json.dumps(topic)}

    
    r = requests.post(url='http://160.40.49.112:5003/produce', data=json.dumps(alert_for_post))
    if not r.ok:
        print('Topic 021 was not created')
    print(r)
            
    return topic
        
        
        
        
        
        
        
#        “Extreme” - Extraordinary threat to life or property; “Severe” - Significant threat to life or property; “Moderate” - Possible threat to life or property; “Minor” – Minimal to no known threat to life or property; “Unknown” - Severity unknown. 