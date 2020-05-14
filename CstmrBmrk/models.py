from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.auth.models import Group,Permission
from CstmrBmrkMgr import settings

class Customer(AbstractUser):
    class Meta:
        db_table="Customer"
    mobile_no=models.BigIntegerField(unique=True,blank=False)
    geo_location = models.PointField(null=False, blank=False, srid=4326, verbose_name="geo_location")
    

class Bookmark(models.Model):
    

    title=models.CharField(max_length=500)
    url=models.TextField()
    source_name = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

class CustomerBookmark(models.Model):

    customer=models.ForeignKey(Customer,related_name="customer",on_delete=models.CASCADE,null=True)
    bookmark=models.ForeignKey(Bookmark,related_name="customer_bookmark",on_delete=models.CASCADE,null=True)








