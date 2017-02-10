
#!python
# django-blog/urls.py
from django.conf.urls import include, url
from django.contrib import admin
# Add this import
from django.contrib.auth import views
from blog.forms import LoginForm
from blog.views import show_category,index2


from blog.views import index, handler404
#from registration.forms import RegistrationFormUniqueEmail
#from registration.backends.default.views import RegistrationView
from django.conf.urls import handler404

APP_NAME='django-blog'
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index2, name='index' ),
    url(r'', include('blog.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),
    url(r'^login/$', views.login , {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    # url(r'^accounts/register/$', 'registration.views.register',
    #     {'form_class': RegistrationFormUniqueEmail,
    #      'backend': 'registration.backends.default.DefaultBackend'},
    #     name='registration_register'),
    # url(r'^register/$',
    #     RegistrationView.as_view(form_class=RegistrationFormUniqueEmail),
    #     name='registration_register'),

]

handler404 = 'blog.views.handler404'
