from django.urls import path

from . import views

app_name = 'quotes'

urlpatterns = [
    path('', views.main, name='main'),
    path('<int:page>', views.main, name='main_paginate'),
    path('quote/<int:quote_id>', views.quote, name='quote'),
    path('tag/<slug:tag_name>/<int:page>', views.quotes_tag, name='quotes_tag'),
    path('tag/<slug:tag_name>/page/<int:page>', views.quotes_tag, name='quotes_tag'),
    path('author/<int:author_id>', views.author, name='author'),
    path('author-view/', views.author_view, name='author-view'),
    path('author-view/<int:page>', views.author_view, name='author-view'),
    path('author-add/', views.author_add, name='author-add'),
    path('quote-add/', views.quote_add, name='quote-add'),
    path('quote-view/', views.quote_view, name='quote-view'),
    path('quote-view/<int:page>', views.quote_view, name='quote-view'),
]