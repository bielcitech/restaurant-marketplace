from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("L'utilisateur doit avoir un nom d'utilisateur")
        if not email:
            raise ValueError("L'utilisateur doit avoir une addresse mail")
        user = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password
        )
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # permissions
    is_active = models.BooleanField(default=True)
    is_vendor = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True, null=True)

    REQUIRED_FIELDS = ['username',]
    USERNAME_FIELD = 'email'

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser
    
    def has_module_perms(self, obj):
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', null=True, blank=True)
    cover_photo = models.ImageField(upload_to='users/cover_photos', null=True, blank=True)
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    address_line2 = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=15, null=True, blank=True)
    city = models.CharField(max_length=15, null=True, blank=True)
    pin_code = models.CharField(max_length=6, null=True, blank=True)
    latitude = models.CharField(max_length=20, null=True, blank=True)
    longitude = models.CharField(max_length=20, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.user.email
