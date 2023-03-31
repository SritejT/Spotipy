import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import flask
from flask import render_template, request, jsonify
import random
from datetime import date
import pandas as pd
import json

cid = '035e7ce95009460d88e5d6f48e4078fb'
secret = '4c49ecc3d9fe40798cd51a3e5f697e31'
curr_year = date.today().year

app = flask.Flask(__name__)

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(auth_manager=client_credentials_manager)

pop_track_list = []


def jprint(obj):

    return print(json.dumps(obj, indent=4))


@app.route('/', methods=['GET'])
def index():

    return render_template('site.html')


@app.route('/inspiration', methods=['GET'])
def inspiration():

    return render_template('inspiration.html')


@app.route('/relatedartists', methods=['GET'])
def related_artists():

    return render_template('related_artists.html')


@app.route('/genres', methods=['GET'])
def genres():

    return render_template('genres.html')


@app.route('/userprofile', methods=['GET'])
def user_profile():

    return render_template('user_profile.html')


@app.route('/search', methods=['GET'])
def search_popular():

    track_result = sp.search(q='year:' + str(curr_year), type='track', limit=50)

    randint = random.randint(0, 49)

    random_artist_img = track_result['tracks']['items'][randint]['album']['images'][0]['url']
    random_pop_track = track_result['tracks']['items'][randint]['name']
    random_artist = track_result['tracks']['items'][randint]['artists'][0]['name']

    return flask.jsonify({"items": [str(random_pop_track), str(random_artist), str(random_artist_img)]})


@app.route('/addpopsong', methods=['GET'])
def add_popular_song():

    song = request.get_json

    print(song['song_to_add'])




@app.route("/risingartists", methods=['POST'])
def get_rising_artists():

    rising_artists = []

    img_list = []

    combined_list = []

    famous_artist = request.get_json()

    artist_results = sp.search(q=str(famous_artist['data']['famous_artist']), limit=1, type='artist')

    id = artist_results['artists']['items'][0]['id']

    while len(rising_artists) < 10:

        related_artists = sp.artist_related_artists(artist_id=id)

        items = len(related_artists['artists']) - 1

        for i in range(0, items):

            rising_artists.append(related_artists['artists'][i]['name'])

            img_list.append(related_artists['artists'][i]['images'][0]['url'])

        id = related_artists['artists'][random.randint(0, items)]['id']

    rising_artists = list(dict.fromkeys(rising_artists))

    img_list = list(dict.fromkeys(img_list))

    while len(rising_artists) > 10:

        rising_artists.pop()
        img_list.pop()

    for i in range(0, len(rising_artists)):

        combined_list.append([rising_artists[i], img_list[i]])

    return flask.jsonify({"content": combined_list})


@app.route('/genre', methods=['POST'])
def find_artists_by_genre():

    genre_artists = []

    img_list = []

    combined_list = []

    data = request.get_json()

    success = False

    while True:

        counter = 0

        results = sp.search(q='year:1950-2020', limit=50, type='artist')

        for artist in results['artists']['items']:

            counter += 1

            if counter == 50:

                return flask.jsonify({"artists": ["Artists not found."]})

            for genre in artist['genres']:

                if str(genre) == (data['genre']).lower():

                    success = True

                    break

            if success:

                break

        if success:

            break

    id = artist['id']

    while len(genre_artists) < 10:

        related_artists = sp.artist_related_artists(artist_id=id)

        items = len(related_artists['artists']) - 1

        for i in range(0, items):

            for genre in related_artists['artists'][i]['genres']:

                if genre == str(data['genre'].lower()):

                    genre_artists.append(related_artists['artists'][i]['name'])

                    img_list.append(related_artists['artists'][i]['images'][0]['url'])

        id = related_artists['artists'][random.randint(0, items - 1)]['id']

    genre_artists = list(dict.fromkeys(genre_artists))

    img_list = list(dict.fromkeys(img_list))

    while len(genre_artists) > 10:

        genre_artists.pop()
        img_list.pop()

    for i in range(0, len(genre_artists)):

        combined_list.append([genre_artists[i], img_list[i]])

    return flask.jsonify({"content": combined_list})


