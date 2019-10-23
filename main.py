import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()


def main(parseargs):
    name = parseargs.query.title()

    is_artist = wikidata.check_if_artist(name)

    label = wikidata.get_label(name)

    if(is_artist):
        referall = "artist"
        genres = wikidata.get_artist_genres(name)
        members = None
        time_period = wikidata.get_artist_start_period(name)
    else:
        referall = "band"
        genres = wikidata.get_band_genres(name)
        members = wikidata.get_band_members(name)
        time_period = wikidata.get_band_time_period(name)

    spotify.get_top_tracks('1vCWHaC5f2uS3yhpwWbIA6')

    # This abstract will be constructed using the available information
    abstract = ''

    # Add something to the abstract for every variable that was found
    # if hometown:
    #     # @todo: find a way do discriminate bands and individuals
    #     abstract += ' is a band from {}'.format(hometown)

    # if bandmembers:

    # if started_in:

    if time_period is not None:
        if len(time_period) > 0:
            abstract += '{} started performing in {}. '.format(name,time_period[0][0:4])
        else:
            abstract += 'It is unclear when {} started performing. '.format(name)

    if genres is not None:
        if len(genres) > 1:
            if len(genres) < 3:
                abstract += 'The genres of the {} are {} and {}. '.format(referall,", ".join(genres[:-1]),genres[-1])
            else:
                abstract += 'The genres of the {} are {} and more.'.format(referall,", ".join(genres[:4]))
        else:
            abstract += 'The genre of the {} is {}. '.format(referall, genres[0])

    # etcetera

    if members is not None:
        if len(members) > 1:
            abstract += 'Members of the band are {} and {}. '.format(", ".join(members[:-1]),members[-1])
        else:
            abstract += '{} is the band member. '.format(", ".join(members[0]))

    print(abstract)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for. Should be in quotes.')
    args = parser.parse_args()
    main(args)
