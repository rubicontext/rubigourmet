import datetime

from django.db import models
from django.utils import timezone

# Create your models here.

class Ingredient(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True, null=True)
    unit = models.CharField(max_length=200)
    comment = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return self.name

class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    url = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added to book', auto_now_add=True, blank=True, null=True)
    #ingredientQuantities = models.ManyToManyField(IngredientQuantity, )
    comment = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)
    def __str__(self):
        return self.name

class IngredientQuantity(models.Model):
    quantity = models.IntegerField()
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, blank=True, null=True)
    def __str__(self):
        return str(self.quantity) + " " +  self.ingredient.name



class Book(models.Model):
    name_user = models.CharField(max_length=50)
    recipes = models.ManyToManyField(Recipe)
    def __str__(self):
        return self.track.title + " - " +  self.date_played