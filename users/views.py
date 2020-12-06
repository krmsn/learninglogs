from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

# GET means this is the first time a view is loading, and we require an empty form.
# POST means that we want to take that info (filled out) and post it/save it to the database.

def register(request):
    if request.method != 'POST':
        form = UserCreationForm()
    else:
        form = UserCreationForm(data = request.POST)

        if form.is_valid():
            new_user = form.save()
            # This line will automatically log them in after they sign up.
            login(request, new_user)
            return redirect('learning_logs:index')

    context = {'form':form}
    return render(request, 'registration/register.html', context)

