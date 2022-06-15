# jamLyricBot
**A Twitter [bot](https://twitter.com/jam_lyric) that posts lyrics from any given Spotify playlist (or in this case, [this one](https://open.spotify.com/playlist/0VQ3cAgmt3nK1SoiIrjon2))**
## How it works
Using the Spotify, Twitter and AZlyrics API, it will first pull the number of tracks in the playlist, then will grab a random subset of 100 tracks, pick a track, and use grab the lyrics for said track. It will then remove all the \[Chorus\], and \[Verse 1\] tags. It will then pick 2 random lines to post on Twitter.
## Setup
1. Clone repository
2. Make .env file in the root folder like this 
```
TWITTERCONSUMER=
TWITTERCONSECRET=
TWITTERACCESS=
TWITTERACCSECRET=
SPOTIFY=
SPOTIFYSECRET=
```
3. Fill in with your API keys
4. Change playlist ID
5. Run!
## Bugs
Nothing right now - although I do probably need to prettify my code.
