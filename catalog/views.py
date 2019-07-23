import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Book, Author, BookInstance, Genre, Language


# Create your views here.
def index(request):
    """View function for home page of site"""

    #Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    #Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact= 'a').count()
    #The 'all()' implied by default
    num_authors = Author.objects.count()
    #Number of languages in the banks
    num_languages = Language.objects.count()

    #Number of visit as counted in session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books' : num_books,
        'num_instances' : num_instances,
        'num_instances_available' : num_instances_available,
        'num_authors' : num_authors,
        'num_languages' : num_languages,
        'num_visits' : num_visits,
    }
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book    #apparently this is enough but in order to make a class view. Django will tell which database should use
    #context_object_name = 'book_list'      #my own name for the list as a template variable
    #queryset = Book.objects.filter(title__icontains="God")[:5]  #first 5 books which contain "GOD"
    #template_name = 'catalog/book_list.html'      #specify my own template name and space
    paginate_by = 10

class BookDetailView(generic.DetailView):
    model = Book

class AuthorListView(generic.ListView):
    model = Author
    #context_object_name = 'author_list'
    #template_name = 'catalog/author_list.html'

class AuthorDetailView(generic.DetailView):
    model = Author
    #context_object_name = 'author-detail'
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user"""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class AllBorrowedBooksListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'catalog/all_borrowed.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian.
    :type request: object
    """
    book_instance = get_object_or_404(BookInstance, pk=pk)

    #If the request is a POST then process the Form data
    if request.method == 'POST':

        #Create a form instance and populate it with data from the request--binding:
        form = RenewBookForm(request.POST)

        if form.is_valid():
            #process the data in form.cleaned_data as required
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            return HttpResponseRedirect(reverse('all-borrowed'))

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date' : proposed_renewal_date})

    context = {
        'form' : form,
        'book_instance' : book_instance,
    }

    return render(request, 'catalog/book_new_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = '__all__'
    initial = {'date_of_death' : '01/01/2018'}


class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


#-----------Book CreateView---------------


class BookCreate(CreateView):
    model = Book
    fields = '__all__'

class BookUpdate(UpdateView):
    model = Book
    fields = '__all__'

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')

#------------Book Instance-----------------

class BookInstanceCreate(CreateView):
    model = BookInstance
    fields = '__all__'
    success_url = reverse_lazy('books')

class BookInstanceUpdate(UpdateView):
    model = BookInstance
    fields = '__all__'

class BookInstanceDelete(DeleteView):
    model = BookInstance
    success_url = reverse_lazy('books')



# ----------------------------------------------



class BookInstanceListView (generic.ListView):
    model = BookInstance
    paginate_by = 30
    template_name = 'catalog/bookinst_list.html'


class BookInstanceDetailView (generic.DetailView):
    model = BookInstance
    paginate_by = 10
    template_name = 'catalog/bookinst_detail.html'


#-------------------------------------------------
#def createUser(request):


