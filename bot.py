'''
Name:        UniCrawler 
Version:     v0.1
Developers:  Andrea Chelini and Davide Frageri
Date:        20/11/2021
'''

from time import sleep
from pytz import timezone
from fetchers import fetch_calendar, fetch_news
import telegram

# Sistema il problema dei certificati
import ssl
if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

cet = timezone('CET')


# CHAT_ID = "@unitnmatematica"
CHAT_ID = "@rappmateunitn"

def bot():
	tg = telegram.TgMsg()
	while True:
		news = fetch_news(["ateneo","dmath"]) # metti sempre ateneo come primo elemento
		events = fetch_calendar(["dmath"])
		for n in news:
			tg.send_message(telegram.newsToMsg(n), CHAT_ID)
			sleep(5)
		for e in events:
			tg.send_message(telegram.eventToMsg(e), CHAT_ID)
			sleep(5)
		print(f"Fetched {len(news)} fresh news and {len(events)} cold events..")
		sleep(3600)

def main():
  print("Starting bot...")
  bot()

if __name__ == "__main__":
    main()
