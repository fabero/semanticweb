import argparse
from Spotify import *
from DBPedia import *

dbpedia = DBPedia()
spotify = Spotify()


def main(parseargs):
    # Convert query to DBpedia format
    artist = '_'.join(parseargs.query.title().split())

    hometown = dbpedia.get_hometown(artist)

    # This abstract will be constructed using the available information
    abstract = '{}'.format(parseargs.query.title())

    # Add something to the abstract for every variable that was found
    if hometown:
        # @todo: find a way do discriminate bands and individuals
        abstract += ' is a band from {}'.format(hometown)

    # if bandmembers:

    # if started_in:

    # etcetera

    print(abstract)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for.')
    args = parser.parse_args()
    main(args)
