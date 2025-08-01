from django.urls import path
from . import views

urlpatterns = [
    path('', views.medroom_list, name='medroom-list'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('room/<int:room_id>/place/<str:slot>/', views.place_create, name='place-create'),
    path('place/<int:pk>/update/', views.PlaceUpdateView.as_view(), name='place-update'),
    path('place/<int:pk>/delete/', views.PlaceDeleteView.as_view(), name='place-delete'),
    path('place/<int:pk>/', views.PlaceDetailView.as_view(), name='place-detail'),
    path('expenses/edit/<int:pk>/', views.edit_expense, name='edit_expense'),  # ✅ to‘g‘rilandi
    path('expenses/delete/<int:pk>/', views.delete_expense, name='delete_expense'),
]
