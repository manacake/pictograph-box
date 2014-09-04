from django.contrib.syndication.views import Feed
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.shortcuts import get_object_or_404, render_to_response
from django.views.generic import ListView
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from blogengine.models import Category, Post, Tag
import markdown2

class CategoryListView(ListView):
    template_name = 'blogengine/category_post_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            category = Category.objects.get(slug=slug)
            return Post.objects.filter(category=category)
        except Category.DoesNotExist:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        try:
            context['category'] = Category.objects.get(slug=slug)
        except Category.DoesNotExist:
            context['category'] = None
        return context

class TagListView(ListView):
    template_name = 'blogengine/tag_post_list.html'

    def get_queryset(self):
        slug = self.kwargs['slug']
        try:
            tag = Tag.objects.get(slug=slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()

    def get_context_data(self, **kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        slug = self.kwargs['slug']
        try:
            context['tag'] = Tag.objects.get(slug=slug)
        except Tag.DoesNotExist:
            context['tag'] = None
        return context

class PostsFeed(Feed):
    title = "RSS feed - posts"
    link = "/"
    description = "RSS feed - blog posts"

    def items(self):
        return Post.objects.order_by('-pub_date')

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        extras = ['fenced-code-blocks']
        # Render description as markdown
        content = mark_safe(markdown2.markdown(force_unicode(item.text),
                                               extras = extras))
        return content

class CategoryPostsFeed(PostsFeed):
    def get_object(self, request, slug):
        return get_object_or_404(Category, slug=slug)

    def title(self, obj):
        return "RSS feed - blog posts in category %s" % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "RSS feed - blog posts in category %s" % obj.name

    def items(self, obj):
        return Post.objects.filter(category=obj).order_by('-pub_date')

class TagPostsFeed(PostsFeed):
    def get_object(self, request, slug):
        return get_object_or_404(Tag, slug=slug)

    def title(self, obj):
        return "RSS feed - blog posts tagged  %s" % obj.name

    def link(self, obj):
        return obj.get_absolute_url()

    def description(self, obj):
        return "RSS feed - blog posts tagged %s" % obj.name

    def items(self, obj):
        # Remember tags use a many-to-many relationship
        try: 
            tag = Tag.objects.get(slug=obj.slug)
            return tag.post_set.all()
        except Tag.DoesNotExist:
            return Post.objects.none()

def getSearchResults(request):
    '''Search for a post by title or text'''
    # Get the query data
    query = request.GET.get('q', '')
    page = request.GET.get('page', 1) # defaults to 1 anyway

    # Query the database
    if query:
        results = Post.objects.filter(Q(text__icontains=query) | Q(title__icontains=query))
    else:
        results = None

    # Add pagination: use paginator to manually paginate results
    pages = Paginator(results, 5)

    # Get specified page
    try:
        returned_page = pages.page(page)
    except EmptyPage: # show last page instead
        returned_page = pages.page(pages.num_pages)

    # Display the search results
    return render_to_response('blogengine/search_post_list.html',
                              {'page_obj': returned_page,
                               'object_list': returned_page.object_list,
                               'search': query})