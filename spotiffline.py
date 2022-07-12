import requests, base64, json, re
import youtubesearchpython as yt
import yt_dlp# CAUTION: LIBRARY NOT MAINTAINED AS OF 23/6/2022
from secret_ids import CLIENT_ID, CLIENT_SECRET

# WILL CHANGE TO ASK USER FOR THESE
# PLAYLIST_LINK = "https://open.spotify.com/playlist/3Zx2NoPvIYWst3GYQrAyb3?si=1ff2abea630a408d"
PLAYLIST_LINK = "https://open.spotify.com/playlist/5C5E0QzJAL2uxT2MfAI5R8?si=4bf12fc3394a489b"
DOWNLOAD_DIRECTORY = "C:/Users/User/Music"
LIMIT = 10 # Default 100
OFFSET = 10 # Default 0

FIELDS = """items(added_at,track(id,name,duration_ms,album(id,name,images,artists),artists))"""

ENDPOINT_APITOKEN = "https://accounts.spotify.com/api/token"

def auth_client_credentials():
    encodedstr = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    b64encoded = base64.urlsafe_b64encode(encodedstr)
    decodedstring = b64encoded.decode()
    # Working, returns access token in response but this flow
    # does not grant access to user information, can only access public information
    # If auth code flow needs external web service we go this route
    response = requests.post(
        ENDPOINT_APITOKEN,
        data={
        "grant_type" : "client_credentials",
        },
        headers={
            "Authorization" : f"Basic {decodedstring}",
            "Content-Type" : "application/x-www-form-urlencoded",
        }
    )
    return response

def get_playlist_items(access_token, playlist_id):
    response = requests.get(
        playlist_id,
        headers={
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {access_token}"
        },
    )

    return response

def response_status_codes(response_auth): # Only applies to Get Playlist Items
    if response_auth.status_code != 200:
        print(response_auth)
        print(response_auth.json())
        if response_auth.status_code == 401:
            print("Access token expired, relaunch app and it should be good.")
        elif response_auth.status_code == 403:
            print("Bad OAuth request, like wrong consumer key/expired timestamp.")
        elif response_auth.status_code == 429:
            print("Exceeded rate limits. Try again in 30 seconds.")
        return 0
    else:
        print(response_auth)
        print("Authentication succeeded!")
    return 1

def main(): # Traffic control

    # if False: # REMOVE THIS LATER WHEN DONE WITH STAGES 2-4 SO AS TO NOT KEEP ON REQUESTING
    # --------- STAGE 0: Authorization ---------
    response_auth = auth_client_credentials()

    if not response_status_codes(response_auth):
        return

    # --------- STAGE 1: Access Spotify API ---------
    # Gets playlist ID from URL and passes it to the endpoint with wanted fields
    playlist_id = re.search('https://open.spotify.com/playlist/(.*)\?', PLAYLIST_LINK).group(1)
    endpoint_playlist_fields = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields={FIELDS}"
    endpoint_playlist_fields_limit = f"{endpoint_playlist_fields}&limit={LIMIT}"
    endpoint_playlist_fields_limit_offset = f"{endpoint_playlist_fields_limit}&offset={OFFSET}"
    items = get_playlist_items(
        response_auth.json()['access_token'], 
        endpoint_playlist_fields_limit_offset,
        )
    with open(f"{playlist_id}.json", "w") as f:
        json.dump(items.json(), f, indent=2)
        print(f"Information saved at {playlist_id}.json.")
        

        # return # Only for redoing stage 1
    
    # --------- STAGE 2: Duplication check ---------
    
    # REMOVE BELOW WHEN DONE WITH STAGES 2-4
    # playlist_id = re.search('https://open.spotify.com/playlist/(.*)\?', PLAYLIST_LINK).group(1)

    with open(f"{playlist_id}.json", "r") as infile:
        items = json.load(infile)["items"]
        with open("keep_track.json", "a") as outfile:
            all_track_artists = {}
            all_album_artists = {}
            all_track_ids = {}
            count = 1
            for item in items:
                first_artist = "" # Artist listed first is usually the lead
                curr_artists = []
                curr_track_name = item["track"]["name"]
                curr_track_id = item["track"]["id"]
                if curr_track_id not in all_track_ids:
                    all_track_ids[curr_track_id] = curr_track_name
                for artist in item["track"]["artists"]:
                    curr_artist_id = artist["id"]
                    curr_artist_name = artist["name"]
                    curr_artists.append(curr_artist_name)
                    if not first_artist:
                        first_artist = curr_artist_name
                    if curr_artist_id not in all_track_artists:
                        all_track_artists[curr_artist_id] = artist["name"]
                for album in item["track"]["artists"]:
                    curr_album_id = album["id"]
                    if curr_album_id not in all_album_artists:
                        all_album_artists[curr_album_id] = album["name"]

                videoSearch = yt.VideosSearch(f"{first_artist} {curr_track_name}", limit=1)
                videolink = videoSearch.result()["result"][0]["link"]
                # URLS.append(videolink)
                ydl_opts = {
                    'format': 'bestaudio',
                    'outtmpl' : f"{DOWNLOAD_DIRECTORY}/{', '.join([i for i in curr_artists])} - {curr_track_name}.%(ext)s",
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                    }]
                }
                print(f"\n------------ SONG #{count}: {', '.join([i for i in curr_artists])} - {curr_track_name} -------------------")
                count += 1
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    error_code = ydl.download(videolink)

                


    return

if __name__ == '__main__':
    main()