from django.contrib.auth.models import User
from django.db import models
from product.models import Item
import uuid


class Cart(models.Model):
    user_session = models.CharField(max_length=255, default=uuid.uuid4())
    item = models.ManyToManyField(Item)
    last_change = models.DateTimeField(auto_now_add=True)
