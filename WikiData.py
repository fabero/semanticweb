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

        if results is not None:
            return results[0]['finalBandLabel']['value']
        return None


