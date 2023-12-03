from django.shortcuts import render, redirect
from .forms import RegisterUserForm


def create_user(request):

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            print("its valid")
            form.save()
            return redirect('login/')
        else:
            print("form is not valid")
            print(form.errors)
    else:
        form = RegisterUserForm()
        context = {"form": form}
        return render(request, 'accounts/create_user.html', context)
