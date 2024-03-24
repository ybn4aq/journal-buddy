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
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, SignupForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
            journal_instance = form.save(commit=False)
            journal_instance.date = form.cleaned_data["date"]
            journal_instance.content = form.cleaned_data["content"]
            journal_instance.rate = form.cleaned_data["rate"]
            journal_instance.save()
            return HttpResponseRedirect(reverse("journalbuddy"))
            cont = form.cleaned_data["content"]
            rating = form.cleaned_data["rate"]
            report = Journal.objects.create(content=cont, rate=rating)
            report.author = request.user
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
        user = get_object_or_404(User, username=self.request.user.username)
        context = super().get_context_data(**kwargs)
        context["entries"] = Journal.objects.filter(author = user)
        return context

    def journal_for_user_and_day(request, username, journal_id):
        user = get_object_or_404(User, username=username)
        try:
            journal_entry = Journal.objects.get(author=user, id = journal_id)
        except Journal.DoesNotExist:
            raise Http404("No Journal entry found for this date.")

        return render(request, 'journalbuddy/solo_journal.html', {'journal_entry': journal_entry})


    
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
                return redirect("/")
            else:
                # Invalid username or password
                return HttpResponse("Invalid username or password. Please try again.")
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
    return render(request, 'journalbuddy/user_home.html', {'username': request.user.username})
