from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from datetime import date
from datetime import datetime
from django.db.models import Count
from django.db.models import Q
from .forms import BookForm, BorrowerForm, TransactionForm
from .models import Borrower, Book, Transaction

class BorrowerModelTest(TestCase):
    def setUp(self):
        # Create a Borrower instance
        self.borrower = Borrower.objects.create(
            first_name="Anthon",
            last_name="Saguid",
            email="anthon.saguid@example.com"
        )

    def test_borrower_creation(self):
        # Test that the borrower is created successfully
        self.assertEqual(self.borrower.first_name, "Anthon")
        self.assertEqual(self.borrower.last_name, "Saguid")
        self.assertEqual(self.borrower.email, "anthon.saguid@example.com")

    def test_borrower_str_method(self):
        # Test the string representation of the borrower
        self.assertEqual(str(self.borrower), "Anthon Saguid")


class BookModelTest(TestCase):
    def setUp(self):
        # Create a Book instance
        self.book = Book.objects.create(
            title="Sample Book",
            author="Author Name", 
            published_date="2023-01-01",
            is_available=True
        )

    def test_book_creation(self):
        # Test that the book is created successfully
        self.assertEqual(self.book.title, "Sample Book")
        self.assertEqual(self.book.author, "Author Name")
        self.assertEqual(str(self.book.published_date), "2023-01-01")
        self.assertTrue(self.book.is_available)

    def test_book_str_method(self):
        # Test the string representation of the book
        self.assertEqual(str(self.book), "Sample Book")


class TransactionModelTest(TestCase):
    def setUp(self):
        # Create a Borrower and a Book instance
        self.borrower = Borrower.objects.create(
            first_name="Mark",
            last_name="Garcia",
            email="mark.garcia@example.com"
        )
        self.book = Book.objects.create(
            title="Python for Beginners",
            author="Jane Doe",
            published_date="2022-01-01"
        )
        # Create a Transaction instance
        self.transaction = Transaction.objects.create(
            book=self.book,
            borrower=self.borrower,
            is_returned=False
        )

    def test_transaction_creation(self):
        # Test that the transaction is created successfully
        self.assertEqual(self.transaction.book, self.book)
        self.assertEqual(self.transaction.borrower, self.borrower)
        self.assertFalse(self.transaction.is_returned)

    def test_transaction_str_method(self):
        # Test the string representation of the transaction
        self.assertEqual(
            str(self.transaction),
            "Python for Beginners borrowed by Mark Garcia"
        )




class BorrowerFormTest(TestCase):

    def test_form_valid_data(self):
        # Test with valid data
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        }
        form = BorrowerForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid with proper data

    def test_form_invalid_data(self):
        # Test with missing first name (required field)
        form_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        }
        form = BorrowerForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid because first_name is required
        self.assertIn('first_name', form.errors)  # Ensure error for first_name

        # Test with invalid email format
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example',  # Invalid email
        }
        form = BorrowerForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid due to bad email format
        self.assertIn('email', form.errors)  # Ensure error for email

    def test_form_save(self):
        # Test form save functionality (check if form can create a new Borrower)
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
        }
        form = BorrowerForm(data=form_data)
        self.assertTrue(form.is_valid())
        borrower = form.save()
        self.assertEqual(borrower.first_name, 'John')
        self.assertEqual(borrower.last_name, 'Doe')
        self.assertEqual(borrower.email, 'john.doe@example.com')



