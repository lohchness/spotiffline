import requests

ACCESS_TOKEN = "BQAVi11kky6MLd2W7TJXyzliLNbVi1mo6cvORyMT0DTcn5zU_zme6cgiIBXGTbdvyUgkVwoU5dZrEjMqnZGXURx-GuqVoSWtQUQk5jhh5yNc9se6vcZ2HAIgBPEd0Mq2lKtuf9nIutCB4TlkIySdjb2l5OSeFIxXD0xH-LzBB6W0MQJ1xuL651GxadLLSB2h3Cbei1sPLrojn7LsBxPQv7Tv0oRoztpEYscib5Oo2UcX02nS8GoxqzdpeVho"
SPOTIFY_CREATE_PLAYLIST_URL = "https://api.spotify.com/v1/users/21s7t6cbfhdjlu134hmkcgfu5/playlists"

def create_playlist_on_spotify(name, public):
    response = requests.post(
        SPOTIFY_CREATE_PLAYLIST_URL,
        headers={
            "Authorization" : f"Bearer {ACCESS_TOKEN}"
        },
        json={
            "name" : name,
            "public" : public
        }
    )
    json_resp = response.json()

    return json_resp


def main():
    playlist = create_playlist_on_spotify(
        name = "testing playlist",
		
        public=False
    )
    
    print(f"Playlist : {playlist}")


if __name__ == '__main__':
    main()