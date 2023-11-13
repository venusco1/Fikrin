from django.shortcuts import render, redirect
from . models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
# Create your views here.


def home(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username,password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect('FknAp:home')
        else:
            error_message = 'Incorrect username or password.'
            return render(request, 'login.html',{'error_message':error_message})
        
    return render(request, 'login.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirm-password')
        mobile_number = request.POST.get('mobile-number')

        if   username and password and mobile_number:
            if CustomUser.objects.filter(username=username).exists():
                return render(request, 'signup.html',{'message_username':'This username is not available.'})
                
            elif CustomUser.objects.filter(mobile_number=mobile_number).exists():
                return render(request, 'signup.html',{'message_mbnumber':'This mobile number is already taken.'})

            elif password != confirmation:
                return render(request, 'signup.html',{'message_password':'Passwords must match.'})
            
            else:
                user = CustomUser.objects.create_user(username=username, password=password, mobile_number=mobile_number)
                user.mobile_number = mobile_number
                user.save()
                user = auth.authenticate(username=username,password=password)
                
                if user is not None:
                    auth.login(request,user)
                    return redirect('FknAp:home')

        else:
            messages.info(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def terms_and_conditions(request):
    return render(request, 'terms.html')

def signout(request):
    auth.logout(request)
    return redirect('FknAp:home')



def profile(request):
    customuser = CustomUser.objects.get(username=request.user.username)
    context = {'customuser': customuser}
    return render(request, "profile.html", context)


@login_required
def create_post(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text')

        
        post = Post.objects.create(creater=request.user, content_text=content_text)
            
        post.save()
        return redirect('FknAp:home')


    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})



def home(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'index.html', {'posts': posts})