from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, DetailView
from django.contrib import messages
from datetime import date
from .models import DailyReport
from .models import MedRoom, Place, Login, Expenses
from .forms import PlaceForm, LoginForm, ExpensesForm
from .tasks import clear_expired_places

def medroom_list(request):
    if 'user_id' not in request.session:
        return redirect('login')

    clear_expired_places()

    if request.method == 'POST' and 'price' in request.POST:
        room_id = request.POST.get('room')
        place_id = request.POST.get('place')
        room = MedRoom.objects.get(id=room_id) if room_id else None
        place = Place.objects.get(id=place_id) if place_id else None

        Expenses.objects.create(
            price=request.POST['price'],
            name=request.POST['name'],
            last_name=request.POST['last_name'],
            text=request.POST['text'],
            room=room,
            place=place
        )
        return redirect('medroom-list')

    rooms = MedRoom.objects.all().order_by('room')
    slots = ['joy1', 'joy2']
    username = request.session.get('username')

    expenses = Expenses.objects.all()
    total_expenses = sum(e.price for e in expenses)

    daily_reports = DailyReport.objects.order_by('-date')[:10]
    return render(request, 'rooms/room_list.html', {
        'rooms': rooms,
        'slots': slots,
        'username': username,
        'expenses': expenses,
        'total_expenses': total_expenses,
        'daily_reports': daily_reports,
    })

def place_create(request, room_id, slot):
    medroom = get_object_or_404(MedRoom, id=room_id)

    if request.method == 'POST':
        form = PlaceForm(request.POST)
        if form.is_valid():
            place = form.save(commit=False)
            place.med_room = medroom
            place.place_slot = slot
            place.is_rented = True
            place.save()
            update_daily_report()
            return redirect('medroom-list')
    else:
        form = PlaceForm()

    return render(request, 'rooms/place_form.html', {
        'form': form,
        'room': medroom,
        'slot': slot,
    })
class PlaceUpdateView(UpdateView):
    model = Place
    form_class = PlaceForm
    template_name = 'rooms/place_form.html'
    success_url = reverse_lazy('medroom-list')

    def form_valid(self, form):
        response = super().form_valid(form)
        from .services import update_daily_report
        update_daily_report()  # 🟢 YANGILAB QO‘YAMIZ
        return response


class PlaceDeleteView(DeleteView):
    model = Place
    template_name = 'rooms/place_confirm_delete.html'
    success_url = reverse_lazy('medroom-list')


class PlaceDetailView(DetailView):
    model = Place
    template_name = 'rooms/place_detail.html'

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            pwd = form.cleaned_data['password']
            try:
                user = Login.objects.get(username=uname, password=pwd)
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                return redirect('medroom-list')
            except Login.DoesNotExist:
                messages.error(request, 'Login yoki parol noto‘g‘ri!')
    else:
        form = LoginForm()

    return render(request, 'rooms/login.html', {'form': form})

def logout_view(request):
    request.session.flush()
    return redirect('login')



def edit_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == 'POST':
        form = ExpensesForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('medroom-list')  # ✅ tuzatildi
    else:
        form = ExpensesForm(instance=expense)
    return render(request, 'edit_expense.html', {'form': form})

def delete_expense(request, pk):
    expense = get_object_or_404(Expenses, pk=pk)
    if request.method == 'POST':
        expense.delete()
        return redirect('medroom-list')  # ✅ tuzatildi
    return render(request, 'delete_expense.html', {'expense': expense})

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