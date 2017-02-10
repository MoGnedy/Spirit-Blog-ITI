from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from models import Post,Category,Comment,Reply
from django.contrib.auth.admin import User , UserChangeForm
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.generic import UpdateView
from django.http import HttpResponseRedirect
from django.utils import timezone
from .models import ForbiddenWords



class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class UserForm(forms.ModelForm):
    # password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email','password', 'is_superuser', 'is_active')






class UserUpdateView(UpdateView):
    form_class = UserForm
    model = User
    template_name = 'updateuser.html'

    def get(self, request, **kwargs):
        self.object = User.objects.get(username=self.request.user)
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


    def get_object(self, queryset=None):
        return self.request.user



class post_form(forms.ModelForm):
	class Meta:
		model = Post
		fields = ('title','image','content','category')


class category_form(forms.ModelForm):
  class Meta:
    model = Category
    fields = ('categoryName',)


class comment_form(forms.ModelForm):
  class Meta:
    model=Comment
    fields=('comment_text',)


class reply_form(forms.ModelForm):
  class Meta:
    model=Reply
    # self.fields['name'].initial

    fields=('replay_text',)


class ForbiddenWordsForm(forms.ModelForm):
    class Meta:
        model = ForbiddenWords
        fields = ('forbiddenWord',)

