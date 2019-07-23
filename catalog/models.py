from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from django.contrib.auth.forms import UserCreationForm

import uuid




# Create your models here
class Genre (models.Model):
    #model representing genre of books
    name = models.CharField(max_length=200, help_text='enter book genre')

    def __str__(self):
        #string for representing model object
        return self.name


class Language(models.Model):
    BookLanguage = models.CharField(max_length=200, help_text='Enter book\'s language')

    def __str__(self):
        return self.BookLanguage


class Book (models.Model):
    #model representing the title of the book
    title = models.CharField(max_length=200, help_text='book title')

    #Foreign key is used because books can only have one author but author can make multiple books
    #Author is a string rather than an object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description about the book')
    isbn = models.CharField(max_length=13, help_text='13 characters <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    #ManyToMany used because genre can contain many books and books can hold many genres
    #Genre class has been defined so we can specify the object above

    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')

    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    def display_genre(self):
        return ', '.join(genre.name for genre in self.genre.all()[0:3])

    display_genre.short_description = 'Genre'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        #Returns the url to access a detail record for this book
        return reverse('book-detail', args = [str(self.id)])



class BookInstance(models.Model):
    '''Model representing a specific copy of a book'''
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m' , 'Maintenance'),
        ('o' , 'On Loan'),
        ('a' , 'Available'),
        ('r' , 'Reserved'),
    )

    status = models.CharField(
        max_length = 1,
        choices = LOAN_STATUS,
        blank = True,
        default = 'm',
        help_text= 'Book availability',
    )

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def get_absolute_url(self):
        #Returns the url to access a detail record for this book
        return reverse('bookinst-detail', args = [str(self.id)])

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        else:
            return False

    class Meta:
        ordering = ['due_back']
        permissions = (("can_mark_returned", "Set book as returned"),)

    def __str__(self):
        '''String representing model object'''
        return f'{self.id} ({self.book.title})'


class Author(models.Model):

    '''Model representing the Author'''
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        '''returns the url to access particular author instance.'''
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        '''represent models'''
        return '{0},{1}'.format(self.last_name, self.first_name)





