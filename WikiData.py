from SPARQLWrapper import SPARQLWrapper, JSON

class WikiData:
    """Interacts with WikiData"""
    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql", agent="agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36")
        self.sparql.setReturnFormat(JSON)
        self.prefixes = """
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        """

    # Search query
    def search_artists(self, query):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?item ?itemLabel
                WHERE 
                {
                   ?item wdt:P31 wd:Q5;
                         wdt:P106/wdt:P279* wd:Q639669 ;
                         rdfs:label ?itemLabel filter (lang(?itemLabel) = "en").
                   FILTER regex (?itemLabel, """ +'"^(' + "|".join(query.split()) + ')"' + """).
                }
                LIMIT 100
        """)

        results = self.sparql.query().convert()['results']['bindings']
        suggestions = []
        if len(results) > 0:
            for item in results:
                suggestions.append(item['itemLabel']['value'])
            print(suggestions)
            return suggestions
        return None


    def check_if_artist(self, artist):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?id ?idLabel ?genreLabel
            WHERE
            {
                   ?id wdt:P31 wd:Q5 .
                   ?id wdt:P106/wdt:P279* wd:Q639669 . # artists
                   ?id rdfs:label """ +'"' + artist + '"' + """@en .
                   ?id rdfs:label ?idLabel filter (lang(?idLabel) = "en").
                   ?id wdt:P136 ?genre .
                   ?genre rdfs:label ?genreLabel filter (lang(?genreLabel) = "en").
            }
        """)

        results = self.sparql.query().convert()['results']['bindings']
        if len(results) > 0:
            if len(results[0]) > 0:
                return True
            else:
                return False
        return False

    def get_label(self, label):
        self.sparql.setQuery(self.prefixes + """
        SELECT DISTINCT ?finalBandLabel ?description
        WHERE
            {
                ?band wdt:P279+ wd:Q2088357 .
                ?finalBand wdt:P31 ?band .
                ?finalBand rdfs:label """ +'"' + label + '"' + """@en .
                ?finalBand rdfs:label ?finalBandLabel filter (lang(?finalBandLabel) = "en").
                ?finalBand schema:description ?description filter (lang(?description) = "en").
            }
        """)
        results = self.sparql.query().convert()['results']['bindings']
        if len(results) > 0:
            return results[0]['finalBandLabel']['value']
        return None

    def get_band_spotify_id(self, artist):
        self.sparql.setQuery(self.prefixes + """
               SELECT DISTINCT ?finalBandLabel ?spotify
                    WHERE
                    {
                        ?band wdt:P279+ wd:Q2088357 . # get all subclasses of musical ensamble
                        ?finalBand wdt:P31 ?band .
                        ?finalBand rdfs:label """ +'"' + artist + '"' + """@en .
                        ?finalBand rdfs:label ?finalBandLabel filter (lang(?finalBandLabel) = "en").
                        ?finalBand wdt:P1902 ?spotify.
                    }
           """)
        results = self.sparql.query().convert()['results']['bindings']
        if len(results) > 0:
            for item in results:
                if item['spotify']:
                    return item['spotify']['value']
        return None

    def get_band_genres(self, band):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?finalBandLabel ?finalGenreLabel
                WHERE
                {
                    ?band wdt:P279+ wd:Q2088357 . # get all subclasses of musical ensamble
                    ?finalBand wdt:P31 ?band .
                    ?finalBand rdfs:label """ +'"' + band + '"' + """@en .
                    ?finalBand rdfs:label ?finalBandLabel filter (lang(?finalBandLabel) = "en").
                    ?finalBand wdt:P136 ?genre .
                    ?genre rdfs:label ?finalGenreLabel filter (lang(?finalGenreLabel) = "en").
                }
        """)

        results = self.sparql.query().convert()['results']['bindings']

        genres = []
        if len(results) > 0:
            for item in results:
                if item['finalGenreLabel']:
                    genres.append(item['finalGenreLabel']['value'])
            if len(genres) > 0:
                return genres
        return None

    def get_band_members(self, band):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?finalBandLabel ?members
                WHERE
                {
                    ?band wdt:P279+ wd:Q2088357 . # get all subclasses of musical ensamble
                    ?finalBand wdt:P31 ?band .
                    ?finalBand rdfs:label """ +'"' + band + '"' + """@en .
                    ?finalBand rdfs:label ?finalBandLabel filter (lang(?finalBandLabel) = "en").
                    ?finalBand wdt:P527/rdfs:label ?members filter (lang(?members) = "en").
                }
        """)

        results = self.sparql.query().convert()['results']['bindings']

        band = []
        if len(results) > 0:
            for item in results:
                if item['members']:
                    band.append(item['members']['value'])
            if len(band) > 0:
                return band
        return None

    def get_band_time_period(self, band):
        self.sparql.setQuery(self.prefixes + """
        SELECT DISTINCT ?finalBandLabel ?StartWorkPeriod
            WHERE
            {
                ?band wdt:P279+ wd:Q2088357 . # get all subclasses of musical ensamble
                ?finalBand wdt:P31 ?band .
                ?finalBand rdfs:label """ +'"' + band + '"' + """@en .
                ?finalBand rdfs:label ?finalBandLabel filter (lang(?finalBandLabel) = "en").
                ?finalBand wdt:P2031 ?StartWorkPeriod .
            }
        """)

        results = self.sparql.query().convert()['results']['bindings']

        period = []
        if len(results) > 0:
            for item in results:
                if item['StartWorkPeriod']:
                    period.append(item['StartWorkPeriod']['value'])
            if len(period) > 0:
                return period
        return None

    # Artist queries

    def get_artist_spotify_id(self, artist):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?id ?idLabel ?spotify
                WHERE
                {
                       ?id wdt:P31 wd:Q5 .
                       ?id wdt:P106/wdt:P279* wd:Q639669 . # artists
                       ?id rdfs:label """ +'"' + artist + '"' + """@en .
                       ?id rdfs:label ?idLabel filter (lang(?idLabel) = "en").
                       ?id wdt:P1902 ?spotify
                }
        """)
        results = self.sparql.query().convert()['results']['bindings']
        if len(results) > 0:
            for item in results:
                if item['id']:
                    return item['spotify']['value']
        return None

    def get_artist_genres(self, artist):
        self.sparql.setQuery(self.prefixes + """
            SELECT DISTINCT ?id ?idLabel ?genreLabel
            WHERE
            {
                   ?id wdt:P31 wd:Q5 .
                   ?id wdt:P106/wdt:P279* wd:Q639669 . # artists
                   ?id rdfs:label """ +'"' + artist + '"' + """@en .
                   ?id rdfs:label ?idLabel filter (lang(?idLabel) = "en").
                   ?id wdt:P136 ?genre .
                   ?genre rdfs:label ?genreLabel filter (lang(?genreLabel) = "en").
            }
        """)

        results = self.sparql.query().convert()['results']['bindings']
        genres = []
        if len(results) > 0:
            if len(results[0]) > 0:
                for item in results:
                    if item['genreLabel']:
                        genres.append(item['genreLabel']['value'])
                return genres
            else:
                return None
        return None

    def get_artist_start_period(self, artist):
        self.sparql.setQuery(self.prefixes + """
        SELECT DISTINCT ?id ?idLabel ?StartWorkPeriod
            WHERE
            {
                   ?id wdt:P31 wd:Q5 .
                   ?id wdt:P106/wdt:P279* wd:Q639669 . # artists
                   ?id rdfs:label """ +'"' + artist + '"' + """@en .
                   ?id rdfs:label ?idLabel filter (lang(?idLabel) = "en").
                   ?id wdt:P2031 ?StartWorkPeriod .
                   #Beware that the output maybe not be in English.
            
            }
        """)

        results = self.sparql.query().convert()['results']['bindings']
        period = []
        if len(results) > 0:
            for item in results:
                if item['StartWorkPeriod']:
                    period.append(item['StartWorkPeriod']['value'])
            if len(period) > 0:
                return period
        return None
