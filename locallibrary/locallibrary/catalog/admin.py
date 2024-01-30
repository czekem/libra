from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, Language


admin.site.register(Book)
admin.site.register(BookInstance)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)

# Register your models here.
