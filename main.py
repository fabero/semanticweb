import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()


def main(parseargs):
    name = parseargs.query.title()

    label = wikidata.get_label(name)
    print(label)

    # This abstract will be constructed using the available information
    abstract = '{}'.format(name)

    # Add something to the abstract for every variable that was found
    # if hometown:
    #     # @todo: find a way do discriminate bands and individuals
    #     abstract += ' is a band from {}'.format(hometown)

    # if bandmembers:

    # if started_in:

    # etcetera


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for. Should be in quotes.')
    args = parser.parse_args()
    main(args)
