from django.shortcuts import render, redirect
from django.views import View
from django.urls import reverse
from django.db.models import Count
from django.views.generic import ListView

from .forms import CommentForm
from .models import Post, Author

# Create your views here.
class IndexView(View):
    def get(self, request):
        latest_posts = Post.objects.order_by('-id')[:3]
        trending_posts = Post.objects.filter(tag__caption='Trending').order_by('-id')[:3]
        top_authors = Author.objects.all().order_by('-rating')
        
        context={'latest_post':latest_posts[0], 'latest_posts': latest_posts[1:3],
            'trending_post':trending_posts[0], 'trending_posts':trending_posts[1:3],
            'top_author': top_authors[0], 'top_authors': top_authors[1:3],}
        return render(request, 'blog/index.html', context)
    
    
class GalleryView(View):
    def get(self, request):
        return render(request, 'blog/gallery.html', {})
    
    
class PostsListView(ListView):
    template_name = 'blog/posts.html'
    model = Post
    ordering = ['id']
    context_object_name = 'posts'
    
    def get_queryset(self):
        return super().get_queryset()


class PostDetailsView(View):
    def get_context_data(self, **kwargs):
        context = {}
        slug = kwargs['slug']
        post = Post.objects.get(slug=slug)
        context['post'] = post
        context['tags'] = post.tag.all()
        post_tags = set(tag.caption for tag in post.tag.all())
        context['related_posts'] = Post.objects.filter(tag__caption__in=post_tags).exclude(id=post.id).annotate(same_tag_count=Count('tag')).order_by('?')[:3]      
        context['comments'] = post.comments.all().order_by('-id')
        context['comment_form'] = CommentForm()
        if post.slug in self.request.session.get('read-later', []): is_saved = True
        else: is_saved = False
        context['is_saved'] = is_saved

        return context
    
    def get(self, request, slug):
        context = self.get_context_data(slug=slug)
        return render(request, 'blog/post_details.html', context)
    
    def post(self, request, slug):
        context = self.get_context_data(slug=slug)
        post = context['post']
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(reverse('post_details', args=[slug]))
        context['comments'] = post.comments.all().order_by('-id')
        context['comment_form'] = comment_form
        return render(request, 'blog/post_details.html', context)


class ReadLaterView(View):
    def get(self, request):
        saved_slugs = request.session.get('read-later', [])
        saved_posts = Post.objects.filter(slug__in=saved_slugs)
        context = {'saved_posts': saved_posts}
        return render(request, 'blog/read_later.html', context)
    
    def post(self, request, slug):
        saved_slugs = request.session.get('read-later', [])
        if slug not in saved_slugs:
            saved_slugs.append(slug)
        elif slug in saved_slugs:
            saved_slugs.remove(slug)
        request.session['read-later'] = saved_slugs
        return redirect(reverse('post_details', args=[slug]))
    

class AuthorInfoView(View):
    def get(self, request, first_name, last_name):
        author = Author.objects.get(first_name=first_name, last_name=last_name)
        author_posts = Post.objects.filter(author=author)
        context = {'author':author,  'author_posts':author_posts}
        return render(request, 'blog/author_info.html', context)


