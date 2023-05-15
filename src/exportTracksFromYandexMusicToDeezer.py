import sys
from src.export_music import export_music_from_yandex
from src.import_music import import_music_to_deezer
from src.print_table import print_table

if __name__ == '__main__':
    # please, check out README file to find info how to get your tokens
    yandexToken = input('Insert your Yandex Token (check out README for more details)\n')
    deezerToken = input('Insert your Deezer Token (check out README for more details)\n')

    # export liked tracks and playlists from Yandex Music
    yandexCollections, yandexLikedTracks = export_music_from_yandex(yandexToken)

    if len(yandexCollections) > 0 or len(yandexLikedTracks) > 0:
        print('### Yandex Music is collected. Trying to transfer it to Deezer... ###\n')
    else:
        print('### No tracks were collected ###\n')
        sys.exit()

    badTracks = import_music_to_deezer(deezerToken, yandexCollections, yandexLikedTracks)

    if len(badTracks) > 0:
        print_table(badTracks)


