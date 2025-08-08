# admin.py
from django import forms
from django.contrib import admin
from .models import MedRoom, Place, Login, Expenses, DailyReport


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'last_name', 'phone_number', 'formatted_created_at']
    search_fields = ['name', 'last_name']
    ordering = ['-created_at']  # eng yangi yozuvlar birinchi

    def formatted_created_at(self, obj):
        return obj.created_at.strftime("%d-%m-%Y %H:%M")
    formatted_created_at.short_description = 'Qo‘shilgan vaqt'

@admin.register(MedRoom)
class MedRoomAdmin(admin.ModelAdmin):
    list_display = ['room', 'chamber_type', 'place']
@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ['username','password']

@admin.register(DailyReport)
class DailyReportAdmin(admin.ModelAdmin):
    list_display = ['total_price']


class ExpensesAdminForm(forms.ModelForm):
    class Meta:
        model = Expenses
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ExpensesAdminForm, self).__init__(*args, **kwargs)
        if 'room' in self.data:
            try:
                room_id = int(self.data.get('room'))
                room = MedRoom.objects.get(id=room_id)
                self.fields['place'].queryset = Place.objects.filter(id__in=[room.joy1.id, room.joy2.id])
            except (ValueError, TypeError, MedRoom.DoesNotExist):
                pass
        elif self.instance.pk and self.instance.room:
            room = self.instance.room
            self.fields['place'].queryset = Place.objects.filter(id__in=[room.joy1.id, room.joy2.id])
        else:
            self.fields['place'].queryset = Place.objects.none()

class ExpensesAdmin(admin.ModelAdmin):
    form = ExpensesAdminForm
    list_display = ('name', 'last_name', 'price', 'room', 'place')

admin.site.register(Expenses, ExpensesAdmin)
