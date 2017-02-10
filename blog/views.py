#!python
#log/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.admin import User
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from forms import post_form,category_form,comment_form,reply_form
from .models import Category,Post,Comment ,ForbiddenWords
from django.utils import timezone
from django.core.mail import send_mail
# from forms import post_form,category_form,comment_form
from .models import Category,Post,Comment
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic import UpdateView,CreateView, DeleteView
from blog.forms import UserForm
from models import Post,Category,Comment,Reply
from forms import category_form, comment_form, post_form,reply_form ,ForbiddenWordsForm
# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
@login_required(login_url="login/")
def home(request):
    context = show_category_for_all(request)

    if request.user.is_authenticated():
        username = request.user.username
        is_admin = request.user.is_superuser
        print(is_admin)
        print(username)
        context['username']= username
        if (is_admin):
            return render(request, "admin-panel.html", context)
        else:
            return render(request, "home.html", context)
    else:
        return render(request, "404.html")

def homelogin(request):
    if request.user.is_authenticated():
        username = request.user.username
        print(username)
        return render(request, "home.html", {'username':username,})
    else:
        return render(request, "404.html")

def index(request):
    username = None
    user_id = request.user.id
    allCategory=Category.objects.all()
    allPost=Post.objects.all()

    if  not request.user.is_authenticated():
        context = {'allCategory':allCategory,'allPost':allPost}

        return render(request, "index.html",context)
    else:
        username = request.user.username
        context={'username': username,'allCategory':allCategory,'allPost':allPost, 'user_id': user_id,}
        return render(request, "index.html",context)

def index2(request):
    username = None
    allPost = Post.objects.all().order_by('pub_date').reverse()[0:5]
    if request.user.is_authenticated():
        username = request.user.username
    allCategory = Category.objects.all()
    index(request)
    # context = {'allCategory':allCategory}
    categories_for_user = Category.objects.filter(
        id__in=Category.users.through.objects.filter(user_id=request.user.id).values_list('category_id'))
    subscribed = {}
    for category in categories_for_user:
        subscribed[category.id] = True
    context = {
        "categories": allCategory,
        "subscribed": subscribed,
        "user": request.user,
        'username': username,
        'allPost': allPost
    }
    print(context)

    return render(request, "index.html", context)



def all_users(request):
    allusers = User.objects.all()
    return render(request, "allusers.html", {'allusers': allusers, })

