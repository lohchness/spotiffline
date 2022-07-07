1.  Retrieve JSON from [spotify API](https://developer.spotify.com/console/get-playlist-tracks/?playlist_id=3Zx2NoPvIYWst3GYQrAyb3&market=ES&fields=items(added_at%2Ctrack(name%2Cduration_ms%2Calbum(name%2Cimages%2Cartists)%2Cartists))&limit=&offset=&additional_types=)
    - playlist_id: **3Zx2NoPvIYWst3GYQrAyb3**
         - use this for now, will ask user for playlist link and number of tracks to retrieve from an unsorted playlist as well as offset
           - maybe also ask number of songs from a playlist sorted by most recent
    - fields: **items(added_at,track(name,duration_ms,album(name,images,artists),artists))**
    - OAuth token: **BQAw2qdili1ZWJS6EV165n-I-_MfHYvR72XfcAJRv0nLr9eRb_xcvb4l2uI3u9Y6uTQQ3VGpwCNa_m2FgvAA0tGs7MOhJagYYaFdfGY76TZLmuDT9eqYCb1Hu8cV-g1vVszb2B272yOLNlh72ne_nxib-
2.  Load, parse json data into dataframe
    - if there are multiple artists for track and album, append them to an ordered list into their dataframe column
      - for metadata purposes
    -  add duplicate protection in the future if i want to download songs from the same playlist again but not want to redownload the same songs
       -  keep id and name fields for track, album, artists
       -  export dataframe into another json
    -  download 640x640 thumbnail from the images field if needed
    -  discard unnecessary fields like href, url
3. Use Youtube API to retrieve URL from a search term
	- search term is "{artist} {song name} audio"
	- [link](https://developers.google.com/youtube/v3/docs/search/list?apix=true) 
    	- change the q field to change query
	- only allowed 10000 units per day, search costs 100 units so 100 songs per day
	- in progress will expand once closer 