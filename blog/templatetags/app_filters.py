from django import template

register = template.Library()


@register.filter
def equal(post, user_id):
    return int(post.userID_id) == int(user_id)


@register.filter
def lookup(dict, key):
    return dict[key]

