import uuid

from django.db import models
from django.contrib.auth.models import User
from product.models import Item


class Wishlist(models.Model):
    user_session = models.CharField(max_length=255, default=uuid.uuid4())
    item = models.ManyToManyField(Item)
