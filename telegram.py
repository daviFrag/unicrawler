import requests
import json
import sys
import urllib

from fetchers import Event, News

class TgMsg:
    tg_secret : str

    def __init__(self) -> None:
        with open('config.json', 'r') as f:
            config = json.loads(f.read())
            if 'telegram' in config.keys():
                telegram_config = config['telegram']
                if 'tg_secret' in telegram_config and telegram_config['tg_secret'] != "":
                    self.tg_secret=telegram_config['tg_secret']
                else:
                    print("Invalid telegram secret!")
                    sys.exit(1)
            else:
                print("Invalid configuration, insert a telegram config in the config.json!")
                sys.exit(1)
            


    def send_message(self, msg : str, chat_id : str):
        r = requests.get(f"https://api.telegram.org/bot{self.tg_secret}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote(msg, safe='')}&parse_mode=HTML")
        with open('logs.txt', 'a') as f:
            f.write(r.text+"\n")
            print(r.text)

'''
Function responsable for casting an Event obj to a string
'''
def eventToMsg(obj : Event) -> str:
    return f"<b>#EVENTO</> \n<b>Titolo: </>{obj.title} \n<b>Data: </>{obj.day} {obj.date} \n<b>Link: </>{obj.url}"

'''
Function responsable for casting a News obj to a string
'''
def newsToMsg(obj : News) -> str:
    content = obj.content
    # match obj.category:
    #     case "DMATH":
    #         return '<b>MATEMATICA news</> \n' + content.title + '\n' + content.link + '\n' + content.published
    #     case "ATENEO":
    #         return  '<b>ATENEO news</> \n' + content.title + '\n' + content.link + '\n' + content.published
    if obj.category=="DMATH":
        return f"<b>#NEWS</> \n<b>Titolo: </>{content.title} \n<b>Link: </>{content.link}"
    elif obj.category=="ATENEO":
        return f"<b>#ATENEO</> \n<b>Titolo: </>{content.title} \n<b>Link: </>{content.link}"
    return ""
