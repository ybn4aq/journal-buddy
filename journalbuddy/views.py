from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import Journal
from .forms import JournalForm
from django.views import generic
from .models import Journal
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
    
    
    