from django.db import models
from django.core.validators import MinLengthValidator, MaxValueValidator, MinValueValidator
from datetime import datetime   

# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=256)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Tag(models.Model):
    caption = models.CharField(max_length=20)
    
    def __str__(self):
        return self.caption


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(blank=True ,unique=True, db_index=True)
    summary = models.TextField(max_length=100)
    context = models.TextField(validators=[MinLengthValidator(300)])
    image = models.ImageField(upload_to="uploads/posts/")
    publish_time = models.DateTimeField(default=datetime.now)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True ,related_name='posts')
    tag = models.ManyToManyField(Tag)
    
    def __str__(self):
        return self.title
    

class Comment(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    comment = models.TextField(blank=False, null=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")

    def __str__(self):
        return self.name