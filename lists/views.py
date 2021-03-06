from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    if request.method == 'GET':
        return render(request, 'list.html', {'list': list_})
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        error = 'You can\'t have an empty list item'
        return render(request, 'list.html', {'list': list_, 'error': error})
    item.save()
    return redirect(list_)


def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
    except ValidationError:
        list_.delete()
        error = 'You can\'t have an empty list item'
        return render(request, 'home.html', {'error': error})
    item.save()
    return redirect(list_)
