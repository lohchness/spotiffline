# SPOTIFFLINE TODO

### LINKS

[Get playlist items Reference (pay attention to cURL request)](https://developer.spotify.com/documentation/web-api/reference/#/operations/get-playlists-tracks)

[Authorization guide](https://developer.spotify.com/documentation/general/guides/authorization/)

[Client Credentials Flow](https://developer.spotify.com/documentation/general/guides/authorization/client-credentials/)

[Use Access Token](https://developer.spotify.com/documentation/general/guides/authorization/use-access-token/)

[Response Status Codes](https://developer.spotify.com/documentation/web-api/)

[Spotify API Dashboard](https://developer.spotify.com/dashboard/applications)


### STAGE 0: Authorization

- [x] Registered app in dashboard
- [x] Implement authorization so that the app automatically requests a new access token
  - ❌ PKCE or Implicit grant
    - PKCE provides protection against request forgery
    - Implicit returns token in URL and doesnt support refresh tokens but is easier to implement
      - only works with JS and a browser
  - [x] Thinking of doing client credentials, it does not require a backend service. Cannot access user information.

### STAGE 1: Access Spotify API

- [x] Retrieve JSON from [spotify API](<https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=3Zx2NoPvIYWst3GYQrAyb3&market=ES&fields=items(added_at%2Ctrack(name%2Cduration_ms%2Calbum(name%2Cimages%2Cartists)%2Cartists))&limit=&offset=&additional_types=>)

  - [ ] will ask user for playlist link and number of tracks to retrieve from an unsorted playlist as well as offset
  - ❌ also ask number of songs from a playlist sorted by most recent
  - [x] fields: **items(added_at,track(name,duration_ms,album(name,images,artists),artists))**

### STAGE 2: Duplication check

- [ ] add duplicate protection in the future if i want to download songs from the same playlist again but not want to redownload the same songs
  - [ ] CHECK IF TRACK IS ALREADY IN JSON FILE
    - Need to ask user how many tracks are in playlist so it can retrieve all playlist items
      - Choose between getting all items in playlist OR just at most 100 recently added tracks
- [ ] download 640x640 thumbnail from images field for Stage 4


### STAGE 3: Download audio
 - SEARCH TERMS DO NOT GUARANTEE A RETURN OF THE CORRECT VIDEO
   - at first I was thinking of having the search term be "ARTIST_NAME TRACK_NAME audio" to filter out music videos, but
   - eg appending "audio" to "The Birthday Massacre - Oceania" will return a url to a nightcore version
     - appending "-nightcore" to exclude will return a completely different song by the same band
     - even adding "audio" to the end of the search query may return an unofficial video with low views or low quality.
   - I weighed the choices and just ended up searching for the term without "audio -acoustic" because most of the songs in my playlist shouldn't have music videos anyway.
 - [x] Retrieve URL of search term using youtubesearchpython.videosSearch("{TERM}", limit=1).result
   - then redirect to yt-dlp for download
   - I could just use subprocess.popen to run the command to download from a search query from terminal, but is more complicated
     - if it works, don't fix it
 - [x] OR Use yt-dlp to download video and convert audio from search term
   - command line is yt-dlp -x "ytsearch1: {QUERY}"
     - automatically downloads best format, but only audio quality rating of 5/10
     - can add --audio-quality 0 for best quality but shouldnt be a problem
   - This will download video first, then convert to audio using ffmpeg. Not feasible for bandwidth restrictions but it suits my purpose. Each download seems to be around 4 MB, so 100 songs is 400 MB downloaded.
   - RECOMMEND MAX 250 SONGS TO DOWNLOAD
     - Each song download is around 4-5 MB, having 250 songs will download at least 1GB. Or you can just go ahead and download more, you have been warned.


##### Housekeeping

- [x] clean up constants/magic numbers, especially endpoints
- ❌ add section to get list of a users playlists?
  - not possible without auth code flow and a backend service. User will have to make their playlist public but only temporarily to retrieve playlist items with client credentials.
