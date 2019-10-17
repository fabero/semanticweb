from SPARQLWrapper import SPARQLWrapper, JSON


class WikiData:
    """Interacts with WikiData"""
    def __init__(self):
        self.sparql = SPARQLWrapper("https://query.wikidata.org/bigdata/namespace/wdq/sparql")
        self.sparql.setReturnFormat(JSON)
        self.prefixes = """
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        """

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

    def get_genres(self, band):
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

    def get_members(self, band):
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