class BookFormTest(TestCase):

    def test_form_valid_data(self):
        # Test with valid data
        form_data = {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'published_date': '1925-04-10',
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid with proper data

    def test_form_invalid_data(self):
        # Test with missing title (required field)
        form_data = {
            'title': '',
            'author': 'F. Scott Fitzgerald',
            'published_date': '1925-04-10',
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid because title is required
        self.assertIn('title', form.errors)  # Ensure error for title

        # Test with invalid published_date format (should be a valid date)
        form_data = {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'published_date': 'invalid-date',
        }
        form = BookForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid due to bad date format
        self.assertIn('published_date', form.errors)  # Ensure error for published_date

    def test_form_save(self):
        # Test form save functionality (check if form can create a new Book)
        form_data = {
            'title': 'The Great Gatsby',
            'author': 'F. Scott Fitzgerald',
            'published_date': '1925-04-10',
        }
        form = BookForm(data=form_data)
        self.assertTrue(form.is_valid())
        book = form.save()
        self.assertEqual(book.title, 'The Great Gatsby')
        self.assertEqual(book.author, 'F. Scott Fitzgerald')
        self.assertEqual(book.published_date, date(1925, 4, 10))  # Ensure the date is saved correctly


class TransactionFormTest(TestCase):

    def setUp(self):
        # Set up necessary data for testing
        self.book = Book.objects.create(
            title='The Great Gatsby', 
            author='F. Scott Fitzgerald', 
            published_date='1925-04-10', 
            is_available=True
        )
        self.borrower = Borrower.objects.create(
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com'
        )

    def test_form_valid_data(self):
        # Test with valid data
        form_data = {
            'book': self.book.id,
            'borrower': self.borrower.id,
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid with proper data

    def test_form_invalid_data(self):
        # Test with missing book (required field)
        form_data = {
            'book': '',
            'borrower': self.borrower.id,
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid because book is required
        self.assertIn('book', form.errors)  # Ensure error for book

        # Test with missing borrower (required field)
        form_data = {
            'book': self.book.id,
            'borrower': '',
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid because borrower is required
        self.assertIn('borrower', form.errors)  # Ensure error for borrower

    def test_form_with_unavailable_book(self):
        # Test with an unavailable book
        unavailable_book = Book.objects.create(
            title='Moby Dick', 
            author='Herman Melville', 
            published_date='1851-10-18', 
            is_available=False
        )

        form_data = {
            'book': unavailable_book.id,  # Unavailable book
            'borrower': self.borrower.id,
        }
        form = TransactionForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid because the book is unavailable
        self.assertIn('book', form.errors)  # Ensure error for unavailable book

    def test_form_save(self):
        # Test form save functionality (check if form can create a new Transaction)
        form_data = {
            'book': self.book.id,
            'borrower': self.borrower.id,
        }
        form = TransactionForm(data=form_data)
        self.assertTrue(form.is_valid())
        transaction = form.save()
        self.assertEqual(transaction.book, self.book)
        self.assertEqual(transaction.borrower, self.borrower)




        

class DashboardViewTest(TestCase):
    def setUp(self):
        # Create test data for books, borrowers, and transactions
        self.book1 = Book.objects.create(title='Test Book 1', author='Author 1', is_available=True)
        self.book2 = Book.objects.create(title='Test Book 2', author='Author 2', is_available=True)

        self.borrower = Borrower.objects.create(first_name='John', last_name='Doe', email='johndoe@example.com')

        # Create a transaction with a specific borrowed date (January 9)
        self.transaction = Transaction.objects.create(
            book=self.book1,
            borrower=self.borrower,
            borrowed_date=datetime(2025, 1, 9),  # January 9th
            is_returned=False
        )

        # Update book1's availability to reflect its borrowed status
        self.book1.is_available = False
        self.book1.save()

    def test_dashboard_view(self):
        # Access the dashboard view
        response = self.client.get(reverse('dashboard'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

        # Test if the 'daily_transactions_data' context contains the correct date
        self.assertIn('January 09', response.context['daily_transactions_data'])  # Should show transaction on January 9

        # Test if the count for January 9th is correct
        self.assertEqual(response.context['daily_transactions_data']['January 09'], 1)

        # Test if the total books, total borrowers, and total transactions are correct
        self.assertEqual(response.context['total_books'], 2)
        self.assertEqual(response.context['total_borrowers'], 1)
        self.assertEqual(response.context['total_transactions'], 1)

        # Test if book availability is correctly calculated
        self.assertEqual(response.context['availability_data']['available'], 1)  # 1 available book (book2)
        self.assertEqual(response.context['availability_data']['borrowed'], 1)   # 1 borrowed book (book1)


class BookListViewTest(TestCase):
    def setUp(self):
        # Create test data
        self.book1 = Book.objects.create(title='Django for Beginners', author='William S. Vincent')
        self.book2 = Book.objects.create(title='Python Crash Course', author='Eric Matthes')
        self.book3 = Book.objects.create(title='Automate the Boring Stuff with Python', author='Al Sweigart')

    def test_book_list_no_search_query(self):
        # Test when no search query is provided
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['books'],
            [self.book1, self.book2, self.book3],
            transform=lambda x: x,
            ordered=False
        )

    def test_book_list_search_by_title(self):
        # Test search by title
        response = self.client.get(reverse('book_list') + '?search=Django')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['books'],
            [self.book1],
            transform=lambda x: x
        )

    def test_book_list_search_by_author(self):
        # Test search by author
        response = self.client.get(reverse('book_list') + '?search=Eric')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['books'],
            [self.book2],
            transform=lambda x: x
        )

    def test_book_list_search_case_insensitive(self):
        # Test case-insensitive search
        response = self.client.get(reverse('book_list') + '?search=django')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['books'],
            [self.book1],
            transform=lambda x: x
        )

    def test_book_list_search_no_results(self):
        # Test search with no matching results
        response = self.client.get(reverse('book_list') + '?search=Nonexistent')
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(
            response.context['books'],
            []
        )


class AddBookTest(TestCase):
    def test_add_book_get_request(self):
        """Test that the add book page renders correctly for a GET request."""
        response = self.client.get(reverse('add_book'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIsInstance(response.context['form'], BookForm)

    def test_add_book_post_valid_data(self):
        """Test that a book can be added successfully with valid data."""
        data = {
            'title': 'New Book',
            'author': 'Jane Doe',
            'published_date': '2022-12-01',
            'is_available': True,
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 302)  # Should redirect after adding the book
        self.assertRedirects(response, reverse('book_list'))

        # Verify the book was added to the database
        self.assertEqual(Book.objects.count(), 1)
        book = Book.objects.first()
        self.assertEqual(book.title, 'New Book')
        self.assertEqual(book.author, 'Jane Doe')
        self.assertEqual(str(book.published_date), '2022-12-01')
        self.assertTrue(book.is_available)

    def test_add_book_post_invalid_data(self):
        """Test that invalid data does not create a book."""
        data = {
            'title': '',  # Invalid: Title is required
            'author': 'Jane Doe',
            'published_date': 'invalid-date',  # Invalid date format
            'is_available': True,
        }
        response = self.client.post(reverse('add_book'), data)
        self.assertEqual(response.status_code, 200)  # Page should reload with errors
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIsInstance(response.context['form'], BookForm)

        # Verify no book was added
        self.assertEqual(Book.objects.count(), 0)


class EditBookViewTest(TestCase):
    def setUp(self):
        # Create a book instance
        self.book = Book.objects.create(
            title="Original Title",
            author="Original Author",
            published_date="2022-01-01",
            is_available=True
        )
        self.edit_url = reverse('edit_book', kwargs={'id': self.book.id})

    def test_edit_book_get(self):
        """Test GET request to edit_book view renders the form with book data."""
        response = self.client.get(self.edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIsInstance(response.context['form'], BookForm)
        self.assertEqual(response.context['form'].instance, self.book)

    def test_edit_book_post_no_transactions(self):
        """Test POST request updates book details when there are no transactions."""
        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'published_date': '2023-01-01',
            'is_available': True  # This field should be updated automatically
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after editing
        self.assertRedirects(response, reverse('book_list'))

        # Verify the book was updated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(str(self.book.published_date), '2023-01-01')
        self.assertTrue(self.book.is_available)  # Should remain True

    def test_edit_book_post_with_borrowed_transaction(self):
        """Test book availability updates correctly with active transactions."""
        # Create a Borrower instance
        borrower = Borrower.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com"
        )

        # Create a transaction for this book
        Transaction.objects.create(
            book=self.book,
            borrower=borrower,
            borrowed_date="2024-01-01",
            is_returned=False
        )

        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'published_date': '2023-01-01',
            'is_available': True  # User input ignored for availability
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after editing
        self.assertRedirects(response, reverse('book_list'))

        # Verify the book was updated and availability recalculated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(str(self.book.published_date), '2023-01-01')
        self.assertFalse(self.book.is_available)  # Should be False because the book is borrowed

    def test_edit_book_post_with_returned_transaction(self):
        """Test book availability updates correctly when transactions are returned."""
        # Create a Borrower instance
        borrower = Borrower.objects.create(
            first_name="Jane",
            last_name="Doe",
            email="jane.doe@example.com"
        )

        # Create a returned transaction for this book
        Transaction.objects.create(
            book=self.book,
            borrower=borrower,
            borrowed_date="2024-01-01",
            returned_date="2024-01-02",
            is_returned=True
        )

        data = {
            'title': 'Updated Title',
            'author': 'Updated Author',
            'published_date': '2023-01-01',
            'is_available': True  # User input ignored for availability
        }
        response = self.client.post(self.edit_url, data)
        self.assertEqual(response.status_code, 302)  # Should redirect after editing
        self.assertRedirects(response, reverse('book_list'))

        # Verify the book was updated and availability recalculated
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Title')
        self.assertEqual(self.book.author, 'Updated Author')
        self.assertEqual(str(self.book.published_date), '2023-01-01')
        self.assertTrue(self.book.is_available)  # Should be True since the transaction is returned



class DeleteBookViewTest(TestCase):
    def setUp(self):
        # Create a book instance
        self.book = Book.objects.create(
            title="Book to Delete",
            author="Author to Delete",
            published_date="2022-01-01",
            is_available=True
        )
        self.delete_url = reverse('delete_book', kwargs={'id': self.book.id})

    def test_delete_book(self):
        """Test DELETE request deletes a book."""
        # Ensure the book exists before deletion
        self.assertEqual(Book.objects.count(), 1)

        # Perform the delete request
        response = self.client.post(self.delete_url)

        # Check the redirect to book list
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('book_list'))

        # Ensure the book is deleted
        self.assertEqual(Book.objects.count(), 0)

    def test_delete_non_existent_book(self):
        """Test that trying to delete a non-existent book returns a 404 error."""
        non_existent_id = self.book.id + 1
        delete_url_non_existent = reverse('delete_book', kwargs={'id': non_existent_id})

        # Perform the delete request for a non-existent book
        response = self.client.post(delete_url_non_existent)

        # Ensure the response is 404, as the book doesn't exist
        self.assertEqual(response.status_code, 404)


class BorrowerListViewTest(TestCase):
    def setUp(self):
        # Create Borrower instances
        self.borrower1 = Borrower.objects.create(first_name="John", last_name="Doe", email="john.doe@example.com")
        self.borrower2 = Borrower.objects.create(first_name="Jane", last_name="Smith", email="jane.smith@example.com")

        # Create a Transaction for borrower1
        self.book1 = Book.objects.create(title="Test Book 1", author="Test Author", published_date="2022-01-01", is_available=True)
        self.transaction1 = Transaction.objects.create(borrower=self.borrower1, book=self.book1, borrowed_date="2022-01-01", is_returned=False)

        self.borrower_list_url = reverse('borrower_list')

    def test_borrower_list(self):
        """Test if borrowers are listed correctly."""
        response = self.client.get(self.borrower_list_url)
        self.assertEqual(response.status_code, 200)

        # Test that both borrowers are in the response
        self.assertContains(response, self.borrower1.first_name)
        self.assertContains(response, self.borrower2.first_name)

    def test_borrower_list_search_by_first_name(self):
        """Test if searching by first name works."""
        response = self.client.get(self.borrower_list_url, {'search': 'John'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.borrower1.first_name)
        self.assertNotContains(response, self.borrower2.first_name)

    def test_borrower_list_search_by_last_name(self):
        """Test if searching by last name works."""
        response = self.client.get(self.borrower_list_url, {'search': 'Smith'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.borrower2.last_name)
        self.assertNotContains(response, self.borrower1.last_name)

    def test_borrower_list_search_by_email(self):
        """Test if searching by email works."""
        response = self.client.get(self.borrower_list_url, {'search': 'john.doe@example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.borrower1.email)
        self.assertNotContains(response, self.borrower2.email)

    def test_borrower_list_search_by_borrow_count(self):
        """Test if searching by borrow count works."""
        # borrower1 has one transaction
        response = self.client.get(self.borrower_list_url, {'search': '1'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.borrower1.first_name)
        self.assertNotContains(response, self.borrower2.first_name)

    def test_borrower_list_no_search_query(self):
        """Test if the borrower list is shown when no search query is provided."""
        response = self.client.get(self.borrower_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.borrower1.first_name)
        self.assertContains(response, self.borrower2.first_name)

    def test_borrower_list_search_no_results(self):
        """Test if no results are returned when no borrowers match the search query."""
        response = self.client.get(self.borrower_list_url, {'search': 'Nonexistent'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No borrowers available")





