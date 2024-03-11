
from django.shortcuts import render, get_object_or_404
from .models import Tag, Post

import random


def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = tag.post_set.all()
    return render(request, 'tag_detail.html', {'tag': tag, 'posts': posts})




def random_posts(request):
    # Retrieve a random set of tags
    tags = Tag.objects.all().order_by('?')[:3]  # Get 3 random tags

    # Retrieve posts associated with these random tags
    posts = Post.objects.filter(tags__in=tags).distinct()

    # Shuffle the order of posts
    shuffled_posts = list(posts)
    random.shuffle(shuffled_posts)

    context = {
        'posts': shuffled_posts
    }
    return render(request, 'home_quotes.html', context)