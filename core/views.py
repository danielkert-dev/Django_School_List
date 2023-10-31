from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.decorators import login_required
from . import forms

@login_required
def index(request):

    if request.user.is_superuser:
        listContent = models.List.objects.all()
    else:
        listContent = models.List.objects.filter(user=request.user)


    content = {
        'list': listContent,
        'form': forms.ListForm(user=request.user),
    }
    return render(request, 'core/index.html', content)

def about(request):
    return render(request, 'core/about.html')



@login_required
def add_list(request):
    if request.method == 'POST':
        form = forms.ListForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            print("Data saved successfully.")
            return redirect('index')
        else:
            print("Form is not valid. Form errors:", form.errors)

    if request.user.is_superuser:
        listContent = models.List.objects.all()
    else:
        listContent = models.List.objects.filter(user=request.user)

    content = {
        'list': listContent,
        'form': form,
    }
    return render(request, 'core/index.html', content)


def delete_list(request, list_id):
    models.List.objects.get(id=list_id).delete()
    return redirect('index')
