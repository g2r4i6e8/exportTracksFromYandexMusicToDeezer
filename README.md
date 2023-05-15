# Transfer your tracks from Yandex Music to Deezer

## How to transfer data from Yandex Music to Deezer
1. [Obtain Yandex Music Token](#getting-yandex-music-token)
2. [Obtain Deezer Token](#getting-deezer-token)
3. Launch script to start transferring your playlists from Yandex Music to Deezer
   ```shell
   $ python src/exportTracksFromYandexMusicToDeezer.py
   ```

### Getting Yandex Music Token
1. (Optional) Open DevTools in your browser and turn on throttling.
2. Open the following link: https://oauth.yandex.ru/authorize?response_type=token&client_id=23cabbbdc6cd418abb4b39c32c41195d
3. Authorize and provide access to your library
4. After a short time a browser will redirect you to https://music.yandex.ru/#access_token=AQAAAAAYc***&token_type=bearer&expires_in=31535645.

    **!!ATTENTION!!** A redirect to another page will happen very quickly, so you need to cancel the page loading as soon as a link with access token appears.
    
    <img src="https://github.com/g2r4i6e8/exportTracksFromYandexMusicToDeezer/blob/master/docs/auth1.png?raw=true" width="1000" />
    <img src="https://github.com/g2r4i6e8/exportTracksFromYandexMusicToDeezer/blob/master/docs/auth2.png?raw=true" width="1000" />
5. Save your token that you can find right after *access_token=*

### Getting Deezer Token
1. Open https://developers.deezer.com/myapps
2. Click "Create a new Application"
3. Create a new app with the following Redirect URL: http://localhost:8080/oauth/return
   
   Other fields may be filled in with some random data.
   
   <img src="https://github.com/g2r4i6e8/exportTracksFromYandexMusicToDeezer/blob/master/docs/deezerApp1.jpg?raw=true" width="600" />
4. Install [deezer-oauth-cli](https://pypi.org/project/deezer-oauth-cli/) via pip: `pip install deezer-oauth-cli`
5. Run this tool using the following syntax: 
   
   ```shell
   $ deezer-oauth APP_ID APP_SECRET
   ```
   
   This will:
   - Spin up a webserver in the background running at http://localhost:8080.
   - Open your browser to grant authorisation access to your Deezer account.
   - Redirect to a page showing the API token & expiry (usually one hour but it is enough).
6. Save your token

   <img src="https://github.com/g2r4i6e8/exportTracksFromYandexMusicToDeezer/blob/master/docs/deezerApp2.png?raw=true" width="600" />

## External requirements

Looks like a subscription is required for both services to operate normally.

All created playlists in Deezer are Public by default. You may want to make them Private after import. 
## Credits

This package was created with
[yandex-music-api](https://github.com/MarshalX/yandex-music-api/) and
[deezer-oauth-cli](https://github.com/browniebroke/deezer-oauth-cli)

Special thanks to [Gleb Liutsko](https://github.com/glebliutsko) for the easy way to get a Yandex token

Code refactoring is done using [ChatGPT](https://openai.com/blog/chatgpt)
