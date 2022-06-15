import time
import tweepy
import json
import asyncio
import logging
import spotify
import random
import re
import os
import azlyrics
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
load_dotenv()
consumer_key = os.getenv("TWITTERCONSUMER")
consumer_secret = os.getenv("TWITTERCONSECRET")
access_token = os.getenv("TWITTERACCESS")
access_secret = os.getenv("TWITTERACCSECRET")
spot_client = os.getenv("SPOTIFY")
spot_secret = os.getenv("SPOTIFYSECRET")
playlist_id = "0VQ3cAgmt3nK1SoiIrjon2"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
spot = spotify.HTTPClient(client_id=spot_client, client_secret=spot_secret)


async def scheduled_job():
    global track, artist
    lyrics = None
    while lyrics is None:
        try:
            numTracks = (await spot.get_playlist_tracks(playlist_id=playlist_id, fields="total"))["total"]
            jam = await spot.get_playlist_tracks(playlist_id=playlist_id, limit=100, offset=random.randint(0, numTracks - 101), fields="items(track(name, artists(name)))")
            picker = random.randint(0,98)
            track, artist = jam["items"][picker]["track"]["name"], jam["items"][picker]["track"]["artists"][0]["name"]
            print(f"{track} by {artist} was chosen.")
            lyrics = azlyrics.lyrics(artist, track)
            try:
                test = lyrics[0]
            except KeyError as err:
                print(err)
                print("whoops, time to restart like nothing happen!!")
                lyrics = None
                time.sleep(5)
            else:
                print("all good")
        except Exception as err:
            print(err)
            print("whoops, time to restart like nothing happen!!")
            lyrics = None
            time.sleep(5)
    filtered = ""
    for line in lyrics[0].split("\n") :
        line = re.sub(r'\[[^()]*\]', "", line)
        if line != "" and line != " " and line != "\n":
            filtered += line + "\n"
    lists = filtered.split("\n")
    rand = random.randint(2, len(lists) - 2)
    api.update_status(f"\"{lists[rand - 1]} {lists[rand + 1]}\" on {track} by {artist}.")


if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler()
    scheduler.add_job(trigger="cron", func=scheduled_job, minute=0)
    scheduler.add_job(trigger="cron", func=scheduled_job, minute=30)
    scheduler.start(paused=False)
    try:
        asyncio.get_event_loop().run_forever()
    except:
        pass