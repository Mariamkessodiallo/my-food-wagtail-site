from django import forms
from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from wagtail.search import index
from modelcluster.fields import ParentalManyToManyField
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from wagtail.images.models import Image


@register_snippet
class Categories(models.Model):
    """
    Snippet for categorizing blog posts.
    """
    name = models.CharField(
        max_length=100,
        verbose_name="Category Name",
        help_text="E.g. Agriculture, Élevage"
    )
    slug = models.SlugField(
        unique=True,
        max_length=80,
        help_text="URL-friendly identifier"
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Post Category"
        verbose_name_plural = "Post Categories"
        ordering = ['name']


@register_snippet
class SeasonalPromotion(models.Model):
    """
    A simple snippet that holds one promotion: a headline, an image, and 
    an optional URL to link to.
    """
    title = models.CharField(
        max_length=255,
        help_text="A short title or heading for this promotion"
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='+',
        help_text="Upload the promotional image"
    )
    link_url = models.URLField(
        blank=True,
        help_text="(Optional) where this promotion should point"
    )
    link_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="(Optional) text for the link button (e.g. “Learn More”)"
    )

    panels = [
        FieldPanel('title'),
        FieldPanel('image'),   # Wagtail will render an image‐chooser automatically
        FieldPanel('link_url'),
        FieldPanel('link_text'),
    ]

    class Meta:
        verbose_name = "Seasonal Promotion"
        verbose_name_plural = "Seasonal Promotions"

    def __str__(self):
        return self.title


class BlogHomePage(Page):
    max_count = 1
    template = "blog/blog_home_page.html"

    def get_context(self, request, *args, **kwargs):
        ctx = super().get_context(request, *args, **kwargs)

        # 1) Grab every live BlogPage, newest first
        all_posts = BlogPage.objects.live().order_by("-date")

        # 2) If there's a ?category=slug, filter by that
        category_slug = request.GET.get("category")
        if category_slug:
            category = get_object_or_404(Categories, slug=category_slug)
            all_posts = all_posts.filter(categories=category)
            ctx["current_category"] = category

        # 3) Sidebar “Popular Post”: take the 3 most recent items
        ctx["sidebar_popular_posts"] = all_posts[:3]

        # 4) Sidebar “Category” list: all Categories
        ctx["sidebar_categories"] = Categories.objects.all()

        # 5) Paginate *all_posts* (no more “featured=False”) into pages of 4
        page_number = request.GET.get("page", 1)
        paginator = Paginator(all_posts, 10)# 4 posts per page
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # 6) “posts” is what your template loops over
        ctx["posts"] = page_obj

        return ctx


class BlogPage(Page):
    """
    Individual blog post pages with date, intro, body, categories, featured flag, and image.
    """
    template = "blog/blog_page.html"


    date = models.DateField(
        "Post date",
        help_text="Publication date of the article"
    )
    intro = models.CharField(
        max_length=250,
        help_text="Brief introduction displayed in post listings"
    )
    body = RichTextField(
        features=['h2', 'h3', 'bold', 'italic', 'link', 'ol', 'ul', 'image'],
        help_text="Main content of the post"
    )

    categories = ParentalManyToManyField(
        'blog.Categories',
        blank=True,
        verbose_name="Categories",
        help_text="Select categories for this post"
    )

    featured = models.BooleanField(
        default=False,
        verbose_name="Featured Post",
        help_text="Display this post in featured sections"
    )

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        help_text="Main image for the post (1200x600px recommended)"
    )

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
        index.FilterField('categories'),
        index.FilterField('featured'),
    ]

    sent_as_newsletter = models.BooleanField(
        default=False,
        help_text="Has this post already been sent as a newsletter?"
    )

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('image'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('featured'),
        
    ]

    promote_panels = Page.promote_panels + [
        FieldPanel('slug'),
        FieldPanel('seo_title'),
        FieldPanel('search_description'),
    ]

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        ordering = ['-date']


    