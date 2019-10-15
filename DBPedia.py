from SPARQLWrapper import SPARQLWrapper, JSON


class DBPedia:
    """Interacts with DBPedia"""
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.sparql.setReturnFormat(JSON)
        self.prefixes = """
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX wd: <http://www.wikidata.org/entity/>
        """

    def get_hometown(self, artist):
        self.sparql.setQuery(self.prefixes + """
        SELECT ?hometownLabel 
            WHERE {
            <http://dbpedia.org/resource/""" + artist + """> <http://dbpedia.org/ontology/hometown> ?hometown .
            ?hometown rdfs:label ?hometownLabel filter (lang(?hometownLabel) = "en").
            }
        """)

        results = self.sparql.query().convert()['results']['bindings']

        if results is not None:
            return results[0]['hometownLabel']['value']
        return None

