from django.urls import path

from . import views
from . import recipe_url_form

urlpatterns = [
    path('', views.index, name='index'),
    path('addrecipe/', recipe_url_form.add_recipe, name='add_recipe_view'),
]