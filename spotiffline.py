import requests, base64, re, yt_dlp
import youtubesearchpython as yt # CAUTION: LIBRARY NOT MAINTAINED AS OF 23/6/2022
from secret_ids import CLIENT_ID, CLIENT_SECRET

FIELDS = """items(added_at,track(id,name,duration_ms,album(id,name,images,artists),artists))"""
ENDPOINT_APITOKEN = "https://accounts.spotify.com/api/token"

def auth_client_credentials():
	# Server-to-server authentication. Can only access public information.
	encodedstr = f"{CLIENT_ID}:{CLIENT_SECRET}".encode()
	b64encoded = base64.urlsafe_b64encode(encodedstr)
	decodedstring = b64encoded.decode()
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

def get_playlist_items(access_token, playlist_link):
	# Retrieves playlist items from a URL and access token.
	response = requests.get(
		playlist_link,
		headers={
			"Accept" : "application/json",
			"Content-Type" : "application/json",
			"Authorization" : f"Bearer {access_token}"
		},
	)
	return response

def response_status_codes(response_auth):
	# Determines whether authorization has succeeded.
	if response_auth.status_code != 200:
		print(response_auth)
		print(response_auth.json())
		if response_auth.status_code == 401:
			print("Access token expired, relaunch app and it should be good.")
		elif response_auth.status_code == 403:
			print("Bad OAuth request, could be wrong consumer key/expired timestamp.")
		elif response_auth.status_code == 429:
			print("Exceeded rate limits. Try again in 30 seconds.")
		return 0
	else:
		print(response_auth)
		print("Authentication succeeded!")
	return 1

def download_tracks(keep_track, download_directory, offset=0):
	# Downloads tracks into directory
	count = offset+1
	
	for item in keep_track["items"]:
		first_artist = "" # Artist listed first is usually the lead, used in search term
		curr_artists = []
		curr_track_name = item["track"]["name"]

		for artist in item["track"]["artists"]:
			curr_artist_name = artist["name"]
			curr_artists.append(curr_artist_name)
			if not first_artist:
				first_artist = curr_artist_name

		# Retrieve video link from youtube search results
		videoSearch = yt.VideosSearch(f"{first_artist} {curr_track_name}", limit=1)
		videolink = videoSearch.result()["result"][0]["link"]

		print(f"\n------------ SONG #{count}: {', '.join([i for i in curr_artists])} - {curr_track_name} -------------------")
		
		# Download track into directory
		curr_track_name = curr_track_name.replace('/','.').replace('\\','.')
		ydl_opts = {
			'format': 'bestaudio',
			'outtmpl' : f"{download_directory}/{', '.join([i for i in curr_artists])} - {curr_track_name}.%(ext)s",
			'postprocessors': [{
				'key': 'FFmpegExtractAudio',
			}]
		}
		with yt_dlp.YoutubeDL(ydl_opts) as ydl:
			error_code = ydl.download(videolink)
		count += 1


def main(): # Traffic control

	# Authorize credentials with Spotify API to access playlist items
	response_auth = auth_client_credentials()

	if not response_status_codes(response_auth):
		return

	# Ask user for information about what and where to download
	playlist_link = input("\nEnter the URL to your playlist. Make sure the playlist is set to public.\nURL: ")
	directory = input("\nPaste the directory where you want the files to be downloaded.\nYou must include the drive, for example C:\\my_files\\download_music_folder.\nDirectory: ").replace("\\","/")

	ask = input("\nWould you like to download all the songs in the playlist?\nIf 'n' is entered, this will download the first 100 songs, when the playlist has no sort applied to it. (y/n): ")
	dl_all = 0
	if ask.lower() == "y":
		dl_all = 1
		playlist_length = int(input("\nEnter the number of songs in the playlist: "))
	elif ask.lower() != "n":
		dl_all = 0
		print("Enter either 'y' or 'n'.")
		return
	
	playlist_id = re.search('https://open.spotify.com/playlist/(.*)\?', playlist_link).group(1)
	endpoint_playlist = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields={FIELDS}"
	
	# Dictionary of tracks to download, passed on to download_tracks()
	keep_track = {"items" : []}

	# Access Spotify API using access token and retrieve playlist items
	if not dl_all:
		keep_track["items"].extend(
			get_playlist_items(
				response_auth.json()['access_token'], 
				endpoint_playlist,
				).json()["items"]
			)
	else:
		offset = 0
		while playlist_length > 0:
			if offset:
				endpoint_playlist += f"&offset={offset}"
			keep_track["items"].extend(
				get_playlist_items(
					response_auth.json()['access_token'], 
					endpoint_playlist,
				).json()["items"]
			)
			offset += 100
			playlist_length -= 100

	# Download tracks into directory
	download_tracks(keep_track, directory)

	return

if __name__ == '__main__':
	main()