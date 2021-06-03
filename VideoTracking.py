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


api_key = 'AIzaSyBvMnwW7NClOkJici-WJAfVFuPusFqlRxw'
youtube = build('youtube', 'v3', developerKey=api_key)
api_key2 = 'AIzaSyBYqe5QINxeNg0tf5BEzh4ngzwBiDloDlI'
youtube2 = build('youtube', 'v3', developerKey=api_key2)


# In[10]:


part=["id","snippet","contentDetails","statistics","status"]
while True:
    try:
        with open('videosData.json') as json_file:
            videosData=[]
            for line in json_file:
                videosData.append(json.loads(line))
    except:
        videosData=[]

    with open('videos.json') as json_file:
        videosJ=[]
        for line in json_file:
            videosJ.append(json.loads(line))
            
    with open('channels_metadata.json') as json_file:
        channels=[]
        for line in json_file:
            channels.append(json.loads(line))


    # In[11]:


    US=set()
    BR=set()
    Other=set()
    for i in channels:
        try:
            i['id']
            try:
                if i['country']=='BR':
                    BR.add(i['id'])
                elif i['country']=='US':
                    US.add(i['id'])
                else:
                    Other.add(i['id'])
            except:
                Other.add(i['id'])
        except:
            pass
    BR=list(BR)
    US=list(US)
    Other=list(Other)


    # In[12]:


    day=date.today()
    if(date.today().weekday()==0):#adiciona possiveis novos videos sobre vacinas toda segunda
        lastupdate = datetime.utcnow()-timedelta(days=7)#ultimo update foi há uma semana
        lastupdate=lastupdate.isoformat("T") + "Z"
        queries=[]
        count=0
        for i in US[0:round(len(US)/2)]:#Busca videos para os estados unidos
            print('Buscando novo video US ',count+1,' de', round(len(US)/2))
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=i,publishedAfter=lastupdate)
            query=request.execute()
            queries.append(query)
            count+=1
        count=0
        queriesBR=[]
        for j in BR[:round(len(BR)/2)]:#Busca videos para o brasil
            print('Buscando novo video BR ',count+1,' de', round(len(BR)/2))
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=j,publishedAfter=lastupdate)
            query=request.execute()
            queriesBR.append(query)
            count+=1
        queriesOther=[]
        for k in Others[:round(len(Others)/2)]:
            print('Buscando novo video país indefinido ',count+1,' de', round(len(Others)/2))
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=k,publishedAfter=lastupdate)
            query=request.execute()
            queriesOther.append(query)
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=k,publishedAfter=lastupdate)
            query=request.execute()
            queriesOther.append(query)
            count+=1
        newvids=0
        for j in queries: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='US'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesBR: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='BR'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesOther: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='Other'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        print(newvids,' new videos found')
    if(date.today().weekday()==1):#adiciona possiveis novos videos sobre vacinas toda terça
        lastupdate = datetime.utcnow()-timedelta(days=7)#ultimo update foi há uma semana
        lastupdate=lastupdate.isoformat("T") + "Z"
        queries=[]
        count=0
        for i in US[round(len(US)/2):]:#Busca videos para os estados unidos
            print('Buscando novo video US ',count+1,' de', round(len(US)/2))
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=i,publishedAfter=lastupdate)
            query=request.execute()
            queries.append(query)
            count+=1
        queriesBR=[]
        count=0
        for j in BR[round(len(BR)/2):]:#Busca videos para o brasil
            print('Buscando novo video BR ',count+1,' de', round(len(BR)/2))
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=j,publishedAfter=lastupdate)
            query=request.execute()
            queriesBR.append(query)
            count+=1
        queriesOther=[]
        for k in Others[round(len(Others)/2):]:
            print('Buscando novo video país indefinido ',count+1,' de', round(len(Others)/2))
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=k,publishedAfter=lastupdate)
            query=request.execute()
            queriesOther.append(query)
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=k,publishedAfter=lastupdate)
            query=request.execute()
            queriesOther.append(query)
            count+=1
        newvids=0
        for j in queries: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='US'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesBR: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='BR'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesOther: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    newvid={}
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='Other'
                    videosJ.append(newvid)
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        print(newvids,' new videos found')


    # In[14]:


    for l in range(len(videosJ)):
        print('Video ',l+1,' de ',len(videosJ))
        checked=False     
        k=videosJ[l]['video']
        for j in range(len(videosData)-1,-1,-1):
            if day.strftime("%d/%m/%y") == videosData[j]['Date']:
                if k==videosData[j]['Video_Id']:
                    checked=True
            else:
                break
        if not checked:
            Vreq=youtube2.videos().list(part=part,id=k)
            Vquery=Vreq.execute()
            dic={}
            rm={}
            if len(Vquery['items'])==0: #se a busca não encontrar nenhum video com o id pesquisado
                for i in range(len(videosData)-1,-1,-1):
                    if videosData[i]['Video_Id']==k:
                        if videosData[i]['Data']!='Video was removed':
                            dic['Date']=day.strftime("%d/%m/%y")
                            dic['Video_Id']=k
                            dic['Data']='Video was removed'#marque como removido esse dia
                            with open('videosData.json','a') as file:#salvando a query
                                write_document_to_file(dic,file)
                            rm['VideoId']=k#adicione aos videos removidos
                            rm['RemovalDate']=day.strftime("%d/%m/%y")#adicione a data aos videos removidos
                            for t in videosJ:
                                if t['video']==k:
                                    rm['Channel']=t['channel']
                                    break
                            with open('removedVideos.json','a') as file2:#salvando o video removido
                                write_document_to_file(rm,file2)
                        break

            else:#se lenght da query>0
                for j in Vquery['items']:#adicione os dados normalmente 
                    dic['Date']=day.strftime("%d/%m/%y")
                    dic['Video_Id']=k
                    dic['Data']=Vquery
                    with open('videosData.json','a') as file:#salvando a query
                        write_document_to_file(dic,file)
    time.sleep(86400)