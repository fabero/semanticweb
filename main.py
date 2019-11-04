import argparse
from Spotify import *
from WikiData import *
from MusicBrainz import *

wikidata = WikiData()
spotify = Spotify()
musicbrainz = MusicBrainz()

def logArrayToTrace(arr, tracel, strname):
    if arr is not None and (len(arr) > 0):
        tracel.append('Found {}: {} and {}.'.format(strname, ", ".join(arr[:-1]), arr[-1]))
    else:
        tracel.append('No {} found.'.format(strname))
    tracel.append('---')

def popularityString(popularity):
    result = " "
    if popularity is not None:
        if popularity < 50:
            if popularity > 30:
                result = " medium popular "
            else:
                result = " not so popular "
        else:
            if popularity > 80:
                result = "n extremely popular "
            else:
                result = " popular "
    return result


def main(query, returnHTML=False):
    if query[0].isupper():
        name = query
    else:
        name = query.title()

    tracelog = ['Fetching Wikidata for query \'{}\'...'.format(name), '---']

    is_artist = wikidata.check_if_artist(name)

    tracelog.append('Checking whether query is artist or band...')
    if is_artist:
        tracelog.append('{} is an artist.'.format(name))
    else:
        tracelog.append('{} is a band.'.format(name))
    tracelog.append('---')
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
    instruments = None

    if (is_artist):
        referall = "artist"
        tracelog.append('Fetching artist genres from Wikidata...')
        genres = wikidata.get_artist_genres(name)
        logArrayToTrace(genres, tracelog, 'genres')

        members = None

        tracelog.append('Fetching \'start period\' of artist from Wikidata...')
        time_period = wikidata.get_artist_start_period(name)
        if time_period is not None and len(time_period) > 0:
            tracelog.append('Start period found: {}.'.format(", ".join(time_period)))
        else:
            tracelog.append('No start period found.')
        tracelog.append('---')

        tracelog.append('Fetching \'played instruments\' of artist from Wikidata...')
        instruments = wikidata.get_artist_instruments(name)
        logArrayToTrace(instruments, tracelog, 'instruments')

        spotify_id = wikidata.get_artist_spotify_id(name)
    else:
        referall = "band"
        tracelog.append('Fetching band genres from Wikidata...')
        genres = wikidata.get_band_genres(name)
        logArrayToTrace(genres, tracelog, 'genres')

        tracelog.append('Fetching band members from Wikidata...')
        members = wikidata.get_band_members(name)
        logArrayToTrace(members, tracelog, 'members')

        tracelog.append('Fetching \'start period\' of band from Wikidata...')
        time_period = wikidata.get_band_time_period(name)
        if time_period is not None and len(time_period) > 0:
            tracelog.append('Start period found: {}.'.format(", ".join(time_period)))
        else:
            tracelog.append('No start period found.')
        tracelog.append('---')

        tracelog.append('Fetching spotify ID from Wikidata...')
        spotify_id = wikidata.get_band_spotify_id(name)
        if spotify_id is not None:
            tracelog.append('Spotify ID found: {}'.format(spotify_id))
        else:
            tracelog.append('No spotify ID found.')
        tracelog.append('---')

    # If no Spotify ID is found, try to get it using MusicBrainz
    tracelog.append('Fetching MusicBrainz ID from Wikidata...')
    musicbrainz_id = wikidata.get_musicbrainz_id(name)
    if musicbrainz_id is not None:
        tracelog.append('MusicBrainz ID found: {}'.format(musicbrainz_id))
    else:
        tracelog.append('No MusicBrainz ID found.')
    tracelog.append('---')

    if spotify_id is None and musicbrainz_id is not None:
        tracelog.append('Fetching Spotify ID from MusicBrainz...')
        spotify_id = musicbrainz.get_spotify_id(musicbrainz_id)
        if spotify_id is not None:
            tracelog.append('Spotify ID found: {}'.format(spotify_id))
        else:
            tracelog.append('No Spotify ID found.')
        tracelog.append('---')

    if spotify_id != "" and spotify_id is not None:
        tracelog.append('Fetching albums from Spotify...')
        albums = spotify.get_artist_albums(spotify_id)
        logArrayToTrace(albums, tracelog, 'albums')

        tracelog.append('Fetching related artists from Spotify...')
        related_artists = spotify.get_related_artists(spotify_id)
        logArrayToTrace(related_artists, tracelog, 'related artists')

        tracelog.append('Fetching artist data from Spotify...')
        artist_data = spotify.get_artist(spotify_id)
        if len(artist_data) > 0:
            tracelog.append('Artist data found: {}'.format(artist_data))
        else:
            tracelog.append('No artist data found.')
        tracelog.append('---')

        popularity = None
        if artist_data is not None:
            popularity = artist_data['popularity']
            follower_total = artist_data['followers']['total']
        if spotify_id != "":
            tracks = spotify.get_top_tracks(spotify_id)
            track_names = [track[0] for track in tracks]
            track_ids = [track[1] for track in tracks]
            track_urls = [track[2] for track in tracks]
            danceability, energy = spotify.get_artist_features(track_ids)

    # This abstract will be constructed using the available information
    abstract = ''

    extended_referall = referall

    tracelog.append('Generating referall term for query...')
    if spotify_id != "":
        if genres is not None:
            if len(genres) > 0:
                extended_referall = "a{}{} {}".format(popularityString(popularity), genres[0], referall)

    tracelog.append('Referall terms: \'{}\' and \'{}\''.format(referall, extended_referall))
    tracelog.append('---')

    tracelog.append('Generating summary for query...')
    if time_period is not None:
        if len(time_period) > 0:
            abstract += '{}, {}, started performing in {}. '.format(name, extended_referall, time_period[0][0:4])
    else:
        abstract += 'It is unclear when {}, {}, started performing. '.format(name, extended_referall)

    if danceability is not None:
        if danceability > 0.5:
            if danceability > 0.8:
                danceableString = "extremely danceable"
            else:
                danceableString = "very danceable"
        else:
            danceableString = "not danceable"

    if energy is not None:
        if energy > 0.5:
            if energy > 0.8:
                energyString = "extremely energetic"
            else:
                energyString = "very energetic"
        else:
            energyString = "calm"

    if energyString is not None and danceableString is not None:
        abstract += 'The {} is known for its {}, {} music. '.format(referall, energyString, danceableString)

    if returnHTML:
        if track_names is not None and track_urls is not None:
            track_name_url = []
            for track in range(len(track_names)):
                track_name_url.append(
                    '<a href="{}" target="_blank">{}</a>'.format(track_urls[track], track_names[track]))

            if len(track_name_url) > 1:
                abstract += 'Top tracks of the {} are {} and {}. '.format(referall, ", ".join(track_name_url[:2]),
                                                                          track_name_url[-1])
            else:
                abstract += 'The top track of the {} is {}. '.format(referall, track_name_url[0])
    if returnHTML is not True:
        if track_names is not None:
            if len(track_names) > 1:
                abstract += 'Top tracks of the {} are {} and {}. '.format(referall, ", ".join(track_names[:2]),
                                                                          track_names[-1])
            else:
                abstract += 'The top track of the {} is {}. '.format(referall, track_names[0])

    if members is not None:
        if len(members) > 1:
            abstract += 'Members of the band are {} and {}. '.format(", ".join(members[:-1]), members[-1])
        else:
            abstract += '{} is the band member. '.format(members[0])

    if albums is not None:
        if len(albums) > 1:
            abstract += 'Some albums of the {} are {} and {}. '.format(referall, ", ".join(albums[:2]), albums[-1])
        else:
            abstract += 'An album of the {} is {}. '.format(referall, albums[0])

    if instruments is not None:
        filteredInstruments = []
        isAsinger = False
        for inst in instruments:
            if inst == "voice" or inst == "vocalist":
                isAsinger = True
            else:
                filteredInstruments.append(inst)
        if len(filteredInstruments) > 1:
            if isAsinger:
                abstract += 'Besides singing, the {} has been known to play several instruments, such as {} and {}. '.format(referall,", ".join(filteredInstruments[:-1]), filteredInstruments[-1])
            else:
                abstract += 'The {} has been known to play several instruments, such as {} and {}. '.format(referall,", ".join(filteredInstruments[:-1]), filteredInstruments[-1])
        else:
            if isAsinger:
                abstract += 'Besides singing, the {} has been known to play {}. '.format(referall,filteredInstruments[0])
            else:
                abstract += 'The {} has been known to play {}. '.format(referall,filteredInstruments[0])

    if related_artists is not None:
        if returnHTML:
            artist_url = []
            for artist in range(len(related_artists)):
                artist_url.append(
                    '<a onclick="getSummary(\'{}\')">{}</a>'.format(related_artists[artist], related_artists[artist]))
            if len(related_artists) > 1:
                abstract += 'Related artists are {} and {}. '.format(", ".join(artist_url[:2]), artist_url[-1])
            else:
                abstract += 'A related artist is {}. '.format(artist_url[0])
        else:
            if len(related_artists) > 1:
                abstract += 'Related artists are {} and {}. '.format(", ".join(related_artists[:2]),
                                                                     related_artists[-1])
            else:
                abstract += 'A related artist is {}. '.format(related_artists[0])

    tracelog.append('Outputting summary...')
    tracelog.append('---')

    if len(abstract) < 5:
        tracelog.append('FAIL')
        abstract += 'Unable to find any information related to the query.'
    else:
        tracelog.append('SUCCESS')
    tracelog.append('---')

    if returnHTML:
        tracelog_Html = ''
        traceList = []
        for trace in range(len(tracelog)):
            traceList.append('<li>{}</li>'.format(tracelog[trace]))
        tracelog_Html += "".join(traceList)
        print('Returning HTML output...')
        html = '<p>{}</p>'.format(abstract)
        html += '<a data-toggle="collapse" href="#tracelog" role="button" aria-expanded="false" aria-controls="tracelog">Toggle tracelog</a>'
        html += '<div class="collapse" id="tracelog">'
        html += '<ul class="tracelog">'
        html += tracelog_Html
        html += '</ul>'
        html += '</div>'
        return html
    return abstract


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query', type=str, help='The band or artist to search for. Should be in quotes.')
    args = parser.parse_args()
    result = main(args.query)
    print(result)
