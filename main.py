import argparse
from Spotify import *
from DBPedia import *

dbpedia = DBPedia()
spotify = Spotify()


def main(parseargs):
    # Convert query to DBpedia format
    artist = '_'.join(parseargs.query.title().split())

    hometown = dbpedia.get_hometown(artist)
    print(hometown)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Fetch data on musical artists and bands.')
    parser.add_argument('query',  type=str, help='The band or artist to search for.')
    args = parser.parse_args()
    main(args)
