from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from .models import Journal
from .forms import JournalForm
from django.views import generic
from .models import Journal
from django.utils.safestring import mark_safe
import datetime
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required
import random
import requests
import json

# Create your views here.

@login_required
def journal(request):
    user = get_object_or_404(User, username=request.user.username)
    num_of_entries = 0
    try:
        entries = Journal.objects.filter(author=user)
        num_of_entries = len(entries)
        print(num_of_entries)
    except:
        num_of_entries = 0
    print(num_of_entries)
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            cont = form.cleaned_data["content"]
            rating = form.cleaned_data["rate"]
            report = Journal.objects.create(content=cont, rate=rating)
            report.author = request.user
            report.iteration = num_of_entries+1
            report.save()

            return HttpResponseRedirect(reverse("journalbuddy:list"))
    else:
        form = JournalForm()

    return render(request, "journalform.html", {'form': form})

class JournalList(generic.ListView):
    # model = Journal
    template_name = "journalList.html"
    context_object_name = "journal_list"
    
    def get_queryset(self):
        entries = Journal.objects.all()
        # return render(request, 'journalbuddy/journalList.html', {'profiles': entries})
        return entries
    
    def get_context_data(self, **kwargs):
        try:
            user = get_object_or_404(User, username=self.request.user.username)
            context = super().get_context_data(**kwargs)
            context["entries"] = Journal.objects.filter(author = user)
            todayexists = False #checking to see if there's an entry for today
            journal_entry = Journal.objects.filter(author=user, date = datetime.date.today())
            if len(journal_entry) > 0:
                todayexists = True
            else :
                todayexists = False

            context["todayexists"] = todayexists
            return context
        except:
            return redirect("login") #go to login page 

    def journal_for_user_and_day(request, username, journal_id):
        user = get_object_or_404(User, username=username)
        try:
            journal_entry = Journal.objects.get(author=user, id = journal_id)
        except Journal.DoesNotExist:
            raise Http404("No Journal entry found for this date.")

        return render(request, 'journalbuddy/solo_journal.html', {'journal_entry': journal_entry})
        
class PickMeUp(generic.ListView):
    model = Journal
    template_name = "pick_me_up.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.request.user.username)
        try:
            good_journals = Journal.objects.filter(author=user, rate__gte=4)
            if(len(good_journals) > 0): #if there's more than 0 things in the user's "good" journals
                random_item = random.choice(good_journals)
                context["random_item"] = random_item
                context["item_found"] = True
        except:
            context["item_found"] = False
        return context



    
    # def see_journal(request, journal_id):
    #     if request.user.is_authenticated:
    #         return render(request, "journalList.html", {"journal_id":journal_id})
    #     else:
    #         return redirect('')
    
# def journal_detail(request, id):
#     journal_entry = get_object_or_404(Journal, id=id)
#     return render(request, 'journalbuddy/solo_journal.html', {'journal_entry': journal_entry})


class HomeView(generic.TemplateView):
    template_name = "../templates/index.html"

def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("/user_home/")
            else:
                # Invalid username or password
                return HttpResponse("""
                                Invalid username or password. Please try again.
                                <br>
                                <a href="/"><button>Try Again</button></a>
                                """, content_type="text/html")
        else:
            return HttpResponse("Form is not valid. Please check your input.")
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
        

def user_logout(request):
    logout(request)
    return redirect("journalbuddy:login")

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("journalbuddy:login")
        else:
            return HttpResponse("Form is not valid. Please check your input.")
    else:
        form = SignupForm()
    return render(request, "signup.html", {"form": form})
  
@login_required
def user_home(request):
    user = get_object_or_404(User, username=request.user.username)
    todayexists = False #checking to see if there's an entry for today
    try:
        journal_entry = Journal.objects.filter(author=user, date = datetime.date.today())
        if len(journal_entry) > 0:
            todayexists = True
        else :
            todayexists = False
    except Journal.DoesNotExist:
        todayexists = False

# api call for random quote

    url = "https://zenquotes.io/api/random"
    response = requests.request("GET", url)
    if (response.status_code == 200):
        json_data = response.json()
        q = json_data[0]["q"]
    else:
        q = "You are worthy of happiness and peace of mind."
    return render(request, 'journalbuddy/user_home.html', {'username': request.user.username, 'todayexists' :todayexists, "quote": q})
