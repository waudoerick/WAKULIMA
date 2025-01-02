from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from ckeditor.fields import RichTextField
class Crop(models.Model):
    """A crop the user produces."""
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return A string representation of the model."""
        return self.text

class Entry(models.Model):
    """Something specific  noted about  a crop."""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    text =  models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'entries'
    def __str__(self):
        """Return a string representation of the model."""
        return f"{self.text[:50]}..."
class Wakulima(models.Model):
    First_Name = models.CharField(max_length=40)
    Last_Name = models.CharField(max_length=40)
    Id_Number = models.CharField(max_length=15)
    Email = models.EmailField(max_length=40)
    Phone_Number = PhoneNumberField(max_length=15)
    Farm_size = models.CharField(max_length=10)
    Farm_Number = models.CharField(max_length=15,primary_key=True)
    Crop_Name = models.CharField(max_length=30)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.First_Name

class Post(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    body = RichTextField(blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_added']

    def __str__(self):
        return self.title  

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = RichTextField(blank=True, null=True)
    #body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self):
        return self.name  

class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    subcounty = models.CharField(max_length=200)
    location = models.CharField(max_length=200) 
    subject = RichTextField(blank=True, null=True)

    def __str__(self):
        return self.name  
        


    