
from django import forms
from .models import Borrower, Book, Transaction

class BorrowerForm(forms.ModelForm):
    class Meta:
        model = Borrower
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Enter your last name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Enter your email',
            }),
        }



class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Enter the book title',
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Enter the author\'s name',
            }),
            'published_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'mm/dd/yyyy',
            }),
        }


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['book', 'borrower']
        widgets = {
            'book': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Search for a book...',
            }),
            'borrower': forms.Select(attrs={
                'class': 'w-full px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-700 bg-gray-800 text-white placeholder-gray-400',
                'placeholder': 'Search for a borrower...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Filter books to include only those that are available
        self.fields['book'].queryset = Book.objects.filter(
            is_available=True  # Only available books
        ).distinct()
