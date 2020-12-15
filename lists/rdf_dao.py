class NetflixShowSearchResult:
    def __init__(self, title, casts, director, description):
        self.title = title
        self.casts = casts
        self.director = director
        self.description = description
    
    @staticmethod
    def fromSearchJSONResult(result):
        searchResultList = []
        for show in result['results']['bindings']:
            casts = show['casts']['value'].split(', ')
            searchResultList.append(NetflixShowSearchResult(
                show['title']['value'],
                casts,
                show['director']['value'],
                show['description']['value']
            ))
        return searchResultList
