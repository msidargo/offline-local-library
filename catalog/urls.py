from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include, path



urlpatterns = [
    path('', views.index, name = 'index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    path('borrowed/', views.AllBorrowedBooksListView.as_view(), name='all-borrowed'),
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name = 'renew_book_librarian'),

    path('author/create/', views.AuthorCreate.as_view(), name='author_create'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author_update'),
    path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author_delete'),

    path('book/create/', views.BookCreate.as_view(), name='book_create'),
    path('book/<int:pk>/update/', views.BookUpdate.as_view(), name='book_update'),
    path('book/<int:pk>/delete/', views.BookDelete.as_view(), name='book_delete'),

    path('bookinst/create/', views.BookInstanceCreate.as_view(), name='bookinst_create'),
    path('bookinst/<uuid:pk>/bookinst_update/', views.BookInstanceUpdate.as_view(), name='bookinst_update'),
    path('bookinst/<uuid:pk>/bookinst_delete/', views.BookInstanceDelete.as_view(), name='bookinst_delete'),

    path('bookinst/', views.BookInstanceListView.as_view(), name='bookinst'),
    path('bookinst/<uuid:pk>/', views.BookInstanceDetailView.as_view(), name='bookinst-detail'),
]