from django.forms import ModelForm, TextInput, NumberInput
from .models import City, BankAccount

class CityForm(ModelForm):
    class Meta:
        model = City 
        fields = ['name']
        widgets = {'name' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}

    

class BankForm(ModelForm):
    class Meta:
        model = BankAccount 
        fields = ['bank_name','card_number']
       

        widgets = {
            'bank_name': TextInput(attrs={
                'class': 'input',
                'placeholder':'Bank Name...',
            }),
            'card_number': NumberInput(attrs={
                'class': 'input',
                'placeholder':' Card Number...',
        
            }),
        }