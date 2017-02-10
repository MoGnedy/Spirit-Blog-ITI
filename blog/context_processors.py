from blog.views import Category,index
def show_category(request):
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
