from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.contrib import messages
from models import User,Quote
# Create your views here.
def index(request):
    return render(request, 'quoteapp/index.html')

def login(request):
    result = User.objects.validateLogin(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request, result[1])

def register(request):
    print request.POST['fullname']
    result = User.objects.validateReg(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect('/')
    return log_user_in(request, result[1])

def print_messages(request, message_list):
    for message in message_list:
        messages.add_message(request, messages.INFO, message)

def log_user_in(request, user):
    request.session['user'] = {
        'id' : user.id,
        'name' : user.name,
        'alias' : user.alias,
        'email' : user.email,
    }
    return redirect('/quotes')

def logout(request):
    request.session.pop('user')
    return redirect('/')


def quotes(request):
    liked_quote = User.objects.get(id=request.session['user']['id']).liked_quote.all()
    quotables = Quote.objects.exclude(id__in=liked_quote.values_list("id", flat=True))
    favorites = User.objects.get(id=request.session['user']['id']).liked_quote.all()
    context = {'quotables':quotables, 'favorites':favorites}
    return render(request, 'quoteapp/quotes.html',context)
def addquote(request):
    result = Quote.objects.addquote(request)
    if result[0] == False:
        print_messages(request, result[1])
        return redirect('/quotes')
    return redirect('/quotes')
def addFavorite(request,quote_id, user_id):
    quote = Quote.objects.addFavorite(quote_id,user_id)
    return redirect('/quotes')
def removeFavorite(request, quote_id, user_id):
    quote = Quote.objects.removeFavorite(quote_id,user_id)
    return redirect('/quotes')
def users(request,user_id):
    quotes= Quote.objects.filter(created_by=user_id)
    user= User.objects.get(id=user_id)
    context = {'quotes':quotes,'user':user}
    return render(request,'quoteapp/user.html',context)
