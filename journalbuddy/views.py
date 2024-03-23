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
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def journal(request):
    if request.method == 'POST':
        form = JournalForm(request.POST)
        if form.is_valid():
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
        context = super().get_context_data(**kwargs)
        context["entries"] = Journal.objects.all()
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
