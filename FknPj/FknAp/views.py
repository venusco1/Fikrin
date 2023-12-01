import os
from django.shortcuts import get_object_or_404, render, redirect
from . models import *
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib import messages ,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .forms import ImageForm

# Create your views here. CustomUser    profile_pic


def home(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'index.html', {'posts': posts})



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



def profile_cropping(request, user_id):
    form = ImageForm(request.POST or None, request.FILES or None)
    customuser = CustomUser.objects.get(username=request.user.username)

    if form.is_valid() and 'profile_pic' in request.FILES:
        # Remove the old profile image if it exists
        if customuser.profile_pic:
            if os.path.isfile(customuser.profile_pic.path):
                os.remove(customuser.profile_pic.path)

        # Save the new profile picture
        form.save_profile_pic(user_id)
        return redirect('FknAp:profile')

    context = {'form': form, 'customuser': customuser}
    return render(request, 'upt_image.html', context)



@login_required
def create_post(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text')

        post = Post.objects.create(creater=request.user, content_text=content_text)
        return redirect('FknAp:home')

    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})



@csrf_exempt
def edit_post(request, post_id):
    if request.method == 'POST':
        text = request.POST.get('edit_text')
        post = get_object_or_404(Post, pk=post_id)
        post.content_text = text         
        new_text = post.content_text
        post.edit_post(new_text=new_text)

        return redirect('FknAp:home')
    
    else:
        return HttpResponse("Method must be 'POST'")
    


def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    
    # Check if the user has permission to delete the post, for example:
    if request.user == post.creater:
        post.delete()

        # Get the scroll position from the query parameter if available
        scroll_position = request.GET.get('scroll_position', '0')
        print(scroll_position)
        # Redirect back to the same page with the scroll position as a query parameter
        return redirect('FknAp:home')

    else:
        # Handle cases where the user doesn't have permission to delete the post
        # Redirect or render an error message as appropriate
        return redirect('FknAp:home')




