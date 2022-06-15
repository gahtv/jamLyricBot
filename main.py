import asyncio
import logging
import os
from pydoc import plain
import random
import re
import time
import azlyrics
import spotify 
import tweepy 
from apscheduler.schedulers.asyncio import AsyncIOScheduler 
from dotenv import load_dotenv 
load_dotenv()
# Get the API keys from the .env file
consumer_key = os.getenv("TWITTERCONSUMER")
consumer_secret = os.getenv("TWITTERCONSECRET")
access_token = os.getenv("TWITTERACCESS")
access_secret = os.getenv("TWITTERACCSECRET")
spot_client = os.getenv("SPOTIFY")
spot_secret = os.getenv("SPOTIFYSECRET")
# Insert playlist ID here
playlist_id = "0VQ3cAgmt3nK1SoiIrjon2"
# Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)
# Spotify API
spot = spotify.HTTPClient(client_id=spot_client, client_secret=spot_secret)


async def scheduled_job():
    global track, artist
    lyrics = None
    while lyrics is None:
        try:
            numTracks = (await spot.get_playlist_tracks(playlist_id=playlist_id, fields="total"))["total"] # Get the number of tracks from the playlist
            playlist = await spot.get_playlist_tracks(playlist_id=playlist_id, limit=100, offset=random.randint(0, numTracks - 101), fields="items(track(name, artists(name)))") # Get a list of 100 tracks from the playlist
            picker = random.randint(0, 98) # Pick a random track from the list
            track, artist = playlist["items"][picker]["track"]["name"], playlist["items"][picker]["track"]["artists"][0]["name"] # Get the track name and artist name
            print(f"{track} by {artist} was chosen.")
            lyrics = azlyrics.lyrics(artist, track) # Get the lyrics
            try: # If the lyrics are not found, try again
                lyrics[0] # Check if the lyrics are empty
            except KeyError as err:
                print(err)
                print("whoops, time to restart like nothing happen!!")
                lyrics = None # Reset the lyrics
                time.sleep(5) # Wait 5 seconds before trying again
            else:
                print("all good")
        except Exception as err: # If the API call fails, try again
            print(err)
            print("whoops, time to restart like nothing happen!!")
            lyrics = None # Reset the lyrics
            time.sleep(5) # Wait 5 seconds before trying again
    filtered = ""
    for line in lyrics[0].split("\n"): # Filter the lyrics to remove the unnecessary stuff
        line = re.sub(r'\[[^()]*\]', "", line) # Remove the brackets from the lyrics
        if line != "" and line != " " and line != "\n": # Remove the empty lines
            filtered += line + "\n" # Add the line to the filtered lyrics
    lists = filtered.split("\n")
    rand = random.randint(2, len(lists) - 2) # Pick 2 random lines from the lyrics
    api.update_status(f"\"{lists[rand - 1]} {lists[rand + 1]}\" on {track} by {artist}.") # Post the lyrics to Twitter


if __name__ == '__main__':
    logging.basicConfig() # Setup logging
    logging.getLogger('apscheduler').setLevel(logging.DEBUG)
    scheduler = AsyncIOScheduler() # Setup the scheduler
    scheduler.add_job(trigger="cron", func=scheduled_job, minute=0)
    scheduler.add_job(trigger="cron", func=scheduled_job, minute=30)
    scheduler.start(paused=False)
    try:
        asyncio.get_event_loop().run_forever()
    except:
        pass