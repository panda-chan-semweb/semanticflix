from SPARQLWrapper import SPARQLWrapper, JSON, JSONLD

prefixes = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX netflix: <http://netflix.com/>
'''


def executeQueryJSON(query):
    '''
    Method used to execute query for SELECT and ASK
    SELECT return a JSON with the data, ASK return a JSON with boolean in key 'boolean'
    '''
    sparql = SPARQLWrapper('https://fuseki.cahyanugraha12.site/semweb/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        result = sparql.query()
        return result.convert()
    except Error as err:
        return err

def executeQueryJSONLD(query):
    '''
    Method used to execute query for DESCRIBE
    DESCRIBE return a JSONLD describing the resource
    '''
    sparql = SPARQLWrapper('https://fuseki.cahyanugraha12.site/semweb/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSONLD)

    try:
        result = sparql.query()
        return result.convert()
    except Error as err:
        return err

def generateSearchQuery(keyword):
    return prefixes + '''
        SELECT ?title (GROUP_CONCAT(?cast;SEPARATOR=", ") AS ?casts) ?director ?description
        WHERE {
            ?netflixShow rdf:type ?type ;
                        rdfs:label ?title ;
                        netflix:cast ?cast ;
                        netflix:director ?director ;
                        netflix:description ?description .
            ?type rdfs:subClassOf netflix:netflix_show .
            FILTER (regex(?title, "%s", "i") || regex(?cast, "%s", "i") || regex(?director, "%s", "i") || regex(?description, "%s", "i"))
        }
        GROUP BY ?title ?director ?description
    ''' % (keyword, keyword, keyword, keyword)