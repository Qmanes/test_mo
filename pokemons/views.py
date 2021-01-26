from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from django.forms.models import model_to_dict
from django.contrib import messages

from var_dump import var_dump
from django.core import serializers
from .uses_cases.pokemon import search_on_pokemon_api, save as save_pokemon, get_presenter
from .models import Pokemon
from .forms import PokemonForm
import json
from .presenters.pokemon import PokemonPresenterShema, PokemonTypePresenterShema, PokemonAbilityPresenterShema, \
						BaseStatPresenterShema,SpecialPresenterShema, EvolutionChainPresenterShema

def index(request):
    	
	pokemons = Pokemon.objects.all()

	form = PokemonForm()

	context = {
		"pokemons": pokemons,
		"form": form
	}
		
	return render(request,"pokemon/index.html", context)

def sync(request):
    	
	try:	 

		form = PokemonForm(request.POST)

		if form.is_valid():

			pokemon_api_response = search_on_pokemon_api(form.cleaned_data['pokemon_id'])

			save_pokemon(pokemon_api_response)

			messages.add_message(request, messages.SUCCESS, "Synchronization Success")

		messages.add_message(request, messages.ERROR, form.errors)

	except Exception as e:

		messages.add_message(request, messages.ERROR, e)
  		
	return redirect("index")
	
def detail(request, pokemon_id):
    	
	try:
    	
		pokemon_presenter, specie_presenter, evolution_chain_presenter = get_presenter(pokemon_id)

		context = {
			"pokemon_presenter": pokemon_presenter,
			"specie_presenter": specie_presenter,
			"evolution_presenter": evolution_chain_presenter
		}

	except Exception as e:

		messages.add_message(request, messages.ERROR, e)
  		
		return redirect("index")

	return render(request,"pokemon/detail.html", context)

def detail_api(request, pokemon_id):

	try:
    	
		pokemon_presenter, specie_presenter, evolution_chain_presenter = get_presenter(pokemon_id)

		json_response = {
			"pokemon" : PokemonPresenterShema().dump(pokemon_presenter),
			"specie": SpecialPresenterShema().dump(specie_presenter),
			"evolution": EvolutionChainPresenterShema().dump(evolution_chain_presenter),
		}


	except Exception as e:

		return JsonResponse({"msg": e}, status = 500)

	return JsonResponse(json_response)

def sync_api(request, pokemon_id):
    	    	
	try:
		pokemon_api_response = search_on_pokemon_api(pokemon_id)

		save_pokemon(pokemon_api_response)

		json_response = {
			"msg": "Sync Success"
		}
	
	except Exception as e:

		return JsonResponse({"msg": e}, status = 500)

	return JsonResponse(json_response)