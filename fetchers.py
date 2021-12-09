from pathlib import Path
import typing
from bs4 import BeautifulSoup
import feedparser
import requests
import pytz
import inspect
import json
from time import sleep

cet = pytz.timezone('CET')

'''
Base class of fetched objects, contains the general __init__ that can convert 
a dict in any of the sub class
'''
class FetchedObj:
    def __init__(self, obj : dict):
        for key in obj.keys():
            setattr(self,key,obj[key])

    def __str__(self):
        return ""
    
    def to_log(self) -> dict:
        attributes = inspect.getmembers(type(self), lambda a:not(inspect.isroutine(a)))
        attributes = attributes[0][1].keys()
        log = {}
        for attr in attributes:
            log[attr] = getattr(self,attr)
        return log

'''
Class of the news objects, can store the values of the news obj fetched
'''
class News(FetchedObj):
    content : str
    category : str
    

'''
Class of the Event objects, can store the values of the calendar events
'''
class Event(FetchedObj):
    day : str
    date : str
    title : str
    url : str

'''
Pull all the cached objects and dinamically create a list of the typed object
'''
def get_cached_objs(type_obj : str) -> typing.List[FetchedObj]:
    # Controllo se il file di log esiste
    fle = Path(f'cache/cached_{type_obj}.json')
    fle.touch(exist_ok=True) # se non esiste creo il file
    cached_objs = []

    with open(f'cache/cached_{type_obj}.json') as f:
        body = f.read()
        if len(body) != 0:
            objs_dict = json.loads(body)
            for obj in objs_dict:
                cached_objs.append(eval(type_obj)(obj))

    return cached_objs

'''
Add object to the corrisponding cache file
'''
def add_cache_objs(previous_obj : typing.List[FetchedObj], new_objs : typing.List[FetchedObj]):
    logs = []
    for obj in previous_obj:
        logs.append(obj.to_log())
    for obj in new_objs:
        logs.append(obj.to_log())
    with open(f'cache/cached_{type(new_objs[0]).__name__}.json', 'w') as f:
        f.write(json.dumps(logs,indent=2, sort_keys=True))

'''
Fetcher of the Event obj, is responsable for the retriving of the information about 
events of specific dipartiments
'''
def fetch_calendar( tags : typing.List[str] ) -> typing.List[Event]:
    cached_activities = get_cached_objs(Event.__name__)
    events = []
    for tag in tags:
        url = f"https://webmagazine.unitn.it/calendario/{tag}"
        while(True):
            html = requests.get(url).text
            soup = BeautifulSoup(html, 'html.parser')
            activities = soup.find_all("td")
            for activity in activities:
                cards = activity.find_all("div",{"class","cal-ateneo-visible"})
                if cards == None:
                    continue
                for card in cards:
                    title = card.find('p').get_text()
                    image = card.find('a').get('href')
                    day = activity.get('headers')[0]
                    date = activity.get('data-date')
                    #voglio aggiungere le news che non sono presenti nella cache
                    if len([x for x in cached_activities if(x.date==date and x.title==title)])==0:
                        events.append(Event({"day":day,"date":date,"title":title,"url":image}))
            sleep(0.5)
            # se il marker non esiste, vuol dire che non possiamo accedere alla pagina successiva
            marker = soup.find('li',{"class","date-next"})
            if marker==None:
                break
            # il marker contiene il link relativo alla pagina successiva, lo immagazino per accedere alla pagina corretta
            url = marker.find('a').get('href')
    if len(events)>0:
        add_cache_objs(cached_activities,events)
    if len(cached_activities)==0:
        return []
    return events

'''
Fetcher of the News obj, is responsable for the retriving of the information about 
news of specific dipartiments
'''
def fetch_news( tags : typing.List[str] ) -> typing.List[News] :
    cached_news = get_cached_objs(News.__name__)
    news = []
    # Leggo tutti i post pubblicati sui tag inseriti
    for tag in tags:
        feed = feedparser.parse(f"https://webmagazine.unitn.it/rss/{tag}/news.xml")
        entries = iter(feed.entries)
        for entry in entries:
            #voglio stampare solo le news che non sono nella cache o sono state fetchate precedentemente
            if len([x for x in news if(x.content['title']==entry['title'] and x.content['published']==entry['published'])])==0:
                if len([x for x in cached_news if(x.content['title']==entry['title'] and x.content['published']==entry['published'])])==0:
                    news.append(News({"category":tag.upper(),"content":entry}))

    if len(news)>0:
        add_cache_objs(cached_news,news)
    if len(cached_news)==0:
        return []
    return news
