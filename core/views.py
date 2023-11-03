from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.decorators import login_required
from . import forms
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView # Import ListView from the correct module
from django.utils.decorators import method_decorator
from django.contrib import messages
# Mixins
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q


@method_decorator(login_required, name='dispatch')
class PostList(LoginRequiredMixin, ListView):
    model = models.List
    template_name = 'core/index.html'
    context_object_name = 'list'
    paginate_by = 5  # Set the number of items per page
    page_kwarg = 'p'  # Use ?p= for pagination

    def get_queryset(self):
        queryset = models.List.objects.all()  # Start with all items
        search_query = self.request.GET.get('search')
        if search_query:
            # Modify the queryset to filter by search query in title, description, or user
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(user__username__icontains=search_query)
            )
        queryset = queryset.order_by('-date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get(self.page_kwarg)

        # Pass the original queryset to the Paginator
        queryset = self.get_queryset()
        paginator = Paginator(queryset, self.paginate_by)

        try:
            items = paginator.page(page)
        except (PageNotAnInteger, EmptyPage):
            items = paginator.page(1)

        context['list'] = items
        context['form'] = forms.ListForm(user=self.request.user)
        return context

    
@method_decorator(login_required, name='dispatch')
class PostDetail(DetailView):
    model = models.List
    template_name = 'core/detail.html'
    context_object_name = 'list'

@method_decorator(login_required, name='dispatch')
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = models.List
    template_name = 'core/edit.html'
    forms_class = forms.ListForm
    fields = ['title', 'description', 'user']
    success_url = reverse_lazy('index')
    
    def form_valid(self, form):
        self.object = form.save()
        messages.success(self.request, 'Object updated successfully.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ListForm(user=self.request.user, instance=self.object)
        return context
    
    
@method_decorator(login_required, name='dispatch')
class PostCreate(LoginRequiredMixin, CreateView):
    model = models.List
    template_name = 'core/create.html'
    forms_class = forms.ListForm
    #User = request user
    fields = ['title', 'description', 'user']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = forms.ListForm(user=self.request.user)
        return context
    

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
            messages.success(request, 'Object saved successfully.')
            return redirect('index')
        else:
            messages.error(request, 'Something went wrong.'.format(form.errors))

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
    messages.success(request, 'Object deleted successfully.')
    return redirect('index')
