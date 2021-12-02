import requests
import json
import sys

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
        r = requests.get(f"https://api.telegram.org/bot{self.tg_secret}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode=HTML")
        with open('logs.txt', 'a') as f:
            f.write(r.text+"\n")
            print(r.text)

'''
Function responsable for casting an Event obj to a string
'''
def eventToMsg(obj : Event) -> str:
    return '<b>EVENTO</> \n' + obj.title + '\n' + obj.day + ' ' + obj.date + '\n' + obj.url

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
        return '<b>&#35;NEWS</> \n' + content.title + '\n' + content.link + '\n' + content.published
    elif obj.category=="ATENEO":
        return '<b>ATENEO</> \n' + content.title + '\n' + content.link + '\n' + content.published
    return ""
