from django.shortcuts import render, HttpResponse, redirect
import bcrypt
from .models import *
from django.contrib import messages
from django.db.models import Q

def index(request):
    return render(request, "python_app/index.html")

def create_user(request):
    if request.method == 'GET':
        return redirect('/')
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value)
            return redirect('/')
    else:
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()) 
        new_user = User.objects.create(name=request.POST['name'], alias=request.POST['alias'], email=request.POST['email'], password=hash)
        request.session['user_id'] =  new_user.id 
        messages.success(request, "Successully registered!")
        return redirect('/')

def login(request):
    if 'user_id' in request.session:
        return redirect('/success')
    if request.method == "GET":
        return redirect('/')
    try:
        User.objects.filter(email=request.POST['log_email'])
    except:
        messages.error(request, "User does not exist.")
        return redirect('/')
    email_m = User.objects.filter(email=request.POST['log_email'])
    if not email_m:
        messages.error(request, "Invalid Email")
        return redirect('/')
    email_match = email_m[0]
    if bcrypt.checkpw(request.POST['log_password'].encode(), email_match.password.encode()):
        request.session['user_id'] = email_match.id
        messages.success(request, "Welcome!!")
        return redirect('/success')
    else: 
        messages.error(request, "Wrong Password.")
        return redirect('/')

def success(request):
    if not "user_id" in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['user_id'])
        context = {
            'user': user, 
            'non_favourites': Quote.objects.all().exclude(join=request.session['user_id']),
            'favourites': Quote.objects.filter(join=request.session['user_id'])
        }
        return render(request, 'python_app/success.html', context)

def submit(request):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('/')
    errors = Quote.objects.quote_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request,value) 
            return redirect('/success')
    else:
        user = User.objects.get(id = request.session['user_id'])
        user.quotes.create(quoted_by=request.POST['quoted_by'], message=request.POST['message'])
        
        return redirect('/success')        

def show_quote(request, id):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('/')
    else: 
        user = User.objects.get(quotes__id=id)
        all_quotes = Quote.objects.filter(users=user)
        context = {
            'user' : user,
            'user_quotes': all_quotes,
            'count': all_quotes.count()
        }
        return render(request, 'python_app/show_quote.html', context)

def add_fave(request, quote_id):
    print(quote_id)
    quote = Quote.objects.get(id=quote_id)
    user = User.objects.get(id=request.session['user_id'])
    user.join.add(quote)
    user.save()
    return redirect('/success')

def remove_fave(request, quote_id):
    quote = Quote.objects.get(id=quote_id)
    quote.join.remove(User.objects.get(id=request.session['user_id']))
    return redirect('/success')

def logout(request):
    if "user_id" not in request.session:
        messages.error(request, "You are not logged in.")
        return redirect('/')
    del request.session['user_id']
    return redirect('/')

