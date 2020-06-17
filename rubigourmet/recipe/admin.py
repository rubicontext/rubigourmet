from django.contrib import admin

# Register your models here.

from .models import Ingredient
from .models import IngredientQuantity
from .models import Recipe
from .models import Book

admin.site.register(Ingredient)
admin.site.register(IngredientQuantity)
#admin.site.register(Recipe)
admin.site.register(Book)

#class TrackInline(admin.StackedInline):
class IngredientQuantityInline(admin.TabularInline):
    model = IngredientQuantity
    extra = 1

class RecipeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['name', 'description', 'url']}),
        ('Other information', {'fields': ['image', 'comment']}),
    ]
    inlines = [IngredientQuantityInline]
    list_display = ('name', 'image_tag', 'date_added')

#admin.site.register(IngredientQuantity, IngredientQuantityInline)
admin.site.register(Recipe, RecipeAdmin)