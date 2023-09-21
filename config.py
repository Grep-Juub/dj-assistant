import os


class Config:
    # Basic Flask configurations
    HOST = os.environ.get("FLASK_RUN_HOST") or "0.0.0.0"
    SECRET_KEY = os.environ.get("SECRET_KEY") or "hard_to_guess_secret_key"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL") or "postgresql://spotify:mygeneratedpassword@localhost:5432/spotifydb"
    )

    # Spotify API configurations
    SPOTIFY_CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
    SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
    SPOTIFY_REDIRECT_URI = os.environ.get("SPOTIFY_REDIRECT_URI") or "http://localhost:5000/callback"
    SPOTIFY_SCOPE = "user-library-read"  # You can extend this scope based on your needs


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {"development": DevelopmentConfig, "production": ProductionConfig, "default": DevelopmentConfig}
