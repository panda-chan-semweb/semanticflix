from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.


def home_page(request):
    error = None

    if request.method == 'POST':
        item = Item.objects.create(text=request.POST['item_text'])
        try:
            item.full_clean()
            item.save()
            return redirect('/')
        except ValidationError:
            item.delete()
            error = "You can't have an empty list item"

    items = Item.objects.all()
    comment = get_comment(items)
    return render(request, 'home.html', {'items': items, 'error': error, 'comment': comment})

def get_comment(items):
    items_counter = len(items)
    comment = 'Astaghfirullah KERJAIN'
    if items_counter == 0:
        comment = 'Saatnya tidur YEY'
    elif items_counter < 5:
        comment = 'Duh kerjain tuh lumayan'
    return comment