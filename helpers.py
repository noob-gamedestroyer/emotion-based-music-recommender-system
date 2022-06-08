import spotipy
import time
import configparser
from IPython.display import clear_output
from spotipy import SpotifyClientCredentials, util

config = configparser.ConfigParser()
config.read('application.properties')

client_id = config.get("SpotifyCredentials", "client_id")
client_secret = config.get("SpotifyCredentials", "client_secret")
redirect_uri = config.get("SpotifyCredentials", "redirect_uri")
username = config.get("SpotifyCredentials", "username")
scope = 'playlist-modify-public'

# Credentials to access the Spotify Music Data
manager = SpotifyClientCredentials(client_id, client_secret)
sp = spotipy.Spotify(client_credentials_manager=manager)

# Credentials to access to  the Spotify User's Playlist, Favorite Songs, etc.
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
spt = spotipy.Spotify(auth=token)


def get_albums_id(ids):
    album_ids = []
    results = sp.artist_albums(ids)
    for album in results['items']:
        album_ids.append(album['id'])
    return album_ids


def get_album_songs_id(ids):
    song_ids = []
    results = sp.album_tracks(ids, offset=0)
    for songs in results['items']:
        song_ids.append(songs['id'])
    return song_ids


def get_songs_features(ids):
    meta = sp.track(ids)
    features = sp.audio_features(ids)

    # meta
    name = meta['name']
    album = meta['album']['name']
    artist = meta['album']['artists'][0]['name']
    release_date = meta['album']['release_date']
    length = meta['duration_ms']
    popularity = meta['popularity']
    ids = meta['id']

    # features
    acousticness = features[0]['acousticness']
    danceability = features[0]['danceability']
    energy = features[0]['energy']
    instrumentalness = features[0]['instrumentalness']
    liveness = features[0]['liveness']
    valence = features[0]['valence']
    loudness = features[0]['loudness']
    speechiness = features[0]['speechiness']
    tempo = features[0]['tempo']
    key = features[0]['key']
    time_signature = features[0]['time_signature']

    track = [name, album, artist, ids, release_date, popularity, length, danceability, acousticness,
             energy, instrumentalness, liveness, valence, loudness, speechiness, tempo, key, time_signature]
    columns = ['name', 'album', 'artist', 'id', 'release_date', 'popularity', 'length', 'danceability', 'acousticness',
               'energy', 'instrumentalness',
               'liveness', 'valence', 'loudness', 'speechiness', 'tempo', 'key', 'time_signature']
    return track, columns


def get_songs_artist_ids_playlist(ids):
    playlist = sp.playlist_tracks(ids)
    songs_id = []
    artists_id = []
    for result in playlist['items']:
        songs_id.append(result['track']['id'])
        for artist in result['track']['artists']:
            artists_id.append(artist['id'])
    return songs_id, artists_id


def download_albums(music_id, artist=False):
    if artist == True:
        ids_album = get_albums_id(music_id)
    else:
        if type(music_id) == list:
            ids_album = music_id
        elif type(music_id) == str:
            ids_album = list([music_id])

    tracks = []
    for ids in ids_album:
        # Obtain Ids contained in album
        song_ids = get_album_songs_id(ids=ids)
        # Obtain features contained in album
        ids2 = song_ids

        print(f"Album Length: {len(song_ids)}")

        time.sleep(.6)
        track, columns = get_songs_features(ids2)
        tracks.append(track)

        print(f"Song Added: {track[0]} By {track[2]} from the album {track[1]}")
        clear_output(wait=True)

    clear_output(wait=True)
    print("Music Downloaded!")

    return tracks, columns


def download_playlist(id_playlist, n_songs):
    songs_id = []
    tracks = []

    for i in range(0, n_songs, 100):
        playlist = spt.playlist_items(id_playlist, limit=100, offset=i)

        for songs in playlist['items']:
            songs_id.append(songs['track']['id'])

    counter = 1
    for ids in songs_id:
        time.sleep(.6)
        track, columns = get_songs_features(ids)
        tracks.append(track)

        print(f"Song {counter} Added:")
        print(f"{track[0]} By {track[2]} from the album {track[1]}")
        clear_output(wait=True)
        counter += 1

    clear_output(wait=True)
    print("Music Downloaded!")

    return tracks, columns


def recommend_default_emotion_songs(str_emotion):
    seed_tra_dic = {
        'Happy': [
            '27NovPIUIRrOZoCHxABJwK',  # industry baby - lil nas
            '2CEgGE6aESpnmtfiZwYlbV',  # dynamite - taio
            '0HPD5WQqrq7wPWR7P7Dw1i',  # tik tok - kesha
            '2LEF1A8DOZ9wRYikWgVlZ8',  # good feeling - flo rida
            '0ct6r3EGTcMLPtrXHDvVjc',  # the nights - avicii
        ],
        'Sad': [
            '3S8jK1mGzQi24ilFb45DAZ',  # lonely - JB
            '7smPGXPTC7rfvvYBs624hl',  # home - mike posner
            '2TIlqbIneP0ZY1O0EzYLlc',  # someone you loved - lewis
            '7ekZl2me2Fjn6ywN16cvFK',  # memories
            '779UN3kabApm2zfqX549vf',  # when was it over
        ],
        'Energetic': [
            '3EtyEzMpfKSaoVhPunvbRV',  # leave me alone - NF
            '7Cq27Qc3WRyQ3ddwVslpVZ',  # heart attack - scarlord
            '6LNoArVBBVZzUTUiAX2aKO',  # off the grid - kanye
            '7hdw5gAGMyyn9z0XgfTv1j',  # no name - nf
        ],
        'Calm': []
    }
    return seed_tra_dic[str_emotion]


def spotify_recommend():
    emotion_str = 'Happy'  # TODO: get a emotion as string from Emotion recognition model
    seed_tra = recommend_default_emotion_songs(emotion_str)
    rec = sp.recommendations(seed_tracks=seed_tra, limit=10)
    id_list = [rec['tracks'][i]['id'] for i in range(len(rec['tracks']))]
    return id_list
