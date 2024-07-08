from django.shortcuts import render, redirect

from item.models import Category, Item

from .forms import SignupForm

# Create your views here.

#This sets up the frontpage
def index(request): 
    items = Item.objects.filter(is_sold=False)[0:6] #filter out objects that have been sold and we display only the first 6
    categories = Category.objects.all()
    return render(request, 'core/index.html', {
        'categories': categories,
        'items': items,
    })

def contact(request):
    return render(request, 'core/contact.html')

def signup(request):
    if request.method == 'POST': #checks if the current request is a POST request(which means the form has been submitted)
        form = SignupForm(request.POST) #creates an instance of SignupForm and populates it with data from the request

        if form.is_valid(): #checks if the submitted form data is valid
            form.save() #form is saved

            return redirect('/login/') # redirects user to the login page
    else:
        form = SignupForm() #creates a new signup form if form data is invalid
    
    return render(request, 'core/signup.html', {
        'form': form
    })