from django.contrib import admin
from catalog.models import Author, Genre, Language, Book, BookInstance, UserProfileInfo, User




#define admin class
class Books(admin.TabularInline):
    model = Book

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [Books]

# @admin.register does the same thing as admin.site.register

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'display_genre', 'language')
    inlines = [BooksInstanceInline]



@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'borrower', 'due_back', 'id')
    list_filter = ('status', 'due_back')
    fieldsets = (
        (None, {
            'fields' : ('book', 'imprint', 'id')
        }),
        ('Availability',{
            'fields' : ('status', 'due_back', 'borrower')
        })
    )


# Register your models here.
#admin.site.register(Book)
admin.site.register(Genre)
admin.site.register(Language)
admin.site.register(Author, AuthorAdmin)
admin.site.register(UserProfileInfo)
#admin.site.register(BookInstance)

