
import requests
from ..models import EvolutionChain
from ..services.connection_api import api_get

def prepare_save(prepare_save_evolution_chain):

    evolution_chain_url = prepare_save_evolution_chain.get('evolution_chain').get("url")

    evolution_chai_api_response = api_get(evolution_chain_url)

    chain_id = evolution_chai_api_response.get("id")

    recursive_save(chain_id, evolution_chai_api_response.get("chain"))

def recursive_save(chain_id, chain, evolution_from = None):

    min_level = chain.get("evolution_details")[0].get("min_level") if chain.get("evolution_details") else None

    specie = __get_specie(chain)

    evolution_chain = EvolutionChain(chain_id = chain_id, min_level = min_level, specie = specie, evolution_from = evolution_from)

    if chain.get("evolves_to"):
        
        evolution_chain.evolution_to = recursive_save(evolution_chain.chain_id, chain.get("evolves_to")[0], evolution_chain.specie)

    evolution_chain.save()
    
    return evolution_chain.specie

def __get_specie(chain):

    from .specie import save as save_specie

    response_specie = api_get(chain.get("species").get("url"))

    return save_specie(response_specie)


