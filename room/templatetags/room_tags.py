from django import template

register = template.Library()

@register.filter
def get_slot(places, slot_name):
    return places.filter(place_slot=slot_name).first()
