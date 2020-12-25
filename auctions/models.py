from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=600)
    image_url = models.URLField()
    publisher = models.CharField(max_length=64)


class Bid(models.Model):
    bid = models.IntegerField()
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="bids")


class Comment(models.Model):
    comment = models.CharField(max_length=64)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments")


class Category(models.Model):
    category = models.CharField(max_length=64)
    listing_id = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="categories")
