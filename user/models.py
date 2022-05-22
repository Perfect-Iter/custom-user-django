from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager, PermissionsMixin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings

'''
model for holding all the users in the club. 
'''
class MyUsersManager(BaseUserManager):

    def create_user(self,email,last_name,username,phone_number,password, first_name, user_role):
        '''
        Manages the creation on student instances
        '''
        if not email:
            raise ValueError("Please add the school email address")
        if not last_name:
            raise ValueError("Please add an admission number")
        if not phone_number:
            raise ValueError("Please add a phone number")
        if not first_name:
            raise ValueError("Full name must be included")
        if not username:
            raise ValueError("User must have a username")
        if not password:
            raise ValueError("User must have a password")

        user = self.model(
            email=self.normalize_email(email),
            last_name = last_name,
            phone_number = phone_number,
            username=username,
            first_name = first_name,
            user_role =user_role
            
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self,email,password,phone_number,last_name,first_name,username,user_role):
        '''
        Manages the creation of superuser 
        '''
        user = self.create_user(
            email=self.normalize_email(email=email),
            password=password,
            username=username,
            first_name=first_name,
            phone_number=phone_number,
            last_name = last_name,
            user_role = user_role
            )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):

    USER_ROLE_CHOICES = (
      ('INTERN', 'intern'),
      ('EMP', 'employee'),
      ('SUP', 'supervisor'),
      ('NEW', 'new'),
 
                    )      
    
    email            = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username         = models.CharField(max_length=50,null= False,unique=True)
    first_name        = models.CharField(max_length=50,null= False)
    last_name        = models.CharField(max_length=50,null= False)
    phone_number     = models.BigIntegerField(unique=True,null= False)
    date_joined      = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login       = models.DateTimeField(verbose_name='last login', auto_now=True)
    user_role        = models.CharField(choices=USER_ROLE_CHOICES,max_length=6, default='NEW')
    is_admin         = models.BooleanField(default=False)
    is_active        = models.BooleanField(default=True)
    is_staff         = models.BooleanField(default=False)
    is_superuser     = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email','phone_number','first_name','last_name']

    objects = MyUsersManager()

    def __str__(self):
        return self.username

    def has_perm(self,perm, obj=None):
        return True
    
    def has_module_perms(self,app_label):
        return True