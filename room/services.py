from datetime import date
from .models import DailyReport, Place

def update_daily_report():
    today = date.today()

    # Bugungi band qilingan joylarni olish
    todays_places = Place.objects.filter(created_at__date=today, is_rented=True)

    # Jami narxni hisoblash
    total_price = sum(place.total_cost for place in todays_places)

    # Agar bugungi sana uchun record bor bo‘lsa yangilaydi, bo‘lmasa yaratadi
    report, created = DailyReport.objects.get_or_create(date=today)
    report.total_price = total_price
    report.save()
