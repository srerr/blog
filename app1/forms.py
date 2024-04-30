from django import forms
from app1.models import Comments,Subscribe,Post
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
class SubscribeForm(forms.ModelForm):
    class Meta:
        model=Subscribe
        fields='__all__'
        labels={'email':_('')}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].widget.attrs['placeholder']='enter email......'
class CommentForm(forms.ModelForm):
    class Meta:
        model=Comments
        fields={'content','email','name','website'}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['content'].widget.attrs['placeholder']='type your comment......'
        self.fields['email'].widget.attrs['placeholder']='email'
        self.fields['name'].widget.attrs['placeholder']='name'
        self.fields['website'].widget.attrs['placeholder']='website(optional)'
class NewUserForm(UserCreationForm):
    class Meta: 
        model=User
        fields=("username","email","password1","password2")
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['placeholder']='enter username'
        self.fields['email'].widget.attrs['placeholder']='email'
        self.fields['password1'].widget.attrs['placeholder']='enter password'
        self.fields['password2'].widget.attrs['placeholder']='confirm password'
    def clean_username(self):
        username=self.cleaned_data['username'].lower()
        new=User.objects.filter(username=username)
        if new.count():
            raise forms.ValidationError("user already exist")
        return username
    def clean_email(self):
        email=self.cleaned_data['email'].lower()
        new=User.objects.filter(email=email)
        if new.count():
            raise forms.ValidationError("email already exist")
        return email
    def clean_password2(self):
        password1=self.cleaned_data['password1']
        password2=self.cleaned_data['password2']
        if password1 and password2 and password1!=password2:
            raise forms.ValidationError("password not matched!")
        return password2
class PostForm(forms.ModelForm):
    class Meta:
        model=Post
        fields='__all__'
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['title'].widget.attrs['placeholder']='title of post'
        self.fields['content'].widget.attrs['placeholder']='write your post'
        self.fields['image'].widget.attrs['placeholder']='post image'