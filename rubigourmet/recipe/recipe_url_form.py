from django import forms
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from recipe.models import Recipe, Ingredient, IngredientQuantity

import requests
import tempfile
import urllib.request
import time
from bs4 import BeautifulSoup
import pdb
from django.core import files
import shutil
from django.core.files import File
import os
import urllib.request
import math

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
        	
        	#return HttpResponseRedirect('/recipe?submitted=True')
        	return HttpResponseRedirect('/admin/recipe/recipe/%s/change/' % recipe.id)

    else:
        form = RecipeUrlForm()
        if 'submitted' in request.GET:
            submitted = True
 
    #return render(request, 'recipe/add_recipe_url.html', {'form': form, 'submitted': submitted})
    return render(request, 'recipe/add_recipe_url.html', {'form': form, 'submitted': submitted})

def scrap_recipe_from_url(url):
	
	#fake test
	#url = 'https://www.cuisineaz.com/recettes/taboule-au-chou-fleur-et-brocoli-102503.aspx?navdiapo=2713-1'

	recipe = Recipe()
	recipe.url = url
	recipe.save() #force save to add children

	#get page
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")

	#detect the domain and get appropriate tags
	domain_name = url.split('/')[2]

	if (domain_name == 'www.marmiton.org'):
		allItems = soup.findAll("li", {"class": "recipe-preparation__list__item"})
		allIngredientQty = soup.findAll("span", {"class": "recipe-ingredient-qt"})
		allIngredientUnitAndNames = soup.findAll("span", {"class": "ingredient"})
		allImages = soup.findAll("img", {"id": "recipe-media-viewer-main-picture"})
	elif (domain_name == 'www.cuisineaz.com'):
		allItems = soup.findAll("p", {"class": "p10"})
		ingredientSection = soup.find("section", {"class": "large-4 medium-4 small-12 columns recipe_ingredients"})
		allIngredientQty = ingredientSection.findAll("span")
		allIngredientUnitAndNames = 'MANUAL'
		allImages = soup.findAll("img", {"id": "ContentPlaceHolder_recipeImg"})

	#get title
	allTitles = soup.findAll('h1')
	allTitles
	#recipe.name = 'fake name'
	recipe.name = allTitles[0].contents[0]

	#TODO detect url domain, and store list of tags


	#get items list
	#allItems = soup.findAll("li", {"class": "recipe-preparation__list__item"})
	#current_item_tag = allItems[0]
	i=0
	for current_item_tag in allItems:
		currentListContent = ''
		for current_content in current_item_tag.contents:
			currentListContent =  current_content
		if i==0:
			recipe.description = '*' + currentListContent
		else:
			recipe.description = recipe.description + '\n' + currentListContent
		i=i+1

	#INGREDIENTS
	#allIngredientQty = soup.findAll("span", {"class": "recipe-ingredient-qt"})
	#allIngredientUnitAndNames = soup.findAll("span", {"class": "ingredient"})

	#loop on ingredient
	i=0
	for current_ingredient_qty in allIngredientQty:
		
		#print('ouuuuuuu')
		#print(current_ingredient_qty.contents)
		if(len(current_ingredient_qty.contents)<1):
			break
		currentQty = current_ingredient_qty.contents[0]
		#currentUnitAndName = allIngredientUnitAndNames[i].contents[0]
		
		#for some sites we need to split 
		if (allIngredientUnitAndNames == 'MANUAL'):
			currentUnitAndName = current_ingredient_qty.contents[0]
			currentQty = current_ingredient_qty.contents[0].split(' ')[0]
			if (not currentQty.isnumeric()):
				currentQty = 1
			else:
				currentUnitAndName = current_ingredient_qty.contents[0].split(' ', 1)[1]
		else:
			currentUnitAndName = allIngredientUnitAndNames[i].contents[0]
		#avoid non integer values in crappy websites
		currentQty = math.ceil(float(currentQty))


		#TODO get ingredient by name or create it
		ingredient = Ingredient()
		ingredient.name=currentUnitAndName
		ingredient.save()

		#init ingredient qty object and add it to recipe
		ingredientQty = IngredientQuantity()
		ingredientQty.ingredient = ingredient
		ingredientQty.quantity = currentQty
		ingredientQty.recipe = recipe
		ingredientQty.save()

		i = i+1

	#image
	#allImages = soup.findAll("img", {"id": "recipe-media-viewer-main-picture"})
	if (len(allImages) >0):
		img_url = allImages[0]['src']
		#recipe.comment = img_url

		# Steam the image from the url
		#request = requests.get(img_url, stream=True)
		
		# Get the filename from the url, used for saving later
		file_name = img_url.split('/')[-1]
		#content = urllib.request.urlretrieve(img_url)
		#recipe.image.save(file_name, File(open(content[0])), save=True)

		

		# save in the ImageField
		result = urllib.request.urlretrieve(img_url) # image_url is a URL to an image
		recipe.image.save(
    		file_name,
    		File(open(result[0], 'rb'))
    	)

		#SECOND ATTEMPT
		#request = requests.get(img_url, stream=True)
		#file = tempfile.NamedTemporaryFile()
		#request.raw.decode_content = True
		#shutil.copyfileobj(request.raw, file)
		#recipe.image = request.raw

	#recipe.name = 'fake name'
	recipe.save()
	return recipe
