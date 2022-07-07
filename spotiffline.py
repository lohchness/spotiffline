from ast import parse
import requests, json, pprint
from secret_ids import CLIENT_ID, CLIENT_SECRET

PLAYLIST_ID = "3Zx2NoPvIYWst3GYQrAyb3"
ACCESS_TOKEN = "BQAt1iR6hGGw4h8fTPQqBFkWNgJFTqjiSF2XSv7xVHHcgFNKCVkexu6PMWNCqgeeub-Y17j5noeuxHWFV3SCF_1FIgnWwnasiXVwc9cm92QrwQdhwd3MsDmW1qHtsvBYoI5xW2bXhpi6GZUFYxqO4Hq66sAL3lt1EkgD-M7-rtGoi551qatJf8tves3z8Q0"
ENDPOINT = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
FIELDS = """items(added_at,track(name,duration_ms,album(name,images,artists),artists))"""
ENDPOINT_WITH_FIELDS = ENDPOINT + f"?fields={FIELDS}"


def implicitgrant_request_user_authorization():
    response = requests.get(
        client_id = CLIENT_ID,
        response_type = 'token',
        redirect_uri = 'spotiffline-login://callback',
        
    )

    hash_fragment = response.split('=')
 
    return hash_fragment

def pcke_req_user_auth():
    response = requests.get(
        client_id = CLIENT_ID,
        response_type = 'code',
        redirect_uri = 'spotiffline-login://callback'
    )


def fetch_json():
    response = requests.get(
        ENDPOINT_WITH_FIELDS,
        headers={
            "Accept" : "application/json",
            "Content-Type" : "application/json",
            "Authorization" : f"Bearer {ACCESS_TOKEN}"
        },
    )
    response_json = response.json()

    return response_json

def parse_json(json):
    pass


def main():
    # --- STAGE 1 ---
    # parse_json = fetch_json()
    # pprint.pprint(parse_json)
    # with open(f"{PLAYLIST_ID}.json", "w") as file:
    #     json.dump(parse_json, file)

    # --- STAGE 2 ---
    parse_json(f"{PLAYLIST_ID}.json")

if __name__ == '__main__':
    main()

