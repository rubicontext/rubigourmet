from django.contrib import admin

# Register your models here.

from .models import Ingredient
from .models import IngredientQuantity
from .models import Recipe
from .models import Book

admin.site.register(Ingredient)
admin.site.register(IngredientQuantity)
admin.site.register(Recipe)
admin.site.register(Book)
