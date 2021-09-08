from django.contrib import messages
from django.shortcuts import redirect, render
import bcrypt
from .decorators import login_required
from .models import Author,Book,Review
from .auth import User
from django.db import IntegrityError

@login_required
def index(request):
    #print(request.session['user']['id'])
    usuario=User.objects.get(id=request.session['user']['id'])
    n_reviews=Review.objects.all().filter(owner=usuario).count()
    reviews=Review.objects.all().order_by('-created_at')[:2]
    other_reviews=Review.objects.all().order_by('-created_at')[2:10]
    
    context = {     
        "reviews":reviews,
        "n_reviews":n_reviews,
        "other_reviews":other_reviews
    }
    return render(request, 'index.html', context)

@login_required
def books(request,book_id):
    book=Book.objects.get(id=book_id)
    reviews=Review.objects.filter(book=book).order_by('-created_at')
    context = {        
        "book":book,    
        "reviews":reviews
    }
    return render(request, 'books.html', context)

@login_required
def users(request,user_id=0):
    if user_id==0:
        usuario=User.objects.get(id=  request.session['user']['id'])
    else:
        usuario=User.objects.get(id=  user_id)
    n_reviews=Review.objects.all().filter(owner=usuario).count()
    reviews=Review.objects.all().filter(owner=usuario)
    context = {   
        "n_reviews":n_reviews,
        "usuario":usuario,
        "reviews":reviews 
    }
    return render(request, 'users.html', context)

@login_required
def books_add(request):
    if request.method == "GET":
        autores=Author.objects.all()
        context = {   
            "autores":autores
        
        }
        return render(request, 'books_add.html', context)
    if request.method == "POST":
        usuario=User.objects.get(id=  request.session['user']['id'])
        titulo=request.POST['title']
        stars=request.POST['stars']
        if request.POST['author']=='other':
            nombre=request.POST['first_name']
            apellido=request.POST['last_name']
            try:
                autor=Author.objects.create(first_name=nombre,last_name=apellido)
            except IntegrityError:
                messages.warning(request,f'Autor(a) existente!')
                autor=Author.objects.filter(first_name=nombre, last_name=apellido)
        else: 
            author_id=request.POST['author']
            autor=Author.objects.get(id=author_id)
        #validacion de que el libro no exista
        try:
            libro=Book.objects.create(title=titulo)
        except  IntegrityError:
            messages.warning(request,f'El libro ya existe ')
            libros=Book.objects.filter(title=titulo).all()[:1]
            libro=libros[0]
        
        libro.authors.add(autor)
        libro.save()
        comentario=request.POST['review_text']
        review=Review.objects.create(texto=comentario,stars=stars,owner=usuario,book=libro)
        return redirect('/')

@login_required
def review_destroy(request,review_id):
    rev=Review.objects.get(id=review_id)
    rev.delete()
    messages.success(request,f'Comentario Eliminado ')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def review_add(request,book_id):
    libro=Book.objects.get(id=book_id)
    usuario=User.objects.get(id=request.session['user']['id'])
    stars=request.POST['stars']
    comentario=request.POST['review_text']
    review=Review.objects.create(texto=comentario,stars=stars,owner=usuario,book=libro)
    messages.success(request,f'Comentario Creado ')
    return redirect('/books/'+str(book_id))
    