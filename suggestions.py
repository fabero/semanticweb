import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()

def suggestions(query):
    name = query.title()

    print('Fetching suggestions for: ')
    print(name)

    artists = wikidata.search_artists(name)

    return artists

