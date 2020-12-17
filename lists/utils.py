from SPARQLWrapper import SPARQLWrapper, JSON, JSONLD

prefixes = '''
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX netflix: <http://netflix.com/>
'''

show_type_list_query = prefixes + '''
    SELECT ?uri ?label
    WHERE {
        ?uri rdfs:subClassOf netflix:netflix_show ;
                rdfs:label ?label .
    }
'''

rating_list_query = prefixes + '''
    SELECT ?uri ?label
    WHERE {
        ?uri rdf:type netflix:rating_type ;
                rdfs:label ?label .
    }
'''

def executeQueryJSON(query):
    '''
    Method used to execute query for SELECT and ASK on RDF database
    SELECT return a JSON with the data, ASK return a JSON with boolean in key 'boolean'
    '''
    sparql = SPARQLWrapper('https://fuseki.cahyanugraha12.site/semweb/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        result = sparql.query()
        return result.convert()
    except Exception as err:
        return err

def executeQueryJSONLD(query):
    '''
    Method used to execute query for DESCRIBE on RDF database
    DESCRIBE return a JSONLD describing the resource
    '''
    sparql = SPARQLWrapper('https://fuseki.cahyanugraha12.site/semweb/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSONLD)

    try:
        result = sparql.query()
        return result.convert()
    except Exception as err:
        return err

def executeQueryJSONDBPedia(query):
    '''
    Method used to execute query for SELECT and ASK on DBPedia
    SELECT return a JSON with the data, ASK return a JSON with boolean in key 'boolean'
    '''
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)

    try:
        result = sparql.query()
        return result.convert()
    except Exception as err:
        return err

def executeQueryJSONLDDBPedia(query):
    '''
    Method used to execute query for DESCRIBE on DBPedia
    DESCRIBE return a JSONLD describing the resource
    '''
    sparql = SPARQLWrapper('http://dbpedia.org/sparql')
    sparql.setQuery(query)
    sparql.setReturnFormat(JSONLD)

    try:
        result = sparql.query()
        return result.convert()
    except Exception as err:
        return err

def generateSearchQuery(keyword, release_year = None, rating = None, show_type = None):
    query = prefixes + '''
        SELECT ?type_label ?title (GROUP_CONCAT(?cast;SEPARATOR=", ") AS ?casts) ?director ?description (str(?release_year) as ?release_year_value) ?rating_label
        WHERE {
            ?netflixShow rdf:type ?type ;
                        netflix:title ?title ;
                        netflix:cast ?cast ;
                        netflix:director ?director ;
                        netflix:description ?description ;
                        netflix:release_year ?release_year ;
                        netflix:rating ?rating .
            ?rating rdfs:label ?rating_label .
            ?type rdfs:subClassOf netflix:netflix_show ;
                    rdfs:label ?type_label .
    ''' 
    if release_year:
        query = query + '''
            FILTER (?release_year = "%s"^^xsd:gYear)
        ''' % (release_year)
    
    if rating:
        query = query + '''
            FILTER (?rating = <%s>)
        ''' % (rating)

    if show_type:
        query = query + '''
            FILTER (?type = <%s>)
        ''' % (show_type)

    query = query + '''
            FILTER (regex(?title, "%s", "i") || regex(?cast, "%s", "i") || regex(?director, "%s", "i") || regex(?description, "%s", "i"))
        }
        GROUP BY ?type_label ?title ?director ?description ?release_year ?rating_label
    ''' % (keyword, keyword, keyword, keyword)

    return query

def generatePersonQuery(personName):
    ask_query = prefixes + 'ASK  { ?x foaf:name  "%s"@en }' % personName
    describe_query = prefixes + 'DESCRIBE ?x WHERE { ?x foaf:name "%s"@en  ; rdf:type dbo:Person } LIMIT 1' % personName
    return {'ask': ask_query, 'describe': describe_query}
