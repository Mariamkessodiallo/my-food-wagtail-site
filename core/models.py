from django.db import models
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel



@register_snippet
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True, editable=False)

    panels = [
        FieldPanel("email"),
       
    ]

    def __str__(self):
        return self.email
