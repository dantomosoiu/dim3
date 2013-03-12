from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm, PasswordInput

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)
    # These fields are optional
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='imgs', blank=True)

    def __unicode__(self):
        return self.user.username


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]

class UserProfileForm(ModelForm):
    class Meta:
        fields=['website','picture']
        model = UserProfile

class loginForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]