from django.contrib import admin
from django.urls import path, include
from core import views

urlpatterns = [
    # Root URL
    path('', views.splash_screen, name='splash_screen'),
    path('dashboard/', views.dashboard, name='dashboard'),

    # Book URLs
    path('books/add/', views.add_book, name='add_book'),
    path('books/edit/<int:id>/', views.edit_book, name='edit_book'),
    path('books/delete/<int:id>/', views.delete_book, name='delete_book'),
    path('books/', views.book_list, name='book_list'),

    # Borrower URLs
    path('borrowers/add/', views.add_borrower, name='add_borrower'),
    path('borrowers/edit/<int:id>/', views.edit_borrower, name='edit_borrower'),
    path('borrowers/delete/<int:id>/', views.delete_borrower, name='delete_borrower'),
    path('borrowers/', views.borrower_list, name='borrower_list'),

    # Transaction URLs
    path('transactions/add/', views.add_transaction, name='add_transaction'),
    path('transactions/edit/<int:id>/', views.edit_transaction, name='edit_transaction'),
    path('transactions/delete/<int:id>/', views.delete_transaction, name='delete_transaction'),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('transactions/mark-returned/<int:id>/', views.mark_as_returned, name='mark_as_returned'),

    path('__reload__/', include('django_browser_reload.urls')),
    path('admin/', admin.site.urls),
]
