from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.utils import generateSearchQuery, executeQueryJSON, show_type_list_query, rating_list_query
from lists.rdf_dao import ShowType, Rating, NetflixShowSearchResult

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
