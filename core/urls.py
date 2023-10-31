from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('add-list/', views.add_list, name='add_list'),
    path('delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
]