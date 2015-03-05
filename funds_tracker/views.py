#from django.shortcuts import render
from django.views import generic
from funds_tracker.models import Donation
from django.db.models import Max, Sum

# Create your views here.
MAIN_PARTIES = ['Australian Greens']


class IndexView(generic.ListView):
    model = Donation
    template_name = 'funds_tracker/index.html'
    context_object_name = 'all_donations'

    def get_queryset(self):
        #Get the most recent year
        max_year = Donation.objects.all().agregate(Max('year'))['year__max']
        #Get all objects for that year
        max_year_objects = Donation.objects.filter(year=max_year.__str__(),
                                                   party_state='FED')
        #Get the totals for the major national parties
        totals = {}
        for party in MAIN_PARTIES:
            totals[party] = max_year_objects.filter(party=party).\
                aggregate(Sum('amount'))
            print totals
        return Donation.objects.order_by('year')
