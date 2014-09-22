# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http import Http404
from models import Post, Tag, Category
from datetime import datetime
from django.db.models.aggregates import Sum

def home(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        RequestContext(request,
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })
    )

def contact(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )
def posts(request):
    assert isinstance(request, HttpRequest)

    #Get Current Page Index
    p = request.GET.get('p', '1')
    try:
        pageIndex = int(p)
    except ValueError:
        pageIndex = 1
    
    posts = Post.objects.order_by("-is_top", "-publish_time")[5 * (pageIndex - 1) : 5 + 5 * (pageIndex - 1)]
    pageCount = Post.objects.all().count() /5 + 1
    pageList = range(1, pageCount + 1)
    if pageIndex > pageCount or pageIndex <= 0:
        raise Http404
    
    # Get Tags
    tags = Tag.objects.all()

    # Get Categories
    catCount = Post.objects.values("category").annotate(Sum('category'))
    catName = Category.objects.only("title")
    cats = {}
    for index in range(len(catName)):
        cats[catName[index].title] = catCount[index]['category__sum']

    return render(
        request,
        'app/posts.html',
        RequestContext(request,
        {
            'posts' : posts,
            'PageCount' : pageCount,
            'pages' : pageList,
            'pageIndex' : pageIndex,
            'tags' : tags,
            'cats' : cats
        })
    )

def post(request, postName):
    assert isinstance(request, HttpRequest)
    #if (postName[-5:] != ".html"):
    #    raise Http404
    #else:
    #    postName = postName[0:-5]

    try:
        post = Post.objects.get(link = postName)
    except Post.DoesNotExist:
        raise Http404

    return render(
        request,
        'app/post.html',
        RequestContext(request,
        {
            'post':post
        })
    )