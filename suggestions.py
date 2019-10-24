import argparse
from Spotify import *
from WikiData import *

wikidata = WikiData()
spotify = Spotify()

def suggestions(query):
    name = query.title()

    artists = wikidata.search_artists(name)

    return artists

