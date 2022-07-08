import random
import string
import base64
from urllib import response
import requests
from secret_ids import CLIENT_ID, CLIENT_SECRET
import webbrowser

BASE_URI = "https://api.spotify.com/v1"
# REDIRECT_URI = "spotiffline-login://callback"
REDIRECT_URI = "https://localhost/"
PLAYLIST_ID = "3Zx2NoPvIYWst3GYQrAyb3"
ACCESS_TOKEN = "BQAt1iR6hGGw4h8fTPQqBFkWNgJFTqjiSF2XSv7xVHHcgFNKCVkexu6PMWNCqgeeub-Y17j5noeuxHWFV3SCF_1FIgnWwnasiXVwc9cm92QrwQdhwd3MsDmW1qHtsvBYoI5xW2bXhpi6GZUFYxqO4Hq66sAL3lt1EkgD-M7-rtGoi551qatJf8tves3z8Q0"
ENDPOINT_PLAYLIST = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
FIELDS = """items(added_at,track(name,duration_ms,album(name,images,artists),artists))"""
ENDPOINT_PLAYLIST_WITH_FIELDS = ENDPOINT_PLAYLIST + f"?fields={FIELDS}"
ENDPOINT_APITOKEN = "https://accounts.spotify.com/api/token"
ENDPOINT_AUTHORIZE = "https://accounts.spotify.com/authorize"
LENGTH = 16

def randomString(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def auth_implicit_grant():
    # working, returns code 200 but found out later that this is 
    # for clients implemented entirely in JS and running in a browser.
    # URL Hash values are not accessible server side, theyre not included in headers
    response = requests.get(
        ENDPOINT_AUTHORIZE,
        {
        "client_id" : CLIENT_ID,
        "response_type" : "token",
        "redirect_uri" : "spotiffline-login://callback", 
        "state" : randomString(LENGTH)
    })
    return response # returns URL containing hash fragment with data encoded as query string, not JSON object

def auth_client_credentials():
    # Working, returns access token in response but this flow
    # does not grant access to user information (if playlist is public we go this route)
    response = requests.post(
        ENDPOINT_APITOKEN,
        # query parameter
        {
        "grant_type" : "client_credentials",
        "client_id" : CLIENT_ID,
        "client_secret" : CLIENT_SECRET
        }
    )
    return response.json()

def auth_code():
    # Request user authorization
    response = requests.get(
        "https://accounts.spotify.com/authorize",
        {
            "client_id" : CLIENT_ID,
            "response_type" : "code",
            "redirect_uri" : REDIRECT_URI,
            # "state" : randomString(LENGTH),
            # "scope" : "playlist-read-private",

            # PKCE Extension
            # "code_challenge_method" : "S256",
            # "code_challenge" : base64.b64encode(hashlib.sha256(randomString(50).encode('utf-8')).digest())
        },
    )
    return response

def request_access_token(code):
    # Turns out for auth code flow we need a web server to recieve 
    # access tokens so we will go for client credentials instead
    to_encode = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
    b64encoded = base64.urlsafe_b64encode(to_encode)
    decodedstring = b64encoded.decode()
    # Exchange authorization code for Access Token
    response = requests.post(
        url="https://accounts.spotify.com/api/token",
        data={
            "grant_type" : "authorization_code",
            "code" : code,
            "redirect_uri" : REDIRECT_URI,
        },
        headers={
            # "Authorization" : f"Basic {base64.b64encode(bytes(CLIENT_ID, 'utf-8'))}:{base64.b64encode(bytes(CLIENT_SECRET, 'utf-8'))}",
            "Authorization" : f"Basic {decodedstring}",
            "Content-Type" : "application/x-www-form-urlencoded"
        }
    )
    return response

def fetch_json():
    # No authorization, need to manually refresh access token in API 
    # TODO: Change Access Token to new access token granted by auth request
    response = requests.get(
        ENDPOINT_PLAYLIST,
        headers={
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {ACCESS_TOKEN}"
        },
    )
    response_json = response.json()

    return response_json


def main():
    # --- STAGE 0 ---
    # Auth code flow
    # response_auth = auth_code()
    # print(response_auth)
    # webbrowser.open(response_auth.url)

    # if response_auth.status_code == 200:
    #     token = request_access_token(response_auth)
    #     print(token)


    # Client Credentials
    # response_auth = auth_client_credentials()

    # Implicit grant
    # response_auth = auth_implicit_grant()

    # --- STAGE 1 ---
    # parse_json = fetch_json()
    # pprint.pprint(parse_json)
    # with open(f"{PLAYLIST_ID}.json", "w") as file:
    #     json.dump(parse_json, file)

    # --- STAGE 2 ---
    return

if __name__ == '__main__':
    main()

