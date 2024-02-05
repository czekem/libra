from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, BookInstance, Author, Authorship, Genre, Language
from django.db.models import Count, Min
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views import View

def index(request):
   
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
   
   
   # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authours = Author.objects.count()
    num_genres = Genre.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
   
   
    context = {
      
      'num_books': num_books,
      'num_instances': num_instances,
      'num_instances_available': num_instances_available,
      'num_authors': num_authours,
      'num_genres': num_genres, 
      'num_visits': num_visits,
      }
   
    return render(request, 'index.html', context=context)


def authors(request):

   
    num_authors = Author.objects.count()
    name_of_authors = ', '.join([f'{author[0]} {author[1]}' for author in Author.objects.values_list('first_name', 'last_name')])
    author_and_books = ', '.join([f'{author} - {title}' for author, title in Book.objects.values_list( 'author__last_name', 'title')])
    
    
    context = {
       'num_authors' : num_authors,
       'name_of_authors' : name_of_authors,
       "author_and_books" : author_and_books,
       
    }
   
    return render(request, 'catalog/authors.html', context=context)

class AuthorDetailView(generic.DetailView):
    model = Author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author = self.object
        context['books'] = Book.objects.filter(author=author)
        return context
 
 
class AuthorListView(generic.ListView):
    model = Author
    
    paginate_by = 10


class BookListView(generic.ListView):
    model = Book
    paginate_by = 10


class BookDetailView(generic.DetailView):
    model = Book

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to the current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 4
    
    def get_queryset(self):
        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )


    
    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

class Myview(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class MyView(PermissionRequiredMixin, View):
    permission_required = "catalog.can_mark_returned"
    permission_required = ('catalog.can_mark_returned', 'catalog.change_book')
    
