from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.utils import generateSearchQuery, executeQueryJSON
from lists.rdf_dao import NetflixShowSearchResult


def home_page(request):
    error = None
    show_search_result = None
    search_done = False

    if request.method == 'POST':
        search_done = True
        keyword = request.POST['show_search']
        query = generateSearchQuery(keyword)
        try:
            result = executeQueryJSON(query)
            show_search_result = NetflixShowSearchResult.fromSearchJSONResult(result)
        except Error as err:
            if hasattr(err, 'message'):
                error = err.message
            else:
                error = str(err)
    return render(request, 'home.html', {'show_search_result': show_search_result, 'search_done': search_done, 'error': error})
