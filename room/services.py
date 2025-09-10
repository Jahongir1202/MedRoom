from datetime import date
from .models import DailyReport, Place

def update_daily_report(place, old_total=None, deleted=False):
    """
    Kunlik hisobotni yangilash:
    - Yangi joy qo'shilsa -> summaga qo'shadi
    - Tahrir qilinsa -> farqni hisoblab qo'shadi/ayiradi
    - O'chirilsa -> hech nima qilmaydi
    """
    # services.py
    today = place.created_at.date() if place.created_at else date.today()
    report, _ = DailyReport.objects.get_or_create(date=today)

    if deleted:
        return report  # o'chirishda hisobot o'zgarmaydi

    if old_total is None:
        # yangi joy qo'shildi
        report.total_price += place.total_cost
    else:
        # tahrir qilindi
        diff = place.total_cost - old_total
        report.total_price += diff

    if report.total_price < 0:
        report.total_price = 0

    report.save()
    return report
