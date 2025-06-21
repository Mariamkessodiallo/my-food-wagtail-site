# core/management/commands/send_newsletter.py
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from blog.models import BlogPage
from core.models import Subscriber

class Command(BaseCommand):
    help = 'Send a blog post to all newsletter subscribers'

    def add_arguments(self, parser):
        parser.add_argument('slug', type=str, help='Slug of the blog post to send')

    def handle(self, *args, **kwargs):
        slug = kwargs['slug']
        try:
            post = BlogPage.objects.get(slug=slug, live=True)
        except BlogPage.DoesNotExist:
            raise CommandError(f"No live blog post found with slug '{slug}'")

        subject = post.title
        message = f"{post.intro}\n\nRead more: https://food.com{post.url}"
        from_email = "mariamkessod99@gmail.com"
        recipient_list = list(Subscriber.objects.values_list('email', flat=True))

        if not recipient_list:
            self.stdout.write(self.style.WARNING("No subscribers to send to."))
            return

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        self.stdout.write(self.style.SUCCESS(f"Newsletter sent to {len(recipient_list)} subscribers."))
