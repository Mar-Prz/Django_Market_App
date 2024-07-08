from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .forms import NewItemForm, EditItemForm
from .models import Category, Item

# Create your views here.

def items(request):
    query = request.GET.get('query', '') #makes url query=searched item eg.teddy
    category_id = request.GET.get('category', 0) #tries to retrieve the value associated with the given key from the dictionary. In this case, the key is 'category'. The second argument to .get(), here 0, is the default value returned if the key is not found in the dictionary
    categories = Category.objects.all()
    items = Item.objects.filter(is_sold=False)

    if category_id:
        items = items.filter(category_id=category_id)

    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query)) #if we have a query we filter the items to show only the ones that we searched or it is in the description

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'category_id': int(category_id)
    })

def detail(request, pk): # accepts two parameters: request (the HTTP request) and pk (short for "primary key", which is used to identify a specific item).
    item = get_object_or_404(Item, pk=pk) #This line tries to retrieve an Item object from the database with the primary key equal to the value of pk. get_object_or_404 is a helper function provided by Django. It attempts to fetch an object from the database, but if no matching object is found, it raises an HTTP 404 error, meaning "Not Found".
    # first pk is the pk from the model itself and the second pk is the pk from the url
    related_items = Item.objects.filter(category=item.category, is_sold=False).exclude(pk=pk)[0:3]

    return render(request, 'item/detail.html', {
        'item': item,
        'related_items': related_items
     })

@login_required
def new(request): #we want django to require that we are logged in to access this, import login_required at the top
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False) #saves form data but doesnt commit changes yet
            item.created_by = request.user
            item.save()

            return redirect('item:detail', pk=item.id)
    else:       
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New Item',
    })

@login_required
def edit(request, pk): #we want django to require that we are logged in to access this, import login_required at the top
    item = get_object_or_404(Item, pk=pk, created_by=request.user)

    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
           form.save()

           return redirect('item:detail', pk=item.id)
    else:       
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit Item',
    })

@login_required
def delete(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    item.delete()

    return redirect('dashboard:index')