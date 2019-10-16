import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()


def main(parseargs):
    name = parseargs.query.title()

    label = wikidata.get_label(name)

    genres = wikidata.get_genres(name)

    # This abstract will be constructed using the available information
    abstract = '{}. \n'.format(name)

    # Add something to the abstract for every variable that was found
    # if hometown:
    #     # @todo: find a way do discriminate bands and individuals
    #     abstract += ' is a band from {}'.format(hometown)

    # if bandmembers:

    # if started_in:

    if genres is not None:
        if len(genres) > 1:
            abstract += 'The genres of the band are {} and {}.'.format(", ".join(genres[:-1]),genres[-1])
        else:
            abstract += 'The genre of the band is {}.'.format(genres[0])

    # etcetera

    print(abstract)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for. Should be in quotes.')
    args = parser.parse_args()
    main(args)
