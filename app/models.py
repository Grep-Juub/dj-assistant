# models.py

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

artist_genre_association = Table(
    "artist_genre",
    Base.metadata,
    Column("artist_id", Integer, ForeignKey("artists.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)

track_genre_association = Table(
    "track_genre",
    Base.metadata,
    Column("track_id", Integer, ForeignKey("tracks.id")),
    Column("genre_id", Integer, ForeignKey("genres.id")),
)


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    tracks = relationship("Track", back_populates="artist")
    genres = relationship("Genre", secondary=artist_genre_association, back_populates="artists")


class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_id = Column(Integer, ForeignKey("artists.id"))
    artist = relationship("Artist", back_populates="tracks")
    genres = relationship("Genre", secondary=track_genre_association, back_populates="tracks")


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    artists = relationship("Artist", secondary=artist_genre_association, back_populates="genres")
    tracks = relationship("Track", secondary=track_genre_association, back_populates="genres")
