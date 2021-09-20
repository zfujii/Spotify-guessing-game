import os
import sys
import spotipy
import webbrowser
import spotipy.util as util
import random
import threading
from json.decoder import JSONDecodeError

username = sys.argv[1]
scope = 'user-read-private user-read-playback-state user-modify-playback-state'

try:
    token = util.prompt_for_user_token(username, scope)
except (AttributeError, JSONDecodeError):
    os.remove(f".cache-{username}")
    token = util.prompt_for_user_token(username, scope)

spotifyObject = spotipy.Spotify(auth=token)

devices = spotifyObject.devices()
if devices['devices']:
    deviceID = devices['devices'][0]['id']
    # Get track information
    track = spotifyObject.current_user_playing_track()
    if track != None:
        artist = track['item']['artists'][0]['name']
        track = track['item']['name']
        if artist !="":
            print("Currently playing " + artist + " - " + track)
else:
    print("Please start your spotify app so you can listen to the songs!")
    
# User information
user = spotifyObject.current_user()
displayName = user['display_name']

## Mode 1: Artist search - songs from a specific artist
## Mode 2: Featured Playlist - songs from the featured playlists
##
def pause_song():
    spotifyObject.pause_playback(deviceID)
    
while True:
    print()
    print(">>> Welcome to the Spotify Guessing Game " + displayName + "!")
    print()
    print("Type: start - If you want to start the game")
    print("Type: info - If you want to learn how to play")
    print("Type: exit - If you want to exit")
    print()
    choice = input("Enter your choice: ")
    # Start game
    if choice == "start":
        while True:
            print()
            print("Type: artist - If you want random songs from a specific artist")
            print("Type: featured - If you want random songs from the Spotify featured playlists")
            print("Type: exit - If you want to exit")
            print()
            trackSelectionList = []
            gameChoice = input("Enter your choice: ")
            # Search for artist
            if gameChoice == "artist":
                print()
                playerChoice = input("Type the artist's name: ")
                print()
                searchResults = spotifyObject.search(playerChoice,1,0,"artist")
                artist = searchResults['artists']['items'][0]
                artistID = artist['id']
                albumResults = spotifyObject.artist_albums(artistID)
                albumResults = albumResults['items']
                randomAlbum = random.choice(albumResults) #random album
                albumID = randomAlbum['id']
                albumArt = randomAlbum['images'][0]['url']
                trackResults = spotifyObject.album_tracks(albumID)
                trackResults = trackResults['items']
                randomTrack = random.choice(trackResults) #random track from the random album
                trackSelectionList.append(randomTrack['uri'])
                spotifyObject.start_playback(deviceID, None, trackSelectionList)
                print()
                print("Playing a random song from " + artist['name'] + " for 15 seconds")
                print()
                start_time = threading.Timer(15,pause_song)
                start_time.start()
                print()
                playerAnswer = input("Enter your guess: ")
                print()
                if playerAnswer.lower() == randomTrack['name'].lower():
                    print("Correct")
                else:
                    print("Wrong")
                    print("The song playing was: " + randomTrack['name'])
            # Play from featured playlists
            elif gameChoice == "featured":    
                featuredList = spotifyObject.featured_playlists(locale="en_US")
                featuredList = featuredList['playlists']['items']
                for i in featuredList:
                    print(i['name'])
                trackSelectionList.append()
                spotifyObject.start_playback(deviceID, None, trackSelectionList)
            if gameChoice == "exit":
                break
    if choice == "info":
        print()
        print("Please have your spotify application open to play")
        print("The game will choose random songs from an artist or featured playlists")
        print("It will play the beginning for 15 seconds and you have to guess the song!")
        print("Have fun!")
        print()
    # End program
    if choice == "exit":
        break
