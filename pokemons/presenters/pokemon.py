from var_dump import var_dump
from marshmallow import Schema, fields, post_load,pre_load


class basic():

    def __init__(self,id, name):

        self.id = id
        self.name = self.apply_format(name)

    def apply_format(self, string):

        string = string.capitalize()

        return string

class PokemonAbilityPresenterShema(Schema):
    
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return PokemonAbilityPresenter(**data)

class PokemonAbilityPresenter(basic):

    def __init__(self, ability):
    
        super().__init__(ability.id, ability.name_txt)

class PokemonTypePresenterShema(Schema):
    
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return PokemonTypePresenter(**data)

class PokemonTypePresenter(basic):

    def __init__(self, type):
    
        super().__init__(type.id, type.name_txt)

class BaseStatPresenterShema(Schema):
    
    base_stat = fields.Float()
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return BaseStatPresenter(**data)

class BaseStatPresenter(basic):

    def __init__(self, base_stat):

        self.base_stat = base_stat["basestat"]

        super().__init__(base_stat["id"], base_stat["name_txt"])

class PokemonPresenterShema(Schema):

    height = fields.Float()
    weight = fields.Float()
    picture_url = fields.Str()
    id = fields.Int()
    name = fields.Str()
    abilities = fields.Nested(PokemonAbilityPresenterShema, many=True)
    types = fields.Nested(PokemonTypePresenterShema, many=True)
    bases_stats = fields.Nested(BaseStatPresenterShema, many=True)

    @post_load
    def make(self, data, **kwargs):

        return PokemonPresenter(**data)

class PokemonPresenter(basic):

    def __init__(self, pokemon):
        
        self.height = pokemon.height
        self.weight = pokemon.weight
        self.picture_url = pokemon.picture_url
        self.set_abilities(pokemon)
        self.set_types(pokemon)
        self.set_base_stats(pokemon)

        super().__init__(pokemon.id, pokemon.name_txt)


    def set_types(self, pokemon):


        self.types=  map(lambda type_iter: PokemonTypePresenter(type_iter), pokemon.type.all())

    def set_abilities(self, pokemon):
        
        self.abilities=  map(lambda ability_iter: PokemonAbilityPresenter(ability_iter), pokemon.ability.all())

    def set_base_stats(self, pokemon):


        base_stats = pokemon.bases_stats.all()

        list_base_stat = list(base_stats.values("basestat","name_txt","id"))  

        self.bases_stats=  map(lambda base_stat: BaseStatPresenter(base_stat), list_base_stat)


class EvolutionChainPresenterShema(Schema):
    
    chain_id = fields.Int()
    evolution_to = fields.Str()
    min_level = fields.Str()
    evolution_from = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return EvolutionChainPresenter(**data)

class EvolutionChainPresenter():

    def __init__(self, evolution_chain):
    
        self.chain_id= evolution_chain.chain_id
        self.evolution_to = evolution_chain.evolution_to.name_txt.capitalize() if evolution_chain.evolution_to else None
        self.min_level= evolution_chain.min_level if evolution_chain.min_level else None
        self.evolution_from = evolution_chain.evolution_from.name_txt.capitalize() if evolution_chain.evolution_from else None

class SpecieHabitatPresenterSchema(Schema):
    
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return SpecieHabitatPresenter(**data)

class SpecieHabitatPresenter(basic):

    def __init__(self, ability):
    
        super().__init__(ability.id, ability.name_txt)

class SpecieEggGroupPresenterSchema(Schema):
    
    id = fields.Int()
    name = fields.Str()

    @post_load
    def make(self, data, **kwargs):

        return SpecieEggGroupPresenter(**data)

class SpecieEggGroupPresenter(basic):

    def __init__(self, ability):
    
        super().__init__(ability.id, ability.name_txt)

class SpecialPresenterShema(Schema):
    
    base_happiness = fields.Float()
    capture_rate = fields.Float()
    color = fields.Str()
    id = fields.Int()
    name = fields.Str()
    habitat =fields.Nested(SpecieHabitatPresenterSchema)
    egg_groups =fields.Nested(SpecieEggGroupPresenterSchema, many = True)

    @post_load
    def make(self, data, **kwargs):

        return SpecialPresenter(**data)

class SpecialPresenter(basic):

    def __init__(self, specie):

        self.base_happiness= specie.base_happiness
        self.capture_rate= specie.capture_rate
        self.color= self.apply_format(specie.color)
        self.habitat= SpecieHabitatPresenter(specie.habitat)
        self.set_egg_groups(specie)

        super().__init__(specie.id, specie.name_txt)

    def set_egg_groups(self, specie):

        self.egg_groups = []

        for egg_group in specie.egg_group.all():

            self.egg_groups.append(SpecieEggGroupPresenter(egg_group))