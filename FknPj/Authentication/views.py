
import os
from django.shortcuts import render, redirect
from . models import *
from FknAp.models import Post
from django.contrib import messages ,auth
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json



def home(request):
    posts = Post.objects.all().order_by('-date_created')
    if request.user.is_authenticated:
        try:
            customuser = CustomUser.objects.get(username=request.user.username)
            context = {'customuser': customuser, 'posts': posts}
            return render(request, 'index.html', context)
        except ObjectDoesNotExist:
            pass  
                                                                                                                                                                                                                                
    return render(request, 'index.html', {'posts': posts})




def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('Authentication:home')
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
                user = auth.authenticate(username=username, password=password)

                if user is not None:
                    auth.login(request,user)
                    return redirect('Authentication:home')

        else:
            messages.info(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')

    return render(request, 'signup.html')



def terms_and_conditions(request):
    return render(request, 'terms.html')



def signout(request):
    auth.logout(request)
    return redirect('Authentication:home')



def profile(request):
    customuser = CustomUser.objects.get(username=request.user.username)
    context = {'customuser': customuser}
    return render(request, "profile.html", context)



def gallery_view(request):
    images = GalleryImage.objects.all()
    return render(request, 'gallery.html', {'images': images})



@login_required
def set_profile_pic(request, image_id):
    customuser = CustomUser.objects.get(username=request.user.username)
    image = GalleryImage.objects.get(pk=image_id)
    customuser.profile_pic = image.image
    customuser.save()
    return redirect('Authentication:home')


def about_us(request):
    return render(request,'about-us.html')

