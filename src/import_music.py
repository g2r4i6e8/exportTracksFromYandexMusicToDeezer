import sys
import requests
import tqdm


def import_music_to_deezer(deezerToken, yandexCollections, yandexLikedTracks):
    """
    The objective of the function is to import music from Yandex to Deezer.
    The function takes Yandex collections and liked tracks as inputs and searches for the corresponding tracks in Deezer.
    It then creates playlists in Deezer and adds the found tracks to them.
    The function also allows the user to like the found tracks in Deezer.

    :param deezerToken:  access token for Deezer API
    :param yandexCollections: a dictionary containing Yandex collections as keys and a list of tracks in each collection as values
    :param yandexLikedTracks: a list of tracks liked by the user in Yandex
    :return: badTracks: a list of tracks that were not found in Deezer
    """

    # get userId
    userId = requests.get('https://api.deezer.com/user/me?access_token={}'.format(deezerToken)).json().get('id')
    if userId is None:
        print('### Incorrect Deezer access token ###')
        sys.exit()

    # build up Deezer request
    def search_deezer(title, artists, album=''):
        url = f'https://api.deezer.com/search?q=track:"{title}" album:"{album}" artist:"{artists}"'
        response = requests.get(url)
        response.raise_for_status()
        data = response.json().get('data', [])
        return data

    # look for track in Deezer based on title, artists' name and album (if available)
    def find_song(track):
        title = track['title']
        artists = track['artists']
        album = track['album']
        data = search_deezer(title, artists, album) or search_deezer(title, artists)
        if not data:
            raise Exception('Not found')
        return data[0].get('id')

    # create playlist in Deezer (take into account that all created playlists are public by default)
    def create_deezer_playlist(userId, deezerToken, playlistName):
        url = f'https://api.deezer.com/user/{userId}/playlists/'
        data = {'access_token': deezerToken, 'title': playlistName}
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()['id']

    # add song to a playlist
    def add_deezer_songs(playlistId, deezerToken, songs):
        url = f'https://api.deezer.com/playlist/{playlistId}/tracks/'
        data = {'access_token': deezerToken, 'songs': ','.join(str(song) for song in songs)}
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    # process all tracks from each playlist
    def process_collection(collectionName, tracks, userId, deezerToken):
        print(f'### Looking for songs to add in playlist "{collectionName}" ###')
        playlistId = create_deezer_playlist(userId, deezerToken, collectionName)
        songs = []
        bad_tracks = []
        for track in tqdm.tqdm(tracks, leave=True):
            try:
                songId = find_song(track)
                songs.append(songId)
            except Exception:
                track['collection'] = collectionName
                bad_tracks.append(track)
        add_deezer_songs(playlistId, deezerToken, songs)
        print(f'\n### Songs added to playlist "{collectionName}" successfully ###\n')
        return badTracks

    # like a found song in Deezer
    def like_song(userId, songId, deezerToken):
        url = f'https://api.deezer.com/user/{userId}/tracks/'
        data = {'access_token': deezerToken, 'track_id': songId}
        response = requests.post(url, data=data)
        response.raise_for_status()
        return response.json()

    # process all liked tracks
    def process_liked_collection(tracks, userId, deezerToken):
        print('### Looking for songs to like ###')
        bad_tracks = []
        for track in tqdm.tqdm(tracks, leave=True):
            try:
                songId = find_song(track)
            except Exception:
                track['collection'] = 'Liked'
                bad_tracks.append(track)
        like_song(userId, songId, deezerToken) or badTracks.append(track)
        return badTracks

    badTracks = []

    # iterate over playlists and import data to Deezer
    if len(yandexCollections) > 0:
        for collectionName, tracks in yandexCollections.items():
            badTracks += process_collection(collectionName, tracks, userId, deezerToken)

    # iterate over Liked and import data to Deezer
    if len(yandexLikedTracks) > 0:
        badTracks += process_liked_collection(yandexLikedTracks, userId, deezerToken)

    print('\n### Import is  finished! ###')

    return badTracks
