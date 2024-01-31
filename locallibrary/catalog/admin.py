from django.contrib import admin
from .models import Book, BookInstance, Author, Genre, Language, Authorship


# admin.site.register(Book)

class BookInline(admin.TabularInline):
    model = Book 
    



@admin.register(BookInstance)  # można też w ten sposób
class BookInstanceAdmin(admin.ModelAdmin):
    list_filter = ('status', 'due_back')
    
    # fieldsets = (
    #     (None, {
    #     'fields': ('book', 'imprint', 'id')
    #     }),
    
    # ('Availabity' ,{
    #     'fields' : ('status', 'due_back')
    #     }),
    # )
    fields = ['book', 'status', ('due_back', 'id')]

   
    
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):  # można też tak
    list_display = ('first_name', 'last_name', 'date_of_birth', 'date_of_death')
    
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    
# admin.site.register(Author, AuthorAdmin) 

# jak tutaj
@admin.register(Authorship)
class AuthorshipAdmin(admin.ModelAdmin):
    pass

class AuthorshipInline(admin.TabularInline):
    model = Authorship


class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class AuthorInstanceInline(admin.TabularInline):
    model = Author
    

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    
    def display_genre(self, obj):
        return ', '.join([genre.name for genre in obj.genre.all()])
    
    inlines = [BooksInstanceInline, AuthorshipInline]
    
    
admin.site.register(Book, BookAdmin)

    
    
admin.site.register(Genre)
admin.site.register(Language)

# admin.site.register(Book, BookAdmin)

# admin.site.register(BookInstance)
# admin.site.register(Author)
