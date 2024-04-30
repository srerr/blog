from django.shortcuts import render,redirect,get_object_or_404
from app1.models import Post,Comments,Subscribe,Tag,Profile,WebsiteMeta
from app1.forms import CommentForm,SubscribeForm,NewUserForm,PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm

def index(request):
    subscribe_form=SubscribeForm()
    posts=Post.objects.all()
    top_posts=Post.objects.all().order_by('-view_count')[0:3]
    recent_posts=Post.objects.all().order_by('-time')[0:3]
    featured_blog=Post.objects.filter(is_featured=True)
    subscribe_successful=None
    website_info=None
    if WebsiteMeta.objects.all().exists():
        website_info=WebsiteMeta.objects.all()[0]
    if featured_blog:
        featured_blog=featured_blog[0]
    if request.POST:
        subscribe_form=SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            subscribe_successful='subscribed successfully'
            subscribe_form=SubscribeForm()   
    context={'posts':posts,'top_posts':top_posts,'recent_posts':recent_posts,'subscribe_form':subscribe_form,'subscribe_successful':subscribe_successful,'featured_blog':featured_blog,'website_info':website_info}
    return render(request,'app1/index.html',context)
def post_page(request,slug):
    post=Post.objects.get(slug=slug)
    comments=Comments.objects.filter(post=post,parent=None)
    form=CommentForm()
    #bookmark logic
    bookmarked=False
    if post.bookmarks.filter(id=request.user.id).exists():
        bookmarked=True
    is_bookmarked=bookmarked
    #like logic
    liked=False
    if post.likes.filter(id=request.user.id).exists():
        liked=True
    number_of_likes=post.number_of_likes()
    post_is_liked=liked
    if request.POST:
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid:
            parent_obj=None
            if request.POST.get('parent'):
                parent=request.POST.get('parent')
                parent_obj=Comments.objects.get(id=parent)
                if parent_obj:
                    comment_reply=comment_form.save(commit=False)
                    comment_reply.parent=parent_obj
                    comment_reply.post=post
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))
            else:
                comment=comment_form.save(commit=False)
                postid=request.POST.get('post_id')
                post=Post.objects.get(id=postid)
                comment.post=post
                comment.save()
                return HttpResponseRedirect(reverse('post_page',kwargs={'slug':slug}))
    if post.view_count is None:
        post.view_count=1
    else:
        post.view_count=post.view_count+1
    post.save()
    #sidebar
    recent_posts=Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]
    top_authors=User.objects.annotate(number=Count('post')).order_by('-number')
    tags=Tag.objects.all()
    related_posts=Post.objects.exclude(id=post.id).filter(author=post.author)[0:3]
    context={'post':post,'form':form,'comments':comments,'is_bookmarked':is_bookmarked,'post_is_liked':post_is_liked,'number_of_likes':number_of_likes,'recent_posts':recent_posts,'top_authors':top_authors,'tags':tags,'related_posts':related_posts}
    return render(request,'app1/post.html',context)
def tag_page(request,slug):
    tag=Tag.objects.get(slug=slug)
    tags=Tag.objects.all()
    top_posts=Post.objects.filter(tags__in=[tag.id]).order_by('-view_count')[0:3]
    recent_posts=Post.objects.filter(tags__in=[tag.id]).order_by('-time')[0:3]
    context={'tag':tag,'top_posts':top_posts,'recent_posts':recent_posts,'tags':tags}
    return render(request,'app1/tag.html',context)
def author_page(request,slug):
    profile=Profile.objects.get(slug=slug)
    top_posts=Post.objects.filter(author=profile.user).order_by('-view_count')[0:3]
    recent_posts=Post.objects.filter(author=profile.user).order_by('-time')[0:3]
    top_authors=User.objects.annotate(number=Count('post')).order_by('number')[0:3]
    context={'profile':profile,'top_posts':top_posts,'recent_posts':recent_posts,'top_authors':top_authors}
    return render(request,'app1/author.html',context)
def search_posts(request):
    search_query=''
    if request.GET.get('q'):
        search_query=request.GET.get('q')
    posts=Post.objects.filter(title__icontains=search_query)
    print('search:',search_query)
    context={'posts':posts,'search_query':search_query}
    return render(request,'app1/search.html',context)
def about(request):
    website_info=None
    if WebsiteMeta.objects.all().exists():
        website_info=WebsiteMeta.objects.all()[0]
    context={'website_info':website_info}
    return render(request,'app1/about.html',context)
def register_user(request):
    form=NewUserForm()
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            login(request,user)
            return redirect("/") 
    context={'form':form}
    return render(request,'registration/registration.html',context)
"""def logins(request):
    form=NewUserForm()
    if request.method=="POST":
        form=NewUserForm(request.POST)
        if form.is_valid():  
            user=form.save()
            login(request,user)
            return redirect("/")"""
         
#def logouts(request):
 #   return redirect("registration/logged_out.html")
#def logins(request):
 #   return redirect("registration/login.html")
def bookmark_post(request,slug):
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.bookmarks.filter(id=request.user.id).exists():
        post.bookmarks.remove(request.user)
    else:
        post.bookmarks.add(request.user)
    return HttpResponseRedirect(reverse('post_page',args=[str(slug)]))
def like_post(request,slug): 
    post=get_object_or_404(Post,id=request.POST.get('post_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return HttpResponseRedirect(reverse('post_page',args=[str(slug)]))
def all_bookmarked_post(request):
    all_bookmarked_posts=Post.objects.filter(bookmarks=request.user)
    context={'all_bookmarked_posts':all_bookmarked_posts}
    return render(request,'app1/all_bookmarked_posts.html',context)
def all_post(request):
    all_posts=Post.objects.all()
    context={'all_posts':all_posts}
    return render(request,'app1/all_posts.html',context)
def all_liked_posts(request):
    all_liked_posts=Post.objects.filter(likes=request.user)
    context={'all_liked_posts':all_liked_posts}
    return render(request,'app1/all_liked_posts.html',context) 
def newpost(request):
    post=Post()
    newpost=PostForm()
    #if request.method == "POST":
     #   form=PostForm(request.POST, request.FILES)
      #  if form.is_valid():
       #     form.save()
        #    print("hi")
         #   return redirect('/') 
    if request.method=="POST":
        title= request.POST.get('title')
        content= request.POST.get('content')
        image = request.FILES.get('image')
        Post.objects.create(title=title, content=content, slug=title, image=image)
        return redirect('/')
    context={'newpost':newpost,'post':post}
    return render(request,'app1/newpost.html',context)
def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})
def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")