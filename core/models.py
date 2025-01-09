from django.db import models

class Borrower(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField(default='2000-01-01')
    is_available = models.BooleanField(default=True)  

    def __str__(self):
        return self.title

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.book.title} borrowed by {self.borrower.first_name} {self.borrower.last_name}'
