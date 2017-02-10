
from django.conf.urls import url
from . import views, forms
from django.conf.urls import (
handler400, handler403, handler404, handler500
)

APP_NAME = 'blog'

# We are adding a URL called /home
urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^show_category_for_all$', views.show_category_for_all, name='show_category_for_all'),
    url(r'^home/login/$', views.homelogin, name='homelogin'),
    url(r'post/new', views.new_post),
    url(r'category/new', views.new_category),
    url(r'category/all', views.show_category),
    url(r'category/(?P<id>[0-9]+)/category_details$', views.category_details),
    url(r'post/(?P<id>[0-9]+)/post_details$', views.post_details),
    url(r'post/all', views.show_post),
    url(r'^post/(?P<id>[0-9]+)/edit', views.edit_post),
    url(r'post/(?P<id>[0-9]+)/delete', views.delete_post),
    # url(r'^post/(?P<id>[0-9]+)/comment$', views.new_comment),
    url(r'^category/(?P<id>[0-9]+)/edit$', views.edit_category),
    url(r'category/(?P<id>[0-9]+)/delete', views.delete_category),
    url(r'^allusers$', views.all_users),
    url(r'^updateuser$', forms.UserUpdateView.as_view(), name='updateuser'),
    url(r'^userobj/(?P<uid>[0-9]+)',views.getUserObject,name='getuserobj'),
    url(r'^updateuser/(?P<pk>[0-9]+)/$', views.UserUpdateView2.as_view(), name='updateuser2'),
    url(r'^createuser/$', views.UserCreateView.as_view(), name='createuser'),
    url(r'^deleteuser/(?P<pk>[0-9]+)/$', views.UserDeleteView.as_view(), name='deleteuser'),
    url(r'^reply/(?P<pk>[0-9]+)$', views.ReplyUpdateView.as_view(), name='updatereply'),
    url(r'^forbidden_words/$', views.all_forbidden_words),
    url(r'^new_forbidden_word/$', views.new_forbidden_word),
    url(r'^(?P<w_id>[0-9]+)/delete_forbidden_word/$', views.delete_forbidden_word),
    url(r'^(?P<comment_txt>[0-9a-zA-Z ]+)/check_comment/$', views.check_forbidden_words_in_comment),
    # url(r'(?P<id>[0-9]+)/category_details$', views.category_details),
    url(r'^category/(?P<c_id>[0-9]+)/subscribe/$', views.subscribe_category),  # redirection to subscribe category
    url(r'^category/(?P<c_id>[0-9]+)/unsubscribe/$', views.unsubscribe_category),  # redirection to unsubscribe category

]

handler404 = 'views.handler404'