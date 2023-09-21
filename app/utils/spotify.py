import threading
from functools import wraps
from flask import session, redirect, url_for, request
from spotipy import Spotify


def spotify_auth_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "token_info" not in session or "access_token" not in session["token_info"]:
            return redirect(url_for("login", next=request.url))

        sp = Spotify(auth=session["token_info"]["access_token"])
        return f(sp, *args, **kwargs)  # Pass both 'self' and 'sp'

    return decorated_function


class SpotifyFetcher:
    def __init__(self, sp):
        self.sp = sp
        self.artist_genres = {}
        self.lock = threading.Lock()

    @staticmethod
    def _fetch_tracks(sp, offset, all_tracks):
        limit = 50
        results = sp.current_user_saved_tracks(limit=limit, offset=offset)
        all_tracks.extend(results["items"])
        print(f"Fetched Spotify Songs: {len(all_tracks)}")

    def get_all_saved_tracks(self):
        all_tracks = []
        threads = []

        # Fetch the first page to get the total number of tracks
        first_page = self.sp.current_user_saved_tracks(limit=1)
        total_tracks = first_page["total"]

        # Start threads to fetch all pages
        for offset in range(0, total_tracks, 50):
            thread = threading.Thread(target=self._fetch_tracks, args=(self.sp, offset, all_tracks))
            threads.append(thread)
            thread.start()

        # Wait for all threads to finish
        for thread in threads:
            thread.join()

        return all_tracks

    def fetch_artist_details(self, artist_ids):
        # Fetch artist details for a batch of artist IDs
        artists_details = self.sp.artists(artist_ids)["artists"]

        # Update our artist_genres dictionary with results
        with self.lock:
            for artist in artists_details:
                self.artist_genres[artist["id"]] = artist["genres"]

    def get_all_artist_genres(self, tracks):
        artist_ids = [track["track"]["artists"][0]["id"] for track in tracks]
        unique_artist_ids = list(set(artist_ids) - set(self.artist_genres.keys()))

        threads = []
        batch_size = 50

        for i in range(0, len(unique_artist_ids), batch_size):
            batch = unique_artist_ids[i : i + batch_size]
            thread = threading.Thread(target=self.fetch_artist_details, args=(batch,))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

        # Create a map by genres
        genre_map = {}
        for artist_id, genres in self.artist_genres.items():
            for genre in genres:
                if genre not in genre_map:
                    genre_map[genre] = []
                genre_map[genre].append(artist_id)

        return genre_map
