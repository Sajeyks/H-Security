from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date
from PIL import Image
from django.core.exceptions import ValidationError
# Create your models here.

def validate_digits(value):
    if value and len(str(value)) < 8:
        raise ValidationError('ID number must have more than 8 digits.')

class UserManager(BaseUserManager):
    """ A manager class for the custom user model """

    def create_user(self, name, email, national_id_no, password=None):
        if name is None:
            raise TypeError('User must have a name')
        if email is None:
            raise TypeError('User must have an email')
        
        if national_id_no is None:
            raise TypeError('User must have an national_id_no')

        user = self.model(name=name, email=self.normalize_email(email), national_id_no=national_id_no)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, name, email,national_id_no, password=None):
        if password is None:
            raise TypeError('Password cannot be null')

        user = self.create_user(name, email,national_id_no, password)
        user.is_superuser = True
        user.is_active = True
        user.is_verified = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ The custom user model """

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, db_index=True)
    phone_number = PhoneNumberField(blank=False)
    national_id_no = models.PositiveIntegerField(unique=True, validators=[validate_digits])
    dob = models.DateField(default=date.today)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'national_id_no']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def age(self):
        today = date.today()
        dob = self.dob
        return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.TextField()
    
    def __str__(self):
        return self.user.email
    
    def save(self, *args, **kwargs):
        super().save()
        
        img = Image.open(self.avatar.path)
        
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
            
        
    