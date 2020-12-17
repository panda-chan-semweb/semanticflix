from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.utils import generateSearchQuery, generatePersonQuery, generateCountryQuery, show_type_list_query, rating_list_query
from lists.utils import executeQueryJSON, executeQueryJSONDBPedia, executeQueryJSONLDDBPedia 
from lists.rdf_dao import ShowType, Rating, NetflixShowSearchResult
import json

def home_page(request):
    error = None
    show_search_result = None
    search_done = False

    show_type_list_result = executeQueryJSON(show_type_list_query)
    rating_list_result = executeQueryJSON(rating_list_query)
    show_type_list = ShowType.fromShowTypeListResult(show_type_list_result)
    rating_list = Rating.fromRatingListResult(rating_list_result)

    if request.method == 'POST':
        search_done = True
        keyword = request.POST['show_search'] if request.POST['show_search'] != '' else None
        release_year = request.POST['release_year'] if request.POST['release_year'] != '' else None
        rating = request.POST['rating'] if request.POST['rating'] != '' else None
        show_type = request.POST['show_type'] if request.POST['show_type'] != '' else None
        query = generateSearchQuery(keyword, release_year, rating, show_type)
        if keyword != None:
            try:
                result = executeQueryJSON(query)
                show_search_result = NetflixShowSearchResult.fromSearchJSONResult(result)
            except Exception as err:
                if hasattr(err, 'message'):
                    error = err.message
                else:
                    error = str(err)
        else:
            error = "Title, Cast, Director, or Description cannot be empty."
    return render(
        request,
        'home.html', 
        {
            'show_type_list': show_type_list,
            'rating_list': rating_list,
            'show_search_result': show_search_result, 
            'search_done': search_done, 
            'error': error
        }
    )

def linked_person(request):
    error = None
    person_description = None
    person_name = None
    person_gender = None
    person_birth_date = None
    person_birth_place = None
    person_abstract = None
    person_primary_topic = None
    person_subject = None
    person_external_link = None
    person_source = None

    if request.method == 'POST':
        person_ask_query = generatePersonQuery(request.POST['name'])['ask']
        result = executeQueryJSONDBPedia(person_ask_query)
        is_person_available = fromAskJSONResult(result)

        if is_person_available:
            person_describe_query = generatePersonQuery(request.POST['name'])['describe']
            result = executeQueryJSONLDDBPedia(person_describe_query)
            person_description = fromDescribeJSONResult(result)[0]

            try:
                person_name = person_description['http://xmlns.com/foaf/0.1/name'][0]['@value']
            except:
                person_name = None
            
            try:
                person_gender = person_description['http://xmlns.com/foaf/0.1/gender'][0]['@value']
            except:
                person_gender = None
            
            try:
                person_birth_date = person_description['http://dbpedia.org/ontology/birthDate'][0]['@value']
            except:
                person_birth_date = None
            
            try:
                person_birth_place = person_description['http://dbpedia.org/ontology/birthPlace'][0]['@id']
            except:
                person_birth_place = None
            
            try:
                person_primary_topic = person_description['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['@id']
            except:
                person_primary_topic = None
            
            try:
                person_source = person_description['@id']
            except:
                person_source = None

            try:
                person_abstract_all = person_description['http://dbpedia.org/ontology/abstract']
                if person_abstract_all:
                    for data in person_abstract_all:
                        if data['@language'] == 'en':
                            person_abstract = data['@value']
            except:
                person_abstract = None

            try:
                person_external_link_all = person_description['http://dbpedia.org/ontology/wikiPageWikiLink']
                person_external_link = []
                if person_external_link_all:
                    for data in person_external_link_all:
                        person_external_link.append(data['@id'])
            except:
                person_external_link = None

            try:
                person_subject_all = person_description['http://purl.org/dc/terms/subject']
                person_subject = []
                if person_subject_all:
                    for data in person_subject_all:
                        person_subject.append(data['@id'])
            except:
                person_subject = None
        else:
            error = "Information about this person is not available on DBPedia."

    return render(
        request,
        'linked_person.html', 
        {
            'person_name': person_name,
            'person_gender': person_gender,
            'person_birth_date': person_birth_date,
            'person_birth_place': person_birth_place,
            'person_abstract': person_abstract,
            'person_primary_topic': person_primary_topic,
            'person_subject': person_subject,
            'person_external_link': person_external_link,
            'person_source': person_source,
            'error': error,
        }
    )

def linked_country(request):
    error = None
    country_description = None
    country_name = None
    country_founding_date = None
    country_currency = None
    country_capital = None
    country_abstract = None
    country_primary_topic = None
    country_subject = None
    country_external_link = None
    country_source = None

    if request.method == 'POST':
        country_ask_query = generateCountryQuery(request.POST['name'])['ask']
        result = executeQueryJSONDBPedia(country_ask_query)
        is_country_available = fromAskJSONResult(result)

        if is_country_available:
            country_describe_query = generateCountryQuery(request.POST['name'])['describe']
            result = executeQueryJSONLDDBPedia(country_describe_query)
            country_description = fromDescribeJSONResult(result)[0]

            try:
                country_name = country_description['http://xmlns.com/foaf/0.1/name'][0]['@value']
            except:
                country_name = None

            try:
                country_founding_date = country_description['http://dbpedia.org/ontology/foundingDate'][0]['@value']
            except:
                country_founding_date = None

            try:
                country_currency = country_description['http://dbpedia.org/ontology/currency'][0]['@id']
            except:
                country_currency = None

            try:
                country_capital = country_description['http://dbpedia.org/ontology/capital'][0]['@id']
            except:
                country_capital = None
            
            try:
                country_primary_topic = country_description['http://xmlns.com/foaf/0.1/isPrimaryTopicOf'][0]['@id']
            except:
                country_primary_topic = None

            try:
                country_source = country_description['@id']
            except:
                country_source = None

            try:
                country_abstract_all = country_description['http://dbpedia.org/ontology/abstract']
                if country_abstract_all:
                    for data in country_abstract_all:
                        if data['@language'] == 'en':
                            country_abstract = data['@value']
            except:
                country_abstract = None

            try:
                country_external_link_all = country_description['http://dbpedia.org/ontology/wikiPageWikiLink']
                country_external_link = []
                if country_external_link_all:
                    for data in country_external_link_all:
                        country_external_link.append(data['@id'])
            except:
                country_external_link = None

            try:
                country_subject_all = country_description['http://purl.org/dc/terms/subject']
                country_subject = []
                if country_subject_all:
                    for data in country_subject_all:
                        country_subject.append(data['@id'])
            except:
                country_subject = None
        else:
            error = "Information about this country is not available on DBPedia."

    return render(
        request,
        'linked_country.html', 
        {
            'country_name': country_name,
            'country_founding_date': country_founding_date,
            'country_currency': country_currency,
            'country_capital': country_capital,
            'country_abstract': country_abstract,
            'country_primary_topic': country_primary_topic,
            'country_subject': country_subject,
            'country_external_link': country_external_link,
            'country_source': country_source,
            'error': error,
        }
    )

def fromAskJSONResult(result):
    return result['boolean']

def fromDescribeJSONResult(result):
        return json.loads(result.serialize(format='json-ld'))