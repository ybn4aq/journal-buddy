from django.contrib import admin
from django.urls import path, include
from . import views
# from .views import edit_journal_entry

urlpatterns = [
    path('list/',views.JournalList.as_view(template_name='journalList.html'), name="list"),
    path('journal/<str:username>/<int:year>/<int:month>/<int:day>/', views.JournalList.journal_for_user_and_day, name='journal_for_day'),
    path("", views.HomeView.as_view(), name="home"),
    path("login/", views.user_login, name="login"),
    path("signup/", views.user_signup, name="signup"),
    path("logout/", views.user_logout, name="logout"),
    # path('journal/<str:username>/<int:year>/<int:month>/<int:day>/', views.JournalList.journal_for_user_and_day, name='journal_for_day'),
    path('journal/<str:username>/<int:journal_id>/', views.JournalList.journal_for_user_and_day, name='journal_for_day'),
    path('journalform/', views.journal, name="journalform"),
    path('user_home/', views.user_home, name='user_home'),
    path('cheerup/',views.PickMeUp.as_view(),name='pick_me_up'),
    path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
    # path('journal/<uuid:id>/', views.journal_detail, name='journal_detail'),  # Adjusted to use journal's id
]
