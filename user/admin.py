from django.contrib.auth.models import Group
from django import forms
from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django.contrib.auth.admin import UserAdmin
from user.models import CustomUser


class MyUserCreationForm(UserCreationForm):
    
    password = forms.CharField(
        label='Password',
        max_length = 32,
        required=True,
        widget=forms.PasswordInput,
        )

    password2 = forms.CharField(
        label='Confirm',
        max_length = 32,
        required=True,
        widget=forms.PasswordInput,
        help_text="Make sure they match!",
        )


    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password2', 'email',
            'first_name','last_name', 'phone_number',]
        help_texts = {
            'password': 'Must be at least 8 characters.',
        }


        def clean_username(self):
            username = self.cleaned_data['username']
            try:
                CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
                return username
            raise ValidationError(self.error_messages['duplicate_username'])
        

        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])

            if commit:
                user.save()
            return user

class MyUserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = CustomUser
        fields = ('username', 'password', 'email',
            'first_name','last_name', 'phone_number',)



# Register your models here.
class CustomUserAdminView(UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_filter = ('username','date_joined')
    


    
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'username',
            'email', 'phone_number',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('email', 'password', 'password2', 'first_name', 'last_name','username')}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()        


admin.site.register(CustomUser, CustomUserAdminView)
admin.site.unregister(Group)

admin.site.site_header = "This is a Blueprint"