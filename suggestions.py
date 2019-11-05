import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()


def suggestions(query):
    name = query.title()

    print('Fetching suggestions for: ')
    print(name)

    artists = spotify.search(name)
    return artists
