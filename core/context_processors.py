from blog.models import BlogHomePage, Categories

def site_wide(request):
    return {
        'blog_home': BlogHomePage.objects.live().first(),
        'categories': Categories.objects.all(),
    }