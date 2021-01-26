from ..services.connection_api import api_get
from .specie import prepare_specie_and_evolution_chain
from .evolution_chain import recursive_save as recursive_save_evolution_chain
from ..models import Pokemon, Stat, BaseStat, Ability, PokemonType
from ..presenters.pokemon import PokemonPresenter, PokemonTypePresenter, PokemonAbilityPresenter, BaseStatPresenter,SpecialPresenter, EvolutionChainPresenter

def search_on_pokemon_api(pokemon_id):

    url = "https://pokeapi.co/api/v2/pokemon/{pokemon_id}".format(pokemon_id = pokemon_id)

    return api_get(url)


def save(pokemon_api_response):

    pokemon = Pokemon()

    pokemon.set_by_pokemon_api(pokemon_api_response)

    pokemon.specie = prepare_specie_and_evolution_chain(pokemon_api_response)

    pokemon.save()

    param = (pokemon,pokemon_api_response)

    __set_abilities(*param)

    __set_types(*param)

    __set_bases_stats(*param)

    return pokemon

def __set_abilities(pokemon, pokemon_api_response):

    for ability_iter in pokemon_api_response.get('abilities'):
        
        response_ability = api_get(ability_iter.get("ability").get("url"))

        ability, created = Ability.objects.get_or_create(
            id=response_ability.get("id"),
            name_txt=response_ability.get("name")
        )

        pokemon.ability.add(ability)

def __set_types(pokemon, pokemon_api_response):

    for type_iter in pokemon_api_response.get('types'):
        
        response_type = api_get(type_iter.get("type").get("url"))

        type, created = PokemonType.objects.get_or_create(
            id=response_type.get("id"),
            name_txt=response_type.get("name")
        )

        pokemon.type.add(type)

def __set_bases_stats(pokemon, pokemon_api_response):

    stats = pokemon_api_response.get('stats')

    for stat_iter in stats:

        response_stat = api_get(stat_iter.get("stat").get("url"))

        stat, created = Stat.objects.get_or_create(
            id=response_stat.get("id"),
            name_txt=response_stat.get("name")
        )

        base_stat_value = stat_iter.get('base_stat')

        base_stat, created = BaseStat.objects.get_or_create(
            pokemon=pokemon,
            stat=stat
        )

        base_stat.base_stat=base_stat_value

        base_stat.save()

def get_presenter(pokemon_id):

    pokemon_get = Pokemon.objects.get(id=pokemon_id)

    pokemon_presenter = PokemonPresenter(pokemon_get)

    special_presenter = SpecialPresenter(pokemon_get.specie)

    evolution_chain_presenter = EvolutionChainPresenter(pokemon_get.specie.evolutionchain)

    return pokemon_presenter, special_presenter, evolution_chain_presenter