from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from recipe.models import Recipe

class RecipeUrlForm(forms.Form):
    url = forms.CharField(max_length=500, label='Url of the new recipe')

def add_recipe(request):
    submitted = False
    if request.method == 'POST':
        form = RecipeUrlForm(request.POST)
        if form.is_valid():
        	cd = form.cleaned_data
        	# assert False
        	#AC TODO, init new new object with url
        	recipe = scrap_recipe_from_url(cd['url'])
        	
        	return HttpResponseRedirect('/recipe?submitted=True')
    else:
        form = RecipeUrlForm()
        if 'submitted' in request.GET:
            submitted = True
 
    return render(request, 'recipe/add_recipe_url.html', {'form': form, 'submitted': submitted})

def scrap_recipe_from_url(url):
	recipe = Recipe()
	recipe.url = url
	recipe.name = 'fake name'
	recipe.save()
	return recipe
