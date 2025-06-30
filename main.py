# creating a musical time machine in python
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()
# welcome
print("Hello I am musically Time Machine ☺️ \nI will take you to back in time ⏱️\nFull of memories💕")

def asking_date() :
  print("Please Enter Date ")
  year = input("Year : ")
  month = input("Month (in numeric) : ")
  day = input("Day : ")

  if 0 < int(month) < 10   :
    month = "0" + month
  if 0 < int(day) < 10  :
    day = "0" + day
  print("\nPlease wait...")
  return f"{year}-{month}-{day}"


response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{asking_date()}/")
response.raise_for_status()
content = response.text

# creating soup
# scraping data from the billboard website
soup = BeautifulSoup(content,"html.parser")
songs = soup.select(".lrv-u-width-100p ul li h3")

# creating list of all 100 songs
all_songs = []
track_ids = []

for index in range(100) :
    word = songs[index].getText()
    word_ = word.replace("\n","").replace("\t","")
    all_songs.append(word_)

# all songs list contain all 100 songs
# track_ids list contain track ids of all songs



# working with spotify api

# authorization with spotify
client_id = "add6ae47f120473aa41dfe57eda82b55"
client_secret = "9fef791cc9e94a17bc5c3c2c2bef1828"
redirect_url = "http://127.0.0.1:8888/callback"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_url,
                                               scope="user-library-read playlist-modify-public playlist-modify-private"))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])



# generating spotify token

token_info = sp.auth_manager.get_cached_token()
if token_info:
    access_token = token_info['access_token']
else:
    access_token = sp.auth_manager.get_access_token()

# spotify id
user_id = sp.current_user()['id']

# creating playlist
create_playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"


# searching a song in spotify
for song in all_songs :
    results = sp.search(q=f"{song}", type='track', limit=1)
    song_id = results['tracks']['items'][0]['id']
    track_ids.append(song_id)




# creating playlist of user name
playlist = sp.user_playlist_create(user_id, "Our Childhood Favourite 100 Songs ☺️", public=True)

# spotify id of my playlist
playlist_id = playlist['id']
playlist_url_link = playlist["external_urls"]["spotify"]

# Add tracks to the playlist
sp.playlist_add_items(playlist_id, track_ids)


# sending sms via twilio
twilio_mobile_no = os.getenv("twilio_mobile_no")
account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")

def send_sms() :
    try :
        print("Give Details of the Recievers's ")
        name = input("Enter Name : ")
        getter_mobile_no = int(input("Enter Mobile : "))
        print("\nplease wait...\n")
        sms = f"Hi {name} ☺️\nI have created a playlist of 100 most popular songs of our time⌚\nclick the link below :\n{playlist_url_link}"

    except :
        print("Invalid data given Try again")



    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=sms,
        from_=twilio_mobile_no,
        to="+91" + str(getter_mobile_no),
    )

    # confirmation
    print("message sent successfully")


print("Playlist Created Successfully on you Spotify Account...")
choice = input("Do you want to Share your playlist (Yes/No) : ").lower()

if choice == "yes":
    send_sms()
else :
    print("Playlist created successfully on your Spotify Account!!")
    print("Enjoy music!!")






