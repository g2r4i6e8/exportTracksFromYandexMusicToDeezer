from yandex_music import Client
import tqdm


def export_music_from_yandex(yandexToken):
    """
    The objective of the "export_music_from_yandex" function is to export playlists and liked tracks
    from a Yandex Music account, and collect some track details that will be used to find similar songs in Deezer.

    :param yandexToken: a string representing the Yandex Music token for authentication.
    :return:
    - yandexCollections: a dictionary containing the collected playlists and their tracks' details
    - yandexLikedTracks: a list containing the collected liked tracks and their details.
    """

    # initialize Yandex Music client
    yandexClient = Client(yandexToken).init()

    # fetch playlists (without Liked)
    yandexPlaylists = []
    try:
        yandexPlaylists = yandexClient.users_playlists_list()
    except: pass # probably user do not have playlists

    # collect some track details that will be used to find similar songs in Deezer
    def get_details(fullTrack):
        title = fullTrack.title or ''
        album = fullTrack.albums[0].title if len(fullTrack.albums) > 0 else ''
        artists = ','.join(artist.name for artist in fullTrack.artists) or ''
        return title, album, artists

    # fetch tracks inside each playlist
    # there are TrackShort instances in playlists, but we need title and artists
    yandexCollections = {}
    for yandexPlaylist in yandexPlaylists:
        yandexPlaylistName = yandexPlaylist.title
        print(f'### Playlist "{yandexPlaylistName}" is processing ###')
        yandexPlaylistShortTracks = yandexPlaylist.fetch_tracks()
        playlistTracks = []
        pbar = tqdm.tqdm(yandexPlaylistShortTracks, leave=True)
        for shortTrack in yandexPlaylistShortTracks:
            fullTrack = shortTrack.fetch_track()
            if fullTrack.type != 'music': continue
            title, album, artists = get_details(fullTrack)
            playlistTracks.append({'title': title, 'artists': artists, 'album': album})
            pbar.update(1)
        yandexCollections[yandexPlaylistName] = playlistTracks
        print(f'### Playlist "{yandexPlaylistName}" is collected ###\n')
        pbar.close()

    # fetch liked tracks
    # there are Track instances in Liked playlist so we can parse them as is
    print('### Playlist "Liked" is processing ###')
    yandexLikedTracks = []
    try:
        for fullTrack in yandexClient.users_likes_tracks().fetch_tracks():
            if fullTrack.type != 'music': continue
            title, album, artists = get_details(fullTrack)
            yandexLikedTracks.append({'artists': artists, 'title': title, 'album': album})
        print('### Playlist "Liked" is collected ###\n')
    except: pass

    return yandexCollections, yandexLikedTracks
