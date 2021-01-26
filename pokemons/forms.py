from django import forms

class PokemonForm(forms.Form):
    
    pokemon_id = forms.IntegerField(label='Pokemon ID')