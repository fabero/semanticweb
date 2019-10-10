from SPARQLWrapper import SPARQLWrapper, JSON


class DBPedia:
    """Interacts with DBPedia"""
    def __init__(self):
        self.sparql = SPARQLWrapper("http://dbpedia.org/sparql")
        self.sparql.setReturnFormat(JSON)
        print("DBPedia started.")

    def get_hometown(self, artist):
        self.sparql.setQuery("""
        SELECT ?hometownLabel 
            WHERE {
            <http://dbpedia.org/resource/""" + artist + """> <http://dbpedia.org/ontology/hometown> ?hometown .
            ?hometown <http://www.w3.org/2000/01/rdf-schema#label> ?hometownLabel .
            }
        """)

        # List of hometowns in multiple languages
        results = self.sparql.query().convert()['results']['bindings']
        if results is not None:
            for item in results:
                # Return the English version of hometown
                if item['hometownLabel']['xml:lang'] == 'en':
                    return item['hometownLabel']['value']
        return None

