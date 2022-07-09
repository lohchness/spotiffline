import requests, base64, json, re
import youtubesearchpython # CAUTION: LIBRARY NOT MAINTAINED AS OF 23/6/2022
from secret_ids import CLIENT_ID, CLIENT_SECRET

# WILL CHANGE TO ASK USER FOR PLAYLIST LINK
PLAYLIST_LINK = "https://open.spotify.com/playlist/3Zx2NoPvIYWst3GYQrAyb3?si=1ff2abea630a408d"

FIELDS = """items(added_at,track(name,duration_ms,album(name,images,artists),artists))"""
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
            print("Exceeded rate limits. Try again in 30 minutes.")
        return 0
    else:
        print(response_auth)
        print("Authentication succeeded!")
    return 1

def main(): # Traffic control

    # --------- STAGE 0: Authorization ---------
    response_auth = auth_client_credentials()

    if not response_status_codes(response_auth):
        return

    # --------- STAGE 1: Access Spotify API ---------
    # Gets playlist ID from URL and passes it to the endpoint with wanted fields
    playlist_id = re.search('https://open.spotify.com/playlist/(.*)\?', PLAYLIST_LINK).group(1)
    endpoint_playlist_fields = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields={FIELDS}"

    items = get_playlist_items(
        response_auth.json()['access_token'], 
        endpoint_playlist_fields,
        )
    
    # --------- STAGE 2: Data processing and duplication check ---------
    with open(f"{playlist_id}.json", "w") as f:
        json.dump(items.json(), f, indent=2)

    return

if __name__ == '__main__':
    main()