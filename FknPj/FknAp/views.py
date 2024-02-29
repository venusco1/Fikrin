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
from django.core.exceptions import ObjectDoesNotExist
import json


import requests
from fcm_django.models import FCMDevice

def send_notification(registration_ids, message_title, message_desc, post_id):

    fcm_api = "AAAAkV-gc5c:APA91bF4PJPVDpihuGhCzMljtG1RjI-ZOn0xLr8UscqsQGw6nPZ7mDz9ttTeXZUj6LHjT1fdwkhUEdXYa22jR-dJ-OEr3_MDwTbVNUsTB8Wofl8H8ApQ8Sbo8dkEnFNTR5OXeOIrtKTS"
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
        "Content-Type": "application/json",
        "Authorization": 'key=' + fcm_api
    }

    payload = {
        "registration_ids": registration_ids,
        "priority": "high",
        "notification": {
            "body": message_desc,
            "title": str(message_title) + ": ",
            "click_action": "/" 

        },
        "data": {
            "post_id": post_id,
        }
    }

    result = requests.post(url, data=json.dumps(payload), headers=headers)
    print(result.json())




@login_required
def create_post(request):
    if request.method == 'POST':
        content_text = request.POST.get('content_text')

        post = Post.objects.create(creater=request.user, content_text=content_text)

        # Get the ID of the newly created post
        post_id = post.id

        try:
            devices = FCMDevice.objects.filter(active=True)
            registration_ids = [device.registration_id for device in devices]

            if registration_ids:
                message_title = request.user
                message_desc = content_text
                send_notification(registration_ids, message_title, message_desc, post_id)
                print('Notification sent to {} devices.'.format(len(registration_ids)))
            else:
                print('No active devices found for sending notifications.')

        except ObjectDoesNotExist:
            print('An error occurred: FCMDevice model not found or misconfigured.')
        except Exception as e:
            print('An error occurred:', str(e))

        return redirect('Authentication:home')

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
        return redirect('Authentication:home')

    else:
        return HttpResponse("Method must be 'POST'")



def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('Authentication:home')



def comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        parent_comment_id = request.POST.get('parent_comment_id')
        parent_comment = None

        if parent_comment_id:
            parent_comment = Comment.objects.get(id=parent_comment_id)

        # Check if the post belongs to the user 
        new_comment = Comment.objects.create(
            post=post,
            commenter=request.user,
            comment_content=comment_text,
            parent_comment=parent_comment,
        )

        # Save notification
        message = f" By {request.user.username}: {comment_text}"
        notification = Notification.objects.create(user=request.user, post=post, message=message)

        return redirect('FknAp:comments', post_id)
    
    else:
        comments = Comment.objects.filter(post=post, parent_comment=None)
        customuser = CustomUser.objects.get(username=request.user.username)
                 
        context = {
            'comments': comments, 'post': post,
            'customuser': customuser,
        }
    
        return render(request, 'comments_copy.html', context)


def add_reply(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    parent_comment = get_object_or_404(Comment, pk=comment_id)
    commenter = request.user

    if request.method == 'POST':
        body = request.POST.get('body')

        new_reply = Comment.objects.create(
            post=parent_comment.post,
            commenter=commenter,
            comment_content=body,
            parent_comment=parent_comment
        )
        

        message = f" By {request.user.username}: {body}"
        notification = Notification.objects.create(user=request.user, post=post, message=message)

        return redirect('FknAp:comments', post_id)

    comments = Comment.objects.filter(post=post, parent_comment=None)
    customuser = CustomUser.objects.get(username=request.user.username)
    context = {
        'comments': comments,
        'post': post,
        'customuser': customuser,
        'parent_comment': parent_comment
    }
    return render(request, 'reply_copy.html', context)



def delete_comment(request, post_id, comment_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        comment = get_object_or_404(Comment, pk=comment_id)
        comment.delete()
        comments = Comment.objects.filter(post=post, parent_comment=None)

        customuser = CustomUser.objects.get(username=request.user.username)
        context = {
            'comments': comments,
            'post': post,
            'customuser': customuser
        }

        return render(request, 'comments_copy.html', context)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)



@csrf_exempt
def like_post(request, id):
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.add(request.user)
                post.save()

                try:
                    devices = FCMDevice.objects.filter(active=True)
                    registration_ids = [device.registration_id for device in devices]

                    if registration_ids:
                        message_title = request.user
                        message_desc = 'You have a new like on your post!'
                        send_notification(registration_ids, message_title, message_desc, id)
                        print('Notification sent to {} devices.'.format(len(registration_ids)))
                    else:
                        print('No active devices found for sending notifications.')

                except ObjectDoesNotExist:
                    print('An error occurred: FCMDevice model not found or misconfigured.')
                except Exception as e:
                    print('An error occurred:', str(e))

                return HttpResponse(status=204)
                
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")


@csrf_exempt
def unlike_post(request, id):
        if request.method == 'PUT':
            post = Post.objects.get(pk=id)
            print(post)
            try:
                post.likers.remove(request.user)
                post.save()
                return HttpResponse(status=204)
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse("Method must be 'PUT'")


def view_notifications(request):
    user_notifications = Notification.objects.filter(post__creater=request.user).order_by('-timestamp')

    context = {
        'notifications': user_notifications,
    }
    return render(request, 'noti.html', context)




def clear_notifications(request):
    user_notifications = Notification.objects.filter(post__creater=request.user).order_by('-timestamp')
    user_notifications.all().delete() 
    return redirect('Authentication:home')



