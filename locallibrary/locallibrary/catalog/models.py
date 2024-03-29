from django.db import models
from django.urls import reverse # Used to generate URLs by reversing the URL patterns
import uuid

class Genre(models.Model):
    """It's a model representing a book genre"""
    name = models.CharField(max_length=200, unique='True', help_text='Enter a book genre (e.g. Science Fiction, French Poetry etc.)')
    
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular Author: Firstname Lastname."""
        return reverse('genre-detail', args=[str(self.id)])
    
class Author(models.Model):
    """
    Model representing an author
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def get_absolute_url(self):
        """Returns the URL to acess a particular author instance"""
        return reverse('author-detail', args=[str(self.id)])
    
    def __str__(self):
        return f" {self.first_name} {self.last_name}"
    
class Book(models.Model):
    """
    Model representing a book (but not a specific copy of a book).
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.RESTRICT, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', 
                            max_length=15, 
                            unique=True, 
                            help_text='13 characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre, help_text="Select genre for this book")
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])
    
    

    
class BookInstance(models.Model):
    """
    Model representing  a specyfic copy of a book
    (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    
    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),

    )
    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text = "Book availability"
    )
    class Meta:
        ordering = ['due_back']
        
    
    def __str__(self):
        return f" {self.id} ({self.book.title})"
    

    
class Language(models.Model):
    name = models.CharField(max_length=200, 
                            unique=True,
                            help_text='Enter a language like i.e. English, Deuchese, French') 
    
    def __str__(self):
        return self.name