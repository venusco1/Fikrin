
from django.shortcuts import render, get_object_or_404
from .models import Tag




def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'tag_list.html', {'tags': tags})

def tag_detail(request, tag_id):
    tag = get_object_or_404(Tag, pk=tag_id)
    posts = tag.post_set.all()
    return render(request, 'tag_detail.html', {'tag': tag, 'posts': posts})
