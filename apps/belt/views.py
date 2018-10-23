from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import re
import bcrypt
EMAIL_REGEX= re.compile (r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
from apps.belt.models import *

def index(request):

    return render(request,'belt/index.html')

def register(request):

    error=False

    for key, value in request.POST.items():
        if len(value)==0:
            messages.error(request, key + ' cannot be empty')
            error=True
    
    if len(request.POST['first_name'])>2 and not request.POST['first_name'].isalpha():
        messages.error(request,'First name must be letters')
        error=True

    if len(request.POST['last_name'])>2 and not request.POST['last_name'].isalpha():
        messages.error(request,'Last name must be letters')
        error=True
    
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Bad email')
        error=True
    
    elif len(User.objects.filter(email=request.POST['email']))>0:
        messages.error(request,'Email already exists')
        error=True
    
    if len(request.POST['password'])<8:
        messages.error(request,'Password must be longer')
        error=True
    
    if request.POST['confirm_password']!=request.POST['password']:
        messages.error(request,'Passwords must match')
        error=True

    if error:
        return redirect('/')

    # ENTER INTO DB
    new_user=User.objects.create(first_name=request.POST['first_name'], 
    last_name=request.POST['last_name'], 
    email=request.POST['email'], 
    password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))

    request.session['u_id']=new_user.id

    return redirect('/quotes')
    # REDIRECT HOME PAGE

def login(request):

    user = User.objects.filter(email=request.POST['email'])

    if len(user)==0:
        messages.error(request,'Try again')
        return redirect('/')
    
    if not bcrypt.checkpw(request.POST['password'].encode(),user[0].password.encode()):
        messages.error(request,'Try again')
        return redirect('/')

    request.session['u_id']=user[0].id

    return redirect('/quotes')

def logout(request):

    request.session.pop('u_id')
    return redirect('/')

def quotes(request):

    if 'u_id' not in request.session:
        messages.error(request,'Must log in')
        return redirect('/')
    
    user=User.objects.get(id=request.session['u_id'])
    quotes=Quote.objects.all().order_by('-created_at')


    context={
        "user" : user,
        "quotes" : quotes
    }

    return render(request,'belt/quotes.html', context)

def add(request):

    user=User.objects.get(id=request.session['u_id']) 
    
    if len(request.POST['author'])>2 and len(request.POST['content'])>10:
        Quote.objects.create(author=request.POST['author'],content=request.POST['content'],creator=user)
        return redirect('/quotes')
    
    messages.error(request,'Author must be more than two characters and quote must be longer than ten characters.')
    return redirect('/quotes')

def delete(request, id):

    Quote.objects.get(id=id).delete()

    return redirect('/quotes')

def user(request, id):

    user=User.objects.get(id=id)
    quotes=Quote.objects.filter(creator=user)

    context={
        "user" : user,
        "quotes" : quotes
    }

    return render(request,'belt/user.html', context)

def myaccount(request, id):

    user=User.objects.get(id=id)

    context={
        "user" : user
    }

    return render(request,'belt/myaccount.html', context)

def edit(request, id):

    user=User.objects.get(id=id)
    error=False

    for key, value in request.POST.items():
        if len(value)==0:
            messages.error(request, key + ' cannot be empty')
            error=True
    
    if not EMAIL_REGEX.match(request.POST['email']):
        messages.error(request,'Bad email')
        error=True
    
    elif len(User.objects.filter(email=request.POST['email']))>0:
        messages.error(request,'Email already exists')
        error=True

    
    if error:
        return redirect('/myaccount/{}'.format(id))
    
    u=User.objects.get(id=id)
    u.first_name=request.POST['first_name']
    u.last_name=request.POST['last_name']
    u.email=request.POST['email']
    u.save()
    
    return redirect('/myaccount/{}'.format(id))

def like(request, id):

    myquote = Quote.objects.get(id=id)
    myuser = User.objects.get(id=request.session['u_id'])
    myuser.likequotes.add(myquote)

    return redirect('/quotes')

def dislike(request, id):

    myquote = Quote.objects.get(id=id)
    myuser = User.objects.get(id=request.session['u_id'])
    myuser.likequotes.remove(myquote)

    return redirect('/quotes')

