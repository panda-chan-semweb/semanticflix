class ShowType:
    def __init__(self, uri, label):
        self.uri = uri
        self.label = label

    @staticmethod
    def fromShowTypeListResult(show_type_list_result):
        show_type_list = []
        for show_type in show_type_list_result['results']['bindings']:
            show_type_list.append(Rating(
                show_type['uri']['value'],
                show_type['label']['value']
            ))
        return show_type_list

class Rating:
    def __init__(self, uri, label):
        self.uri = uri
        self.label = label

    @staticmethod
    def fromRatingListResult(rating_list_result):
        rating_list = []
        for rating in rating_list_result['results']['bindings']:
            rating_list.append(Rating(
                rating['uri']['value'],
                rating['label']['value']
            ))
        return rating_list

class NetflixShowSearchResult:
    def __init__(self, show_type, title, casts, directors, description, release_year, rating, countries):
        self.show_type = show_type
        self.title = title
        self.casts = casts
        self.directors = directors
        self.description = description
        self.release_year = release_year
        self.rating = rating
        self.countries = countries
    
    @staticmethod
    def fromSearchJSONResult(result):
        searchResultList = []
        for show in result['results']['bindings']:
            casts = show['casts']['value'].split(', ')
            directors = show['directors']['value'].split(', ')
            countries = show['countries']['value'].split(', ')
            searchResultList.append(NetflixShowSearchResult(
                show['type_label']['value'],
                show['title']['value'],
                casts,
                directors,
                show['description']['value'],
                show['release_year_value']['value'],
                show['rating_label']['value'],
                countries
            ))
        return searchResultList
