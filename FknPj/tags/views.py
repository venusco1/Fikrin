import random

from django.shortcuts import get_object_or_404, render

from .models import Post, Tag


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, "tag_list.html", {"tags": tags})


def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = tag.post_set.all()
    return render(request, "tag_detail.html", {"tag": tag, "posts": posts})


def random_posts(request):
    posts = list(Post.objects.all())  # Convert QuerySet to a list
    random.shuffle(posts)  # Shuffle the list of posts

    context = {"posts": posts}
    return render(request, "home_quotes.html", context)
