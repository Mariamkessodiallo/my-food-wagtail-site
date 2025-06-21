from wagtail import hooks
from django.core.management import call_command
from blog.models import BlogPage
import logging

logger = logging.getLogger(__name__)

@hooks.register('after_publish_page')
def send_newsletter_after_publish(request, page):
    print("✅ Hook triggered for:", page)

    if isinstance(page, BlogPage):
        post = BlogPage.objects.get(id=page.id)
        print("➡️ This is a BlogPage:", post.slug)

        if not post.sent_as_newsletter:
            print("🟢 Newsletter not yet sent, sending now...")
            try:
                call_command('send_newsletter', post.slug)
                post.sent_as_newsletter = True
                post.save(update_fields=['sent_as_newsletter'])
                print("✅ Newsletter sent and flag updated.")
            except Exception as e:
                print("❌ Error sending newsletter:", e)
        else:
            print("🔁 Already sent as newsletter.")
    else:
        print("❌ Not a BlogPage instance.")
