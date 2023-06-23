from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class newBlog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField(max_length=10000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    

class Comments(models.Model):
    blog = models.ForeignKey(newBlog, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.description}"