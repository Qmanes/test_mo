
import requests
from ..models import Specie, Habitat,EggGroup
from .evolution_chain import prepare_save as prepare_save_evolution_chain
from ..services.connection_api import api_get

def prepare_specie_and_evolution_chain(pokemon_api_response):

    species_url = pokemon_api_response.get("species").get("url")

    specie_api_response = api_get(species_url)

    prepare_save_evolution_chain(specie_api_response)

    return save(specie_api_response)

def save(specie_api_response):

    specie = Specie()

    specie.set_by_pokemon_api(specie_api_response)

    param = (specie, specie_api_response)

    __set_type_by_api_response(*param)

    __set__habit_by_api_response(*param)
    
    specie.save()

    __set_egg_group(*param)

    return specie

def __set_type_by_api_response(specie, specie_api_response):

    for genera in specie_api_response.get('genera'):
        
        if genera.get('language').get("en"):
            
            specie.type = genera.get("genus")

def __set__habit_by_api_response(specie, specie_api_response):

    response_habitat = api_get(specie_api_response.get("habitat").get("url"))

    habitat, created = Habitat.objects.get_or_create(
            id=response_habitat.get("id"),
            name_txt=response_habitat.get("name")
        )

    specie.habitat = habitat

def __set_egg_group(specie, specie_api_response):
	
	for egg_group_iter in specie_api_response.get('egg_groups'):
    		
		response_egg_group = api_get(egg_group_iter.get("url"))

		egg_group, created = EggGroup.objects.get_or_create(
			id=response_egg_group.get("id"),
			name_txt=response_egg_group.get("name")
		)

		specie.egg_group.add(egg_group)