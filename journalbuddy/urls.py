from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.JournalList.as_view(template_name='journalList.html'), name="list"),
    path("calendar/", views.CalendarView.as_view(), name="calendar"),
    path('journal/<str:username>/<int:year>/<int:month>/<int:day>/', views.JournalList.journal_for_user_and_day, name='journal_for_day'),
    path("/", views.HomeView.as_view(), name="home")
]
