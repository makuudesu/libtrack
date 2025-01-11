from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages 
from django.http import HttpResponse 
from django.utils import timezone  
from django.db.models import Q  # For complex queries
from django.db.models import Count
from datetime import timedelta
from collections import Counter
from collections import defaultdict
from .models import Book, Borrower, Transaction
from .forms import BookForm, BorrowerForm, TransactionForm




# Dashboard
def dashboard(request):
    # Annotate Borrower count with the number of transactions (borrowed books)
    borrowers = Borrower.objects.annotate(borrow_count=Count('transaction'))

    # Prepare the borrower count data (borrowers with 0, 1, 2 times borrowed)
    borrower_counts = Counter([borrower.borrow_count for borrower in borrowers])

    # Prepare the transaction counts by date (e.g., January 1, January 2, etc.)
    transactions = Transaction.objects.all()
    transaction_counts = defaultdict(int)  # Use defaultdict to handle missing dates
    for transaction in transactions:
        date_str = transaction.borrowed_date.strftime('%B %d')
        transaction_counts[date_str] += 1

    # Prepare the book availability data (Available, Borrowed)
    available_books = Book.objects.filter(is_available=True).count()  # Books that are available
    borrowed_books = Book.objects.filter(is_available=False).count()  # Books that are borrowed

    # Prepare the total counts
    total_books = Book.objects.count()
    total_borrowers = borrowers.count()
    total_transactions = transactions.count()

    # Prepare the context with all the necessary data
    context = {
        'borrower_count_data': dict(borrower_counts),
        'daily_transactions_data': dict(transaction_counts),
        'availability_data': {
            'available': available_books,
            'borrowed': borrowed_books,
        },
        'total_books': total_books,
        'total_borrowers': total_borrowers,
        'total_transactions': total_transactions,
    }

    return render(request, 'dashboard.html', context)


# Book List
def book_list(request):
    search_query = request.GET.get('search', '')  # Get the search query from the GET request
    if search_query:
        # Filter books by title or author based on the search query (case-insensitive)
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(author__icontains=search_query)
    else:
        books = Book.objects.all()  # If no search query, return all books
    
    return render(request, 'book_list.html', {'books': books})

# Add Book
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'add_book.html', {'form': form})

# Edit Book
def edit_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            edited_book = form.save(commit=False)

            # Determine availability based on transactions
            is_borrowed = Transaction.objects.filter(book=book, is_returned=False).exists()
            edited_book.is_available = not is_borrowed
            edited_book.save()
            
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'add_book.html', {'form': form, 'book': book})

# Delete Book
def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('book_list')





# Borrower LIst
def borrower_list(request):
    search_query = request.GET.get('search', '')
    
    # Annotate each borrower with the borrow count
    borrowers = Borrower.objects.annotate(borrow_count=Count('transaction'))

    if search_query:
        # Filter by first name, last name, email, or borrow count
        borrowers = borrowers.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(borrow_count__icontains=search_query)  # Allows searching by borrow count
        )

    return render(request, 'borrower_list.html', {'borrowers': borrowers})


# Add Borrower
def add_borrower(request):
    if request.method == 'POST':
        form = BorrowerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('borrower_list')
        else:
            return render(request, 'add_borrower.html', {'form': form})  # Pass the form back on invalid
    else:
        form = BorrowerForm()
    return render(request, 'add_borrower.html', {'form': form})


# Edit Borrower
def edit_borrower(request, id):
    borrower = get_object_or_404(Borrower, id=id)
    if request.method == 'POST':
        form = BorrowerForm(request.POST, instance=borrower)
        if form.is_valid():
            form.save()
            return redirect('borrower_list')
    else:
        form = BorrowerForm(instance=borrower)
    return render(request, 'add_borrower.html', {'form': form, 'borrower': borrower})

# Delete Borrower
def delete_borrower(request, id):
    borrower = get_object_or_404(Borrower, id=id)
    borrower.delete()
    return redirect('borrower_list')




# Transaction List
def transaction_list(request):
    transactions = Transaction.objects.select_related('borrower', 'book')  # Fetch related borrower and book data

    # Search functionality (search by book title, borrower, borrowed date)
    search_query = request.GET.get('search', '')  # Get search query from URL
    if search_query:
        transactions = transactions.filter(
            Q(book__title__icontains=search_query) |
            Q(borrower__first_name__icontains=search_query) |
            Q(borrower__last_name__icontains=search_query) |
            Q(borrowed_date__icontains=search_query)  # Search by borrowed date
        )

    # Annotate each transaction with return status
    for transaction in transactions:
        if transaction.returned_date:
            deadline = transaction.borrowed_date + timedelta(days=7)
            transaction.return_status = "Late" if transaction.returned_date > deadline else "On-Time"
        else:
            transaction.return_status = "Not Returned"

    return render(request, 'transaction_list.html', {'transactions': transactions, 'search_query': search_query})

# Add Transaction
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            
            # Update the book's availability
            if transaction.book.is_available:  # Ensure the book is available
                transaction.book.is_available = False
                transaction.book.save()
                transaction.save()
                return redirect('transaction_list')
            else:
                # Handle the case where the book is already borrowed
                messages.error(request, "This book is already borrowed.")
                return redirect('add_transaction')
    else:
        form = TransactionForm()
    return render(request, 'add_transaction.html', {'form': form})

# Edit Transaction
def edit_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'add_transaction.html', {'form': form, 'transaction': transaction})

# Delete Transaction
def delete_transaction(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    transaction.delete()
    return redirect('transaction_list')




# Mark as Returned
def mark_as_returned(request, id):
    transaction = get_object_or_404(Transaction, id=id)
    
    if transaction.is_returned:
        return HttpResponse("This book has already been returned.", status=400)

    # Mark the transaction as returned
    transaction.is_returned = True
    transaction.returned_date = timezone.now()  # Record the return date
    transaction.save()

    # Update the book's availability
    book = transaction.book
    book.is_available = True
    book.save()

    return redirect('transaction_list')

# Splash Screen
def splash_screen(request):
    return render(request, 'splash.html')

