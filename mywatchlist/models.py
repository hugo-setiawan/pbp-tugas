from django.db import models

# Create your models here.
class MyWatchList(models.Model):
    watched = models.BooleanField()
    title = models.TextField()
    rating = models.PositiveSmallIntegerField()
    release_date = models.DateField()
    review = models.TextField()