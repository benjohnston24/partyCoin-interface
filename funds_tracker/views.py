#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name: views.py

Purpose: funds_tracker app views script

Created: Wed Mar 11 13:07:22 AEDT 2015
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = "Wed Mar 11 13:07:30 AEDT 2015"
__license__ = 'MPL v2.0'

## LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://moziljla.org/MPL/2.0/.

# Django usage is subject to the terms and conditions of the FREE-BSD license
# https://github.com/django/django/blob/master/LICENSE
##IMPORTS#####################################################################

from django.shortcuts import render
from django.views import generic
from funds_tracker.models import Donation, PartyInfo
from django.db.models import Max, Sum
from graphos.renderers import gchart
from graphos.sources.simple import SimpleDataSource
import matplotlib.pyplot as plt
from StringIO import StringIO
import base64

import operator
##############################################################################
#The number of top parties to list in the summary
NO_TOP_PARTIES = 4


#Rename to summaryview
class IndexView(generic.ListView):
    #model = Donation
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

        #Get the logos and wiki pages of the most well funded parties
        for i in range(len(filtered_parties)):
            w_l = PartyInfo.objects.filter(party=filtered_parties[i][0]).\
                values('logo', 'wiki_page')
            filtered_parties[i] += (w_l[0]['logo'], w_l[0]['wiki_page'])
        #print filtered_parties

        #Temp
        x = [1, 2, 3, 4, 5]
        y = [1, 2, 3, 4, 5]
        fig = plt.plot(x, y)
        chart_buffer = StringIO()
        plt.savefig(chart_buffer, format="png")
        chart = base64.b64encode(chart_buffer.getvalue())

        return {'summary': filtered_parties,
                'chart': chart}
        #return Donation.objects.order_by('year')


class ImageView(generic.ListView):
    model = PartyInfo
    template_name = 'funds_tracker/logos.html'
    context_object_name = 'partyInfo'

    def get_queryset(self):
        return PartyInfo.objects.all().order_by('party')


def party(request, pk):
    party = PartyInfo.objects.filter(party=pk)
    context = {'party': party}
    return render(request, 'funds_tracker/party.html', context)
