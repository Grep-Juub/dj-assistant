from flask import Flask, render_template, request, redirect, url_for, session
from spotipy.oauth2 import SpotifyOAuth
from app.utils.spotify import SpotifyFetcher, spotify_auth_required


from app import app

# Spotify setup
sp_oauth = SpotifyOAuth(
    client_id=app.config["SPOTIFY_CLIENT_ID"],
    client_secret=app.config["SPOTIFY_CLIENT_SECRET"],
    redirect_uri=app.config["SPOTIFY_REDIRECT_URI"],
    scope=app.config["SPOTIFY_SCOPE"],
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/callback")
def callback():
    # Handle the callback after user grants/denies permission
    token_info = sp_oauth.get_access_token(request.args["code"])
    session["token_info"] = token_info
    return redirect(url_for("get_tracks"))


@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)


@app.route("/tracks")
@spotify_auth_required
def get_tracks(sp):
    fetcher = SpotifyFetcher(sp)
    results = fetcher.get_all_saved_tracks()
    track_data = [(track["track"]["name"], track["track"]["artists"][0]["name"]) for track in results]
    return render_template("tracks.html", tracks=track_data)


@app.route("/genres")
@spotify_auth_required
def get_genres(sp):
    # Fetch the user's saved tracks
    fetcher = SpotifyFetcher(sp)
    tracks = fetcher.get_all_saved_tracks()
    total_tracks = len(tracks)

    # Map tracks to their genres
    genres = fetcher.get_all_artist_genres(tracks)
    genre_counts = {genre: len(tracks) for genre, tracks in genres.items()}

    return render_template("genres.html", total_tracks=total_tracks, genre_counts=genre_counts)
