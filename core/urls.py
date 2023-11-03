from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('detail/<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('edit/<int:pk>/', views.PostUpdate.as_view(), name='edit_list'),
    path('create/', views.PostCreate.as_view(), name='create'),
    path('about/', views.about, name='about'),
    path('add-list/', views.add_list, name='add_list'),
    path('delete-list/<int:list_id>/', views.delete_list, name='delete_list'),
]