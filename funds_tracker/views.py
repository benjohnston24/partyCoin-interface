#from django.shortcuts import render
from django.views import generic
from funds_tracker.models import Donation
from django.db.models import Max, Sum
import operator

# Create your views here.
MAIN_PARTIES = ['Australian Labor Party (ALP)',
                'Liberal Party of Australia',
                'Australian Greens',
                ]
#The number of top parties to list in the summary
NO_TOP_PARTIES = 5


#Rename to summaryview
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
        sorted_totals = sorted(totals.items(), key=operator.itemgetter(1),
                               reverse=True)
        #Create a blank list to return
        filtered_parties = []
        #Return only the most well funded parties
        for i in range(NO_TOP_PARTIES):
            filtered_parties.append((sorted_totals[i][0].__str__(),
                                    sorted_totals[i][1]))
        return filtered_parties
        #return Donation.objects.order_by('year')
