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
api_key3 = 'AIzaSyBD-Epo0MEZmxJu-ZKhDSwWSBmhNSyPjYU'
youtube3 = build('youtube', 'v3', developerKey=api_key3)
api_key4 = 'AIzaSyBnHb4QwVnEvg4LHwWnY5ihlaxARZzxmNc'
youtube4 = build('youtube', 'v3', developerKey=api_key4)
api_key5 = 'AIzaSyAbZWYK9EvoiWiqLnx5Ie5fKMlZsfKhMc8'
youtube5 = build('youtube', 'v3', developerKey=api_key5)
covid_keywords = [
    "covid",
    "covid-19",
    "coronavirus",
    "coronav\u00edrus",
    "vaccine",
    "vacina",
    "vaxx",
    "vaccination",
    "vacina\u00e7\u00e3o",
    "corona",
    "pfizer",
    "moderna",
    "janssen",
    "johnson &amp; johnson",
    "johnson & johnson",
    "astrazeneca",
    "biontech",
    "coronavac",
    "butantan",
    "covaxin",
    "oxford",
    "oxford-astrazeneca"
    "sputnik v",
    "gamaleya",
    "cansino",
    "vector institute",
    "novavax",
    "sinopharm",
    "sinovac",
    "sinopharm-wuhan",
    "bharat biotech",
    "tratamento precoce",
    "early treatment",
    "pff2",
    "n95",
    "surgical mask",
    "m\u00e1scara",
    "m\u00e1scara cir\u00fargica",
    "m\u00e1scaras cir\u00fargicas",
    "\u00e1lcool",
    "face mask",
    "mask",
    "cloroquina",
    "ivermectina",
    "ivermectin",
    "hydroxychloroquine",
    "chloroquine"
]
# In[10]:

def check_vaccine(vidId,keywords,NVquery):
    title=NVquery['items'][0]['snippet']['title'].lower()
    description=NVquery['items'][0]['snippet']['description'].lower()
    present_keywords=[]
    for word in keywords:
        if word in title or word in description:
            present_keywords.append(word)
    return present_keywords


part=["id","snippet","contentDetails","statistics","status"]
while True:
    try:
        with open('/home/marcelo/jsons/videosData.json') as json_file:
            videosData=[]
            for line in json_file:
                videosData.append(json.loads(line))
    except:
        videosData=[]

    with open('/home/marcelo/jsons/videos.json') as json_file:
        videosJ=[]
        for line in json_file:
            videosJ.append(json.loads(line))
            
    with open('/home/marcelo/jsons/channels_metadata.json') as json_file:
        channels=[]
        for line in json_file:
            channels.append(json.loads(line))


    # In[11]:

'''
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
'''

    # In[12]:


    day=date.today()
    '''if(date.today().weekday()==0):#adiciona possiveis novos videos sobre vacinas toda segunda
        lastupdate = datetime.utcnow()-timedelta(days=7)#ultimo update foi há uma semana
        lastupdate=lastupdate.isoformat("T") + "Z"
        queries=[]
        count=0
        print('Buscando novos videos US')
        for i in US[0:round(len(US)/2)]:#Busca videos para os estados unidos
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=i,publishedAfter=lastupdate)
            query=request.execute()
            queries.append(query)
            count+=1
        count=0
        queriesBR=[]
        print('Buscando novos videos BR')
        for j in BR[:round(len(BR)/2)]:#Busca videos para o brasil
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=j,publishedAfter=lastupdate)
            query=request.execute()
            queriesBR.append(query)
            count+=1
        queriesOther=[]
        print('Buscando novos videos Outros')
        for k in Other[:round(len(Other)/2)]:
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
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='US'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesBR: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='BR'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesOther: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='Other'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
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
        print('Buscando novos videos US')
        for i in US[round(len(US)/2):]:#Busca videos para os estados unidos
            request = youtube.search().list(q='vaccine',part=['id','snippet'],channelId=i,publishedAfter=lastupdate)
            query=request.execute()
            queries.append(query)
            count+=1
        queriesBR=[]
        count=0
        print('Buscando novos videos BR')
        for j in BR[round(len(BR)/2):]:#Busca videos para o brasil
            request = youtube.search().list(q='vacina',part=['id','snippet'],channelId=j,publishedAfter=lastupdate)
            query=request.execute()
            queriesBR.append(query)
            count+=1
        queriesOther=[]
        print('Buscando novos videos Outros')
        for k in Other[round(len(Other)/2):]:
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
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='US'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesBR: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='BR'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        for j in queriesOther: #adiciona os novos videos aos videos a serem monitorados
            for i in j['items']:
                try:
                    NVreq=youtube2.videos().list(part=part,id=i['id']['videoId'])
                    NVquery=NVreq.execute()
                    newvid={}
                    newvid['keywords']=check_vaccine(i['id']['videoId'],covid_keywords,NVquery)
                    if len(newvid['keywords']) > 0:
                        newvid['vaccine']=True
                    else:
                        newvid['vaccine']=False
                    newvid['date']=day.strftime("%d/%m/%y")
                    newvid['video']=i['id']['videoId']
                    newvid['channel']=i['snippet']['channelId']
                    newvid['country']='Other'
                    videosJ.append(newvid)
                    newvid['data']=NVquery
                    newvids+=1
                    with open('videos.json','a') as file:#salvando a query
                        write_document_to_file(newvid,file)
                except:
                    pass
        print(newvids,' new videos found')'''


    # In[14]:

    print('Buscando ',len(videosJ),' videos')
    for l in range(len(videosJ)):
        checked=False     
        k=videosJ[l]['video']
        for j in range(len(videosData)-1,-1,-1):
            if day.strftime("%d/%m/%y") == videosData[j]['Date']:
                if k==videosData[j]['Video_Id']:
                    checked=True
            else:
                break
        if not checked:
            if l <8000:
                Vreq=youtube2.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            elif l<16000:
                Vreq=youtube3.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            elif l <24000:
                Vreq=youtube5.videos().list(part=part,id=k)
                Vquery=Vreq.execute()
            else:
                Vreq=youtube4.videos().list(part=part,id=k)
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
                            with open('/home/marcelo/jsons/videosData.json','a') as file:#salvando a query
                                write_document_to_file(dic,file)
                            rm['VideoId']=k#adicione aos videos removidos
                            rm['RemovalDate']=day.strftime("%d/%m/%y")#adicione a data aos videos removidos
                            for t in videosJ:
                                if t['video']==k:
                                    rm['Channel']=t['channel']
                                    break
                            with open('/home/marcelo/jsons/removedVideos.json','a') as file2:#salvando o video removido
                                write_document_to_file(rm,file2)
                        break

            else:#se lenght da query>0
                for j in Vquery['items']:#adicione os dados normalmente 
                    dic['Date']=day.strftime("%d/%m/%y")
                    dic['Video_Id']=k
                    dic['channelId']=Vquery['items'][0]['snippet']['channelId']
                    dic['title']=Vquery['items'][0]['snippet']['title']
                    dic['Data']=Vquery['items'][0]['statistics']
                    with open('/home/marcelo/jsons/videosData.json','a') as file:#salvando a query
                        write_document_to_file(dic,file)
    print('done ',day)   
    time.sleep(86400)
