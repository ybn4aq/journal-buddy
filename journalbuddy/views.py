from django.shortcuts import render
from django.views import generic
from .models import Journal

# Create your views here.
class JournalList(generic.ListView):
    model = Journal
    template_name = "journalList.html"
    context_object_name = "journal_list"
    
    def get_queryset(self):
        entries = Journal.objects.all()
        return entries