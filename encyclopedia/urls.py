from django.urls import path
from . import views

app_name="encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("search/", views.search, name="search"),
    path('new_entry/', views.new_entry, name='new_entry'),
    path('edit_page/', views.edit_page, name='edit_page'),
    path("random_page", views.random_page, name="random_page"),
]