@app.route('/promptuser', methods=['POST'])
def prompt_user():

    user_recents_list = []
    top_list = []
    common_list = []
    user_recents_ids = []
    top_ids = []
    common_ids = []
    energy = []
    danceability = []
    tempo = []
    recommended_list = []
    recommended_artists = []
    recommended_images = []
    combined_list = []

    token = spotipy.prompt_for_user_token(username='',
                                          scope='user-read-recently-played',
                                          client_id=cid,
                                          client_secret=secret,
                                          redirect_uri='http://127.0.0.1:8569/')

    sp = spotipy.Spotify(auth=token)

    recents = sp.current_user_recently_played(limit=50)

    for i in range(0, len(recents['items'])):

        user_recents_ids.append(recents['items'][i]['track']['id'])

        user_recents_list.append(recents['items'][i]['track']['name'])

    top = sp.current_user_top_tracks(limit=50)

    for i in range(0, len(top['items'])):

        top_ids.append(top['items'][i]['id'])

        top_list.append(top['items'][i]['name'])

    for i in range(0, len(user_recents_list)):

        for j in range(0, len(top_list)):

            if user_recents_list[i] == top_list[j]:

                common_list.append(user_recents_list[i])

                common_ids.append(user_recents_ids[i])

    if len(common_list) == 0:

        return jsonify({"user_recents": ["Artists not found."]})

    for song_id in common_ids:

        results = sp.audio_features(song_id)

        energy.append(results[0]['energy'])
        danceability.append(results[0]['danceability'])
        tempo.append(results[0]['tempo'])

    df = pd.DataFrame({"name": common_list,
                       "energy": energy,
                       "danceability": danceability,
                       "tempo": tempo})

    description = df.describe()

    mean_energy = description.loc['mean']['energy']
    mean_danceability = description.loc['mean']['danceability']
    mean_tempo = description.loc['mean']['tempo']

    energy_deviation = description.loc['std']['energy'] / 2
    danceability_deviation = description.loc['std']['danceability'] / 2
    tempo_deviation = description.loc['std']['tempo'] / 2

    for i in range(curr_year - 5, curr_year):

        results = sp.search(q='year: ' + str(i), type='track', limit=50)

        for j in range(0, len(results['tracks']['items'])):

            id = results['tracks']['items'][j]['id']

            features = sp.audio_features(id)

            if mean_energy - energy_deviation < features[0]['energy'] < mean_energy + energy_deviation:

                if mean_danceability - danceability_deviation < features[0]['danceability'] < mean_danceability + danceability_deviation:

                    if mean_tempo - tempo_deviation < features[0]['tempo'] < mean_tempo + tempo_deviation:

                        recommended_list.append(results['tracks']['items'][j]['name'])

                        recommended_artists.append(results['tracks']['items'][j]['album']['artists'][0]['name'])

                        recommended_images.append(results['tracks']['items'][j]['album']['images'][0]['url'])

    for i in range(0, len(recommended_list)):

        combined_list.append((recommended_list[i], recommended_artists[i], recommended_images[i]))

    combined_list = list(dict.fromkeys(combined_list))

    return jsonify({"user_recents": combined_list})

@app.route('/trending', methods=["GET", "POST"])
def get_trending_tracks():

    id_list = []

    playlist_results = sp.search(q="Global Top 50", type='playlist', limit=1)

    id = playlist_results['playlists']['items'][0]['id']

    track_results = sp.playlist_tracks(playlist_id=id)

    for i in track_results['items']:

        id_list.append(i['track']['id'])

    return "Done!"




if __name__ == '__main__':

    app.run(port=8570)
