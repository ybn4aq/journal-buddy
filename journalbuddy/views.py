from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib import messages
from .models import Journal
from .forms import JournalForm
from django.views import generic
from .models import Journal

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