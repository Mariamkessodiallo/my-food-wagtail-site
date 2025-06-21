# views.py
from django.shortcuts import render, get_object_or_404
from .models import Categories, BlogPage

def category_view(request, slug):
    category = get_object_or_404(Categories, slug=slug)
    posts = BlogPage.objects.live().filter(categories=category).order_by('-date')
    return render(request, 'blog/category_page.html', {
        'category': category,
        'posts': posts,
    })
