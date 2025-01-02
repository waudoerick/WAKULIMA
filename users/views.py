from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from store.models import *
#from .decorators import unauthenticated_user,allowed_user

def register(request):
    """Register a new user."""
    if request.method != 'POST':
        #Display blank registration form.
        form = UserCreationForm()
    else:
        #Process completed form.
        form = UserCreationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save()
          
            customer=Customer.objects.create()
            customer.user= new_user
            customer.name= new_user.username
            customer.save()
            
            #Log the usser in and then redirect to home page.
            login(request, new_user)
           
            return redirect('farmers:index')

    #Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'registration/register.html',context)