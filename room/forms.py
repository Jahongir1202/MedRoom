from django import forms
from .models import Place, MedRoom, Login, Expenses


class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        exclude = ['med_room', 'place_slot', 'created_at']
        widgets = {
            'is_full_room': forms.CheckboxInput()
        }
class MedRoomForm(forms.ModelForm):
    class Meta:
        model = MedRoom
        fields = '__all__'

class LoginForm(forms.ModelForm):
    class Meta:
        model = Login
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

class ExpensesForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'