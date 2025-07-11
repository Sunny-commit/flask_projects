from django.db import models
from .category import Category
# Create your models here.
class Product(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to='img')
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    desc=models.TextField()
    price=models.IntegerField()