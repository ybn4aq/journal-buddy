from django.shortcuts import render
from .models import UserProfile

def user_profiles(request):
    profiles = UserProfile.objects.all()  # Fetch all UserProfile instances
    return render(request, 'journalbuddy/user_profiles.html', {'profiles': profiles})