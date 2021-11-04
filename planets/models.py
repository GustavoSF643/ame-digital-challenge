from django.db import models

class Planet(models.Model):
    name = models.CharField(max_length=255)
    climate = models.CharField(max_length=255)
    terrain = models.CharField(max_length=255)
    movie_appearances = models.IntegerField()