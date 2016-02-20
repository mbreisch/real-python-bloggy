from django.http import HttpResponse
from django.template import Context, loader, RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.core.urlresolvers import reverse
from models import Post
from forms import PostForm


# helper functions
def encode_url(url):
    return url.replace(' ', '_')


def get_popular_posts():
    return Post.objects.all().order_by('-views')[:5]


# Create your views here.
def index(request):
    latest_posts = Post.objects.all().order_by('-created_at')
    popular_posts = get_popular_posts()
    t = loader.get_template('blog/index.html')
    context_dict = {
        'latest_posts': latest_posts,
        'popular_posts': popular_posts,

    }
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def post(request, slug):
    single_post = get_object_or_404(Post, slug=slug)
    single_post.views += 1  # increment the number of views
    single_post.save()  # and save it
    t = loader.get_template('blog/post.html')
    context_dict = {
        'single_post': single_post,
        'popular_posts': get_popular_posts(),
    }
    c = Context(context_dict)
    return HttpResponse(t.render(c))


def add_post(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            data=form.save(commit=True) # Save method returns the object being saved
            return redirect(reverse('post',args=[data.slug]))
        else:
            print form.errors
    else:
        form = PostForm()
    return render_to_response('blog/add_post.html', {'form': form}, context)
