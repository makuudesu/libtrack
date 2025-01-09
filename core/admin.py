from django.contrib import admin
from .models import Borrower, Book, Transaction

# Register Borrower
class BorrowerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')  # Fields to display in the admin list view
    search_fields = ('first_name', 'last_name', 'email')  # Add search functionality

# Register Book
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'is_available')  # Fields to display
    search_fields = ('title', 'author')  # Add search functionality
    list_filter = ('is_available',)  # Add filter for availability

# Register Transaction
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('book', 'borrower', 'borrowed_date', 'returned_date', 'is_returned')
    list_filter = ('is_returned', 'borrowed_date')  # Filter by returned status and borrow date
    search_fields = ('book__title', 'borrower__first_name', 'borrower__last_name')  # Search for related fields

admin.site.register(Borrower, BorrowerAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Transaction, TransactionAdmin)
