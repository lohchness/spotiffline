from ast import parse
import requests, json, pprint
from secret_ids import CLIENT_ID, CLIENT_SECRET

PLAYLIST_ID = "3Zx2NoPvIYWst3GYQrAyb3"
ACCESS_TOKEN = "BQBCfEbYLo44QS11RjUyMjLFK9HZiHUP6im3hssI44KB-QbTIKmMrOJkMjymngj2EKZ2boXYuRchr8CzG2N7FtXkGEuQ7ejjEThDSu1CTs6EqOj49BviEHZQQN7yukQ05LjA32sgWZC4GVGUeiWzjiWfb5i49qC6UYccz4Yy6WcpJtjGDqpbraBwNUXEGPs"
ENDPOINT = f"https://api.spotify.com/v1/playlists/{PLAYLIST_ID}/tracks"
FIELDS = """items(added_at,track(name,duration_ms,album(name,images,artists),artists))"""

ENDPOINT_WITH_FIELDS = f"{ENDPOINT}?fields={FIELDS}"

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

def main():
    parse_json = fetch_json()
    # print(parse_json)
    pprint.pprint(parse_json)

if __name__ == '__main__':
    main()


