
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Subscriber

from blog.models import BlogPage, Categories, SeasonalPromotion

def homepage(request):
    # 1) Get all live posts, newest first
    all_posts = BlogPage.objects.live().order_by("-date")
    
    # 2) Keep the first 6 featured posts for your slider
    slider_posts = all_posts.filter(featured=True)[:6]

    # 3) Build a queryset of *all* featured posts (newest first)
    all_featured = all_posts.filter(featured=True)

    # 4) Paginate those featured posts, 4 per page
    paginator = Paginator(all_featured, 4)   # 4 featured posts / page
    page_number = request.GET.get("page", 1) # read ?page=…
    try:
        paginated_featured = paginator.page(page_number)
    except PageNotAnInteger:
        paginated_featured = paginator.page(1)
    except EmptyPage:
        paginated_featured = paginator.page(paginator.num_pages)

    # 5) Sidebar data (unchanged)
    sidebar_categories      = Categories.objects.all()
    sidebar_popular_posts   = all_posts[:3]   # “three latest” for sidebar

    # 6) NEW: fetch all SeasonalPromotion snippets
    promotions = SeasonalPromotion.objects.all().order_by('-id')

    return render(request, "index.html", {
        "slider_posts": slider_posts,                # first six featured for your carousel
        "paginated_featured": paginated_featured,    # <Page> of featured posts, 4 per page
        "sidebar_categories": sidebar_categories,
        "sidebar_popular_posts": sidebar_popular_posts,
        "promotions": promotions,
    })

def about(request):
    return render(request, 'about.html')

def contact(request):

    return render(request, 'contact.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings  # To use DEFAULT_FROM_EMAIL

def contact(request):
    
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        # Basic validation
        if not name or not email or not subject or not message:
            messages.error(request, "Tous les champs doivent être remplis.")
            return redirect('contact')

        # Compose email content
        full_message = f"Message de {name} <{email}>:\n\n{message}"

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,  # 'mariamkessod99@gmail.com'
                recipient_list=['infofoodaccess2@gmail.com'],  # Your contact email
                fail_silently=False,
            )
            messages.success(request, "Merci pour votre message! Nous vous répondrons bientôt.")
        except Exception as e:
            messages.error(request, "Erreur lors de l'envoi du message. Veuillez réessayer plus tard.")
            # Optionally log the exception e

        return redirect('contact')

    # If GET request, just render the contact page (your template)
    return render(request, 'contact.html')



def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, "Thank you for subscribing!")
            else:
                messages.info(request, "You are already subscribed.")
        else:
            messages.error(request, "Please enter a valid email address.")
    return redirect(request.META.get('HTTP_REFERER', '/'))

