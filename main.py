import argparse
from Spotify import *
from WikiData import *
from MusicBrainz import *

wikidata = WikiData()
spotify = Spotify()
musicbrainz = MusicBrainz()


def popularityString(popularity):
    result = " "
    if (popularity is not None):
        if (popularity < 50):
            if (popularity > 30):
                result = " medium popular "
            else:
                result = " not so popular "
        else:
            if (popularity > 80):
                result = " extremely popular "
            else:
                result = " popular "
    return result


def main(query):
    name = query.title()

    is_artist = wikidata.check_if_artist(name)

    label = wikidata.get_label(name)

    track_names = None
    track_ids = None
    track_urls = None
    albums = None
    related_artists = None
    popularity = None
    follower_total = None
    danceability = None
    danceableString = None
    energy = None
    energyString = None
    musicbrainz_id = None

    if(is_artist):
        referall = "artist"
        genres = wikidata.get_artist_genres(name)
        members = None
        time_period = wikidata.get_artist_start_period(name)
        spotify_id = wikidata.get_artist_spotify_id(name)
    else:
        referall = "band"
        genres = wikidata.get_band_genres(name)
        members = wikidata.get_band_members(name)
        time_period = wikidata.get_band_time_period(name)
        spotify_id = wikidata.get_band_spotify_id(name)

    # If no Spotify ID is found, try to get it using MusicBrainz
    musicbrainz_id = wikidata.get_musicbrainz_id(name)
    if spotify_id is None and musicbrainz_id is not None:
        spotify_id = musicbrainz.get_spotify_id(musicbrainz_id)

    if (spotify_id != "" and spotify_id is not None):
        albums = spotify.get_artist_albums(spotify_id)
        related_artists = spotify.get_related_artists(spotify_id)
        artist_data = spotify.get_artist(spotify_id)
        popularity = artist_data['popularity']
        follower_total = artist_data['followers']['total']
        if (spotify_id != ""):
            tracks = spotify.get_top_tracks(spotify_id)
            track_names = [track[0] for track in tracks]
            track_ids = [track[1] for track in tracks]
            track_urls = [track[2] for track in tracks]
            danceability, energy = spotify.get_artist_features(track_ids)

    # This abstract will be constructed using the available information
    abstract = ''

    extended_referall = referall


    if (spotify_id != ""):
        if(genres is not None):
            if(len(genres) > 0):
                extended_referall = "a{}{} {}".format(popularityString(popularity), genres[0], referall)

    if time_period is not None:
        if len(time_period) > 0:
            abstract += '{}, {}, started performing in {}. '.format(name,extended_referall,time_period[0][0:4])
        else:
            abstract += 'It is unclear when {}, {}, started performing. '.format(name,extended_referall)

    if(danceability is not None):
        if(danceability > 0.5):
            if(danceability > 0.8):
                danceableString = "extremely danceable"
            else:
                danceableString = "very danceable"
        else:
            danceableString = "not very danceable"

    if(energy is not None):
        if(energy > 0.5):
            if(energy > 0.8):
                energyString = "extremely energetic"
            else:
                energyString = "very energetic"
        else:
            energyString = "not very energetic"

    if(energyString is not None and danceableString is not None):
        abstract += 'The {} is known for its {}, {} music. '.format(referall, energyString, danceableString)

    if track_names is not None and track_urls is not None:
        track_name_url = []
        for track in range(len(track_names)):
            track_name_url.append('{} ({})'.format(track_names[track], track_urls[track]))

        if len(track_name_url) > 1:
            abstract += 'Top tracks of the {} are {} and {}. '.format(referall, ", ".join(track_name_url[:2]), track_name_url[-1])
        else:
            abstract += 'The top track of the {} is {}. '.format(referall, track_name_url[0])

    if members is not None:
        if len(members) > 1:
            abstract += 'Members of the band are {} and {}. '.format(", ".join(members[:-1]),members[-1])
        else:
            abstract += '{} is the band member. '.format(", ".join(members[0]))

    if albums is not None:
        if len(albums) > 1:
            abstract += 'Some albums of the {} are {} and {}. '.format(referall, ", ".join(albums[:2]),albums[-1])
        else:
            abstract += 'An album of the {} is {}. '.format(referall, albums[0])

    if related_artists is not None:
        if len(related_artists) > 1:
            abstract += 'Related artists are {} and {}. '.format(", ".join(related_artists[:2]),related_artists[-1])
        else:
            abstract += 'A related artist is {}. '.format(referall, related_artists[0])

    return abstract


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for. Should be in quotes.')
    args = parser.parse_args()
    result = main(args.query)
    print(result)

