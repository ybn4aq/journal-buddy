from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from .models import Journal
from .forms import JournalForm
from django.views import generic
from .models import Journal
from .utils import Calendar
from django.utils.safestring import mark_safe
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from forms import LoginForm, SignupForm

# Create your views here.
def journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST, request.FILES)
        if form.is_valid():
            journal_instance = form.save(commit=False)
            journal_instance.date = form.cleaned_data["date"]
            journal_instance.content = form.cleaned_data["content"]
            journal_instance.rate = form.cleaned_data["rate"]
            journal_instance.save()
            return HttpResponseRedirect(reverse("journalbuddy"))
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
        context = super().get_context_data(**kwargs)
        context["entries"] = Journal.objects.all()
        return context

    def journal_for_user_and_day(request, username, year, month, day):
        user = get_object_or_404(User, username=username)
        try:
            journal_entry = Journal.objects.get(author=user, date__year=year, date__month=month, date__day=day)
        except Journal.DoesNotExist:
            raise Http404("No Journal entry found for this date.")

        return render(request, 'journalbuddy/solo_journal.html', {'journal_entry': journal_entry})
    

class CalendarView(generic.ListView):
    model = Journal
    template_name = "../templates/calendar.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = self.get_date(self.request.GET.get("day", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        return context

    def get_date(self, day):
        return datetime.today()
        if day:
            year, month = (int(x) for x in day.split('-'))
            return datetime.date(year, month, day=1)
        return datetime.today()
    

class HomeView(generic.TemplateView):
    template_name = "../templates/index.html"

def user_login(request):
    form = LoginForm(request.POST)
    if request.method == "POST":
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("/")  # TODO: make this user home page

def user_logout(request):
    logout(request)
    return redirect("login")

def user_signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            form = SignupForm()
        return render(request, "signup.html", {"form": form})
    
