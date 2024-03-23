from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('list/',views.JournalList.as_view(template_name='journalList.html'), name="list"),
    path("journal/<int:year>/<int:month>/<int:day>", views.JournalView.as_view(), name="journal")
]
