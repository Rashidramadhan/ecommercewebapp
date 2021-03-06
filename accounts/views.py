
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib import messages



def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Your account has been created..you can now login')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'registration/signup.html', {'form': form})



