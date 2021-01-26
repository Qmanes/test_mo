from django.db import models

# aplica herencia

class Pokemon(models.Model):

    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)
    height = models.FloatField()
    weight = models.FloatField()
    picture_url = models.CharField(max_length=200, blank=True)
    bases_stats = models.ManyToManyField("Stat", through='BaseStat')
    ability = models.ManyToManyField("Ability")
    type = models.ManyToManyField("PokemonType")
    specie = models.OneToOneField("Specie", on_delete=models.CASCADE, default = 0)

    def set_by_pokemon_api(self, response):

        self.id = response.get('id')
        self.name_txt = response.get('name')
        self.height = response.get('height')
        self.weight = response.get('weight')
        self.picture_url = response.get('sprites').get("other").get("dream_world").get("front_default")
        

class Stat(models.Model):

    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)

class BaseStat(models.Model):

	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
	stat = models.ForeignKey(Stat, on_delete=models.CASCADE)
	base_stat = models.IntegerField(default=0)

class Specie(models.Model):

    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    base_happiness = models.FloatField()
    capture_rate = models.FloatField()  
    habitat = models.ForeignKey("Habitat", on_delete = models.CASCADE)
    egg_group = models.ManyToManyField("EggGroup")

    def set_by_pokemon_api(self, response):

        self.id = response.get('id')
        self.name_txt = response.get('name')
        self.base_happiness = response.get('base_happiness')
        self.capture_rate = response.get('capture_rate')
        self.color = response.get('color').get("name")

class EggGroup(models.Model):
    
    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)

class Habitat(models.Model):
    
    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)

class PokemonType(models.Model):
    
    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)

class Ability(models.Model):
    
    id = models.IntegerField(default=0,primary_key=True)
    name_txt = models.CharField(max_length=200)

class EvolutionChain(models.Model):

    chain_id = models.IntegerField()
    specie = models.OneToOneField("Specie", on_delete = models.CASCADE,primary_key=True, unique=True)
    evolution_to = models.ForeignKey("Specie", on_delete = models.CASCADE, null = True, related_name="evolution_to")
    min_level = models.IntegerField(null=True)
    evolution_to = models.ForeignKey("Specie", on_delete = models.CASCADE, null = True, related_name="evolution_to")
    evolution_from = models.ForeignKey("Specie", on_delete = models.CASCADE, null = True, related_name="evolution_from")