#!/usr/bin/env python
# coding: utf-8

# In[7]:


from googleapiclient.discovery import build
import json
import pandas as pd
from datetime import date, timedelta,datetime
import numpy as np
import time


# In[8]:


def write_document_to_file(document, file):
    json.dump(document, file)
    file.write("\n")
    file.flush()


# In[9]:


api_key = 'AIzaSyBnHb4QwVnEvg4LHwWnY5ihlaxARZzxmNc'
youtube = build('youtube', 'v3', developerKey=api_key)
api_key2 = 'AIzaSyAbZWYK9EvoiWiqLnx5Ie5fKMlZsfKhMc8'
youtube2 = build('youtube', 'v3', developerKey=api_key2)
api_key3 = 'AIzaSyBYqe5QINxeNg0tf5BEzh4ngzwBiDloDlI'
youtube3 = build('youtube', 'v3', developerKey=api_key3)
api_key4 = 'AIzaSyBD-Epo0MEZmxJu-ZKhDSwWSBmhNSyPjYU'
youtube4 = build('youtube', 'v3', developerKey=api_key4)
api_key5 = 'AIzaSyB7EHy2ZKpfPTY56yRVuu7a8lChfB-IVjw'
youtube5 = build('youtube', 'v3', developerKey=api_key5)

# In[10]:

part=["id","snippet","contentDetails","statistics","status"]
while True:
    change=False
    with open('/princeton_data/source_files/metadata_videos.json') as json_file:
        videosJ=[]
        for line in json_file:
            videosJ.append(json.loads(line))
    
    try:
        with open('/princeton_data/source_files/daily_logging_videos.json') as json_file:
            videosData=[]
            for line in json_file:
                videosData.append(json.loads(line))
    except:
        videosData=[]
    videosData=videosData[-2*(len(videosJ)):]    
    with open('/princeton_data/source_files/removedVideos.json') as json_file:
        allrmvid=[]
        for line in json_file:
            allrmvid.append(json.loads(line))
    # In[12]:
    day=date.today()
    
    print('Buscando ',len(videosJ),' videos')
    for l in range(len(videosJ)):
        checked=False
        try:        
            k=videosJ[l]['video_id']
        except:
            continue
        for j in range(len(videosData)-1,-1,-1):
            if day.strftime('%Y-%m-%d') == videosData[j]['Date']:
                if k==videosData[j]['Video_Id']:
                    checked=True
            else:
                break
        if not checked:
            if l <8000:
                Vreq=youtube.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            elif l<16000:
                Vreq=youtube2.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            elif l <24000:
                Vreq=youtube3.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            else:
                Vreq=youtube4.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            dic={"Date":np.nan,'title':np.nan,"Video_Id":np.nan,"channelId":np.nan,'status':np.nan,"viewCount":np.nan,"likeCount":np.nan,"dislikeCount":np.nan,"favoriteCount":np.nan,"commentCount": np.nan}
            rm={}
            if len(Vquery['items'])==0: #se a busca n??o encontrar nenhum video com o id pesquisado
                exists=False
                for j in range(len(allrmvid)-1,-1,-1):
                    i=allrmvid[j]
                    if i['VideoId']==k and i['back_online']==False:
                        exists=True
                if not exists:
                    rm['VideoId']=k#adicione aos videos removidos
                    for t in videosJ:#encontra canal do video
                        try:
                            if t['video_id']==k:
                                rm['Channel']=t['channel_id']
                                break
                        except:
                            pass
                    rm['RemovalDate']=day.strftime('%Y-%m-%d')#adicione a data aos videos removidos
                    rm['back_online']=False #marca que n??o est?? online
                    allrmvid.append(rm)
                    change=True
                    #with open('/princeton_data/source_files/removedVideos.json','a') as file2:#salvando o video removido
                    #   write_document_to_file(rm,file2)
            else:#se lenght da query>0
                for j in Vquery['items']:#adicione os dados normalmente 
                    dic['Date']=day.strftime('%Y-%m-%d')
                    dic['Video_Id']=k
                    dic['channelId']=Vquery['items'][0]['snippet']['channelId']
                    dic['title']=Vquery['items'][0]['snippet']['title']
                    dic.update(Vquery['items'][0]['statistics'])
                    for i in range(len(allrmvid)):#se o video era anteriormente removido
                        if allrmvid[i]['VideoId']==k:
                            allrmvid[i]['back_online']=True #ele volta a estar online
                            change=True

                    with open('/princeton_data/source_files/daily_logging_videos.json','a') as file:#salvando a query
                        write_document_to_file(dic,file)
    if change:
        with open('/princeton_data/source_files/removedVideos.json','w') as file: #salvando as mudan??as nos removidos
            for document in allrmvid:
                write_document_to_file(document,file)
    print('done ',day)   
    time.sleep(86400)
