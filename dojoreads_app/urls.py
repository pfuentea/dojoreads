from django.urls import path
from . import views, auth
urlpatterns = [
    path('', views.index),
    path('registro', auth.registro),
    path('login', auth.login),
    path('logout', auth.logout),
    path('books', views.index),
    path('books/add', views.books_add), 
    path('books/<int:book_id>', views.books),
    path('users/<int:user_id>', views.users),
    path('review/<int:review_id>/destroy', views.review_destroy), 
    path('review/<int:book_id>/add', views.review_add),
]
