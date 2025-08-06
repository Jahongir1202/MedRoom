from datetime import timedelta
from django.utils import timezone
from .models import Place

def clear_expired_places():
    now = timezone.now()
    expired_places = Place.objects.filter(day__isnull=False)

    for place in expired_places:
        expire_time = place.created_at + timedelta(days=place.day or 0)
        if now >= expire_time:
            # Joy bo‘shatamiz
            place.name = ''
            place.last_name = ''
            place.phone_number = None
            place.job = ''
            place.brought = ''
            place.price = None
            place.price_nurse = None
            place.day = None
            place.is_full_room = False
            place.save()