def handler404(request):
    response = render_to_response('404.html',
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

class UserUpdateView2(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'updateuser.html'
    success_url = reverse_lazy('home')

class UserCreateView(CreateView):
    form_class = UserForm
    model = User
    template_name = 'createuser.html'
    success_url = reverse_lazy('home')


class UserDeleteView(DeleteView):
    form_class = UserForm
    model = User
    template_name = 'deleteuser.html'
    success_url = reverse_lazy('home')



def getUserObject(request,uid):
    user = User.objects.get(id = uid)
    return HttpResponse(user)

def show_category(request):
    username = None
    allPost = Post.objects.all().order_by('pub_date').reverse()[0:5]
    if request.user.is_authenticated():
        username = request.user.username
    allCategory = Category.objects.all()
    index(request)
    # context = {'allCategory':allCategory}
    categories_for_user = Category.objects.filter(
        id__in=Category.users.through.objects.filter(user_id=request.user.id).values_list('category_id'))
    subscribed = {}
    for category in categories_for_user:
        subscribed[category.id] = True
    context = {
        "categories": allCategory,
        "subscribed": subscribed,
        "user": request.user,
        'username': username,
        'allPost': allPost
    }
    print(context)

    return render(request, "category.html", context)


def subscribe_category(request, c_id):
    category = Category.objects.get(pk=c_id)
    # user = User.objects.get(pk = request.user.id)
    # user = request.user
    user = request.user
    username = request.user.username
    user_email = request.user.email
    category_name = category.categoryName
    send_mail('successfully subscribed','Thank you '+ username +'\nYou have successfully subscribed to ' + category_name + ' category' , 'noreply@Gnedyblog.com', [user_email])
    category.users.add(user)

    # return HttpResponseRedirect("/category_details/" + c_id)    #/category/all/  or /home/
    return HttpResponseRedirect("/")


def unsubscribe_category(request, c_id):
    category = Category.objects.get(pk=c_id)
    # user = User.objects.get(pk = request.user.id)
    # user = request.user
    user = request.user
    username = request.user.username
    user_email = request.user.email
    category_name = category.categoryName
    send_mail('successfully unsubscribed','Thank you '+ username +'\nYou have successfully unsubscribed from ' + category_name + ' category' , 'noreply@Gnedyblog.com', [user_email])

    category.users.remove(user)
    return HttpResponseRedirect("/")


def show_post(request):
    post = Post.objects.all().order_by('pub_date').reverse()
    context = {'post': post}
    return render(request, "post.html", context)

def new_post(request):
    form = post_form()
    user_id = request.user.id
    print(user_id)
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES)
        post = form.save(commit=False)
        print(form)
        post.user_id = int(user_id)
        print(form)
        if form.is_valid():
            post.save()
            return HttpResponseRedirect(
                '/post/all')

    context = {'p_form': form}
    return render(request, 'blog/post_form.html', context)


# add category
def new_category(request):
    form = category_form()
    if request.method == 'POST':
        form = category_form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/all')

    context = {'ct_form': form}
    return render(request, 'blog/category_form.html', context)


def category_details(request, id):
    allCategory=Category.objects.all()
    category = Category.objects.get(id=id)
    post = Post.objects.filter(category=id)
    context = show_category_for_all(request)
    context['post']= post
    return render(request, 'category_details.html', context)


def edit_category(request, id):
    category = Category.objects.get(id=id)
    form = category_form(instance=category)
    if request.method == 'POST':
        form = post_form(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/category/all')

    context = {'ct_form': form}
    return render(request, 'blog/category_form.html', context)


# delete
def delete_category(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return HttpResponseRedirect('/category/all')


def post_details(request, id):
    is_admin = request.user.is_superuser
    post = Post.objects.filter(id=id)
    comment = Comment.objects.filter(post_id=id)
    com = new_comment(request, id)
    replies = Reply.objects.filter(post_id=id)
    x=show_category_for_all(request)
    print(replies)

    # replies = blog_reply.objects.filter(post_id=id)
    # replay=new_Replay(request,id,comment.id)
    y = {'post': post, 'comment': comment, 'id': id, 'comment_form': com["comment_form"],'replies':replies,'is_admin':is_admin }
    context = x.copy()
    context.update(y)
    print(context)
    return render(request, 'post_details.html', context)


# edit
def edit_post(request, id):
    post = Post.objects.get(id=id)
    form = post_form(instance=post)
    if request.method == 'POST':
        form = post_form(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/post/all')

    context = {'p_form': form}
    return render(request, 'blog/post_form.html', context)


# delete
def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect('/post/all')
    # add comment


def new_comment(request, id):
    post = Post.objects.get(id=id)
    post_id = post.id;
    user_id = request.user.id
    if request.method == "POST":
        form = comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            com_con = comment.comment_text
            com_con2 = check_profanity(com_con)
            comment.comment_text = com_con2
            comment.post_id = post_id
            comment.user_id = int(user_id)
            comment.save()


            # comment.save()
            rep = Reply.objects.create(comment_id=comment.id,post_id=post_id,)
            print(rep)
            # rep.comment_id = com.id
            # rep.post_id = id
            rep.save()
            print(rep)

            comment_id = comment.id
            # reply=new_Replay(request,id,comment_id)
            # return render(request, 'post_details.html','replay_form':reply["replay_form"])

            # return {'comment_form': form, 'comment_id': comment_id}
            # return post_details(request,id)
    else:
        form = comment_form()
    return {'comment_form': form, }


# def new_Reply(request, post_id, comment_id):
#     post = Post.objects.get(id=post_id)
#     post_id = post.id;
#     comment = Comment.objects.get(id=comment_id)
#     comment_id = comment.id
#     user_id = request.user.id
#     if request.method == "POST":
#         form = reply_form(request.POST)
#         if form.is_valid():
#             reply = form.save(commit=False)
#             reply.post_id = post_id
#             reply.user_id = int(user_id)
#             reply.comment_id = id
#             reply.save()
#             return post_details(request, post_id)
#     else:
#         form = reply_form()
#     return {'reply_form': form}

class ReplyUpdateView(UpdateView):
    form_class = reply_form
    model = Reply
    template_name = 'updatereply.html'
    success_url = reverse_lazy('index')



#forbidden words
def all_forbidden_words(request):
    all_forbidden_words = ForbiddenWords.objects.all()
    context = {'all_forbidden_words' : all_forbidden_words}
    return render(request, 'list_forbidden_words.html', context)




def delete_forbidden_word(request, w_id):
    word = ForbiddenWords.objects.get(id= w_id)
    word.delete()
    return HttpResponseRedirect('/forbidden_words/')



def new_forbidden_word(request):
    form = ForbiddenWordsForm()
    if request.method == 'POST':
        form = ForbiddenWordsForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/forbidden_words/')
    context = {'forbidden_words_form' : form }
    return render(request, 'blog/forbidden_words_form.html', context)


#TO DO : take comment text to be replaced with the original comment on post
def check_forbidden_words_in_comment(request, comment_txt):
    coment_txt_arr = comment_txt.split(",")
    all_forbidden_words = ForbiddenWords.objects.all()
    for word in all_forbidden_words:
        replaced=""
        if comment_txt.find(word.forbiddenWord):
            for c in word.forbiddenWord:
                replaced+="*"
            comment_txt= comment_txt.replace(word.forbiddenWord,replaced)

    return HttpResponseRedirect('/forbidden_words/')

#end forbidden words


def check_profanity(content):
    filtered = ''
    first_word = True
    for word in content.split():
        if not first_word:
            filtered += ' '
        first_word = False
        if ForbiddenWords.objects.filter(forbiddenWord = word.lower()):
            filtered += ('*' * len(word))
        else:
            filtered += word
    return filtered



def show_category_for_all(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    # index(request)

    allCategory = Category.objects.all()
    # context = {'allCategory':allCategory}
    categories_for_user = Category.objects.filter(
        id__in=Category.users.through.objects.filter(user_id=request.user.id).values_list('category_id'))
    subscribed = {}
    for category in categories_for_user:
        subscribed[category.id] = True
    context = {
        "categories": allCategory,
        "subscribed": subscribed,
        "user": request.user,
        'username': username,
    }

    return context