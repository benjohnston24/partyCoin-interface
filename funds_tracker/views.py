#from django.shortcuts import render
from django.views import generic
from funds_tracker.models import Donation
from django.db.models import Max, Sum

# Create your views here.
MAIN_PARTIES = ['Australian Labor Party (ALP)',
                'Liberal Party of Australia',
                'Australian Greens',
                ]


class IndexView(generic.ListView):
    model = Donation
    template_name = 'funds_tracker/index.html'
    context_object_name = 'major_national_parties'

    def get_queryset(self):
        #Get the most recent year
        max_year = Donation.objects.all().aggregate(Max('year'))['year__max']
        #Get all objects for that year
        max_year_objects = Donation.objects.filter(year=max_year.__str__(),
                                                   party_state='FED')
        parties = max_year_objects.values_list('party', flat=True).\
            order_by('party').distinct()
        #Get the totals for the major national parties
        totals = {}
        for party in parties:
            totals[party] = max_year_objects.filter(party=party).\
                aggregate(Sum('amount'))['amount__sum'].__int__()
        return totals
        #return Donation.objects.order_by('year')
