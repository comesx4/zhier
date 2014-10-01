# Create your views here.
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from django.http import Http404
from models import Post, Tag, Category
from datetime import datetime
from django.db.models.aggregates import Count

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
    cate = request.GET.get('cate', '')

    # Get the Current Page Index
    try:
        pageIndex = int(p)
    except ValueError:
        pageIndex = 1

    # Get the Current CateIndex
    try:
        cateIndex = int(cate)
    except ValueError:
        cateIndex = ''

    if '' == cateIndex:
        postsAll = Post.objects.order_by("-is_top", "-publish_time")
    else:
        postsAll = Post.objects.filter(category = cateIndex).order_by("-is_top", "-publish_time")

    posts = postsAll[5 * (pageIndex - 1) : 5 + 5 * (pageIndex - 1)]

    pageCount = postsAll.count() /5 + 1
    
    pageList = range(1, pageCount + 1)
    if pageIndex > pageCount or pageIndex <= 0:
        raise Http404
    
    # Get Tags
    tags = Tag.objects.all()

    # Get Categories
    catCount = Post.objects.values("category").annotate(Count('category'))
    catName = Category.objects.only("title")
    cats = {}
    for cat in catName:
        cats[cat.title] = [ 0 if catCount.filter(category=cat.id) == 0 else catCount.filter(category=cat.id)[0]['category__count'], cat.id]

    return render(
        request,
        'app/posts.html',
        RequestContext(request,
        {
            'title' : 'All Posts',
            'posts' : posts,
            'PageCount' : pageCount,
            'pages' : pageList,
            'pageIndex' : pageIndex,
            'tags' : tags,
            'cats' : cats,
            'crtCate' : cateIndex
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