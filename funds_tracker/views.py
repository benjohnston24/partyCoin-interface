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

# LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://moziljla.org/MPL/2.0/.

# Django usage is subject to the terms and conditions of the FREE-BSD license
# https://github.com/django/django/blob/master/LICENSE
# IMPORTS#####################################################################

from django.shortcuts import render
from django.views import generic
from collections import OrderedDict
from funds_tracker.models import Donation, PartyInfo
from django.db.models import Max, Sum
from settings import STATES_ABBR, STATES_LIST

import operator
from utilities import get_donation_year_total, generate_pie_chart,\
    generate_bar_chart
from django.template.defaulttags import register

##############################################################################
# The number of top parties to list in the summary
NO_TOP_PARTIES = 4
LIBERAL_BLUE = '#1e6f88'
ALP_RED = '#B83537'
PALMER_YELLOW = '#dfff2c'
GREENS_GREEN = '#34e01d'
OTHERS = '#CA6FD6'
COLOURS = []


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='test')
def test_filter(xargs):
    # import pdb
    # db.set_trace()
    return str(xargs.strip(' '))


@register.filter(name='sort')
def sort_dict(value):
    if isinstance(value, dict):
        new_dict = OrderedDict()
        sorted_items = sorted(value.items())
        for item in sorted_items:
            new_dict[item[1]] = item[0]

        return new_dict
    elif isinstance(value, list):
        return sorted(value)
    else:
        return value


def get_summary(state):
    # Get the most recent year
    max_year = Donation.objects.all().aggregate(Max('year'))['year__max']
    # Get all objects for that year
    max_year_objects = Donation.objects.filter(year=max_year.__str__(),
                                               party_state=state.lower())
    parties = max_year_objects.values_list('party', flat=True).\
        order_by('party').distinct()
    # Get the totals for the most funded parties
    totals = {}
    grand_total = 0
    for party in parties:
        totals[party] = max_year_objects.filter(party=party).\
            aggregate(Sum('amount'))['amount__sum'].__int__()
        grand_total += totals[party]
    sorted_totals = sorted(totals.items(), key=operator.itemgetter(1),
                           reverse=True)
    # Create a blank list to return
    filtered_parties = []
    filtered_names = []
    filtered_values = []
    if len(totals) < NO_TOP_PARTIES:
        no_of_parties = len(totals)
    else:
        no_of_parties = NO_TOP_PARTIES
    # Return only the most well funded parties
    for i in range(no_of_parties):
        filtered_parties.append((sorted_totals[i][0].__str__(),
                                sorted_totals[i][1]))
        filtered_names.append(sorted_totals[i][0].__str__())
        filtered_values.append(sorted_totals[i][1])

    filtered_names.append('Others')
    filtered_values.append(grand_total - sum(filtered_values))
    # Get the logos and wiki pages of the most well funded parties
    for i in range(len(filtered_parties)):
        w_l = PartyInfo.objects.filter(party=filtered_parties[i][0]).\
            values('logo', 'wiki_page')
        # try:
        filtered_parties[i] += (w_l[0]['logo'], w_l[0]['wiki_page'])
        # except:
        # TODO handle this better
        # pass

    return (max_year, filtered_parties, filtered_names, filtered_values)


# Rename to summaryview
class IndexView(generic.ListView):
    # model = Donation
    template_name = 'funds_tracker/index.html'
    context_object_name = 'major_national_parties'

    def get_queryset(self):
        max_year_FED, filtered_parties_FED, filtered_names, filtered_values = \
            get_summary('FED')
        # Colours for pie chart
        COLOURS = []
        # TODO add database of colour codes for parties
        for name in filtered_names:
            if name.lower().find('liberal') >= 0:
                COLOURS.append(LIBERAL_BLUE)
            elif name.lower().find('labor') >= 0:
                COLOURS.append(ALP_RED)
            elif name.lower().find('palmer') >= 0:
                COLOURS.append(PALMER_YELLOW)
            elif name.lower().find('greens') >= 0:
                COLOURS.append(GREENS_GREEN)
            else:
                COLOURS.append(OTHERS)

        # Generate Pie chart of national donations
        # patches, texts, autotexts = plt.pie(filtered_values,
        #                                    labels=filtered_names,
        #                                    autopct='%1.1f%%',
        #                                    radius=0.8,
        #                                    wedgeprops={'edgecolor': 'white',
        #                                                'linewidth': 2},
        #                                    colors=COLOURS)
        # for t in texts:
        #    t.set_size('smaller')
        #    t.set_family('Arial')
        # for t in autotexts:
        #    t.set_size('smaller')
        #    t.set_color('white')
        #    t.set_weight('bold')
        # chart_buffer = StringIO()
        # plt.savefig(chart_buffer, bbox_inches='tight', format="png")
        # chart = base64.b64encode(chart_buffer.getvalue())
        chart = generate_pie_chart(filtered_names, filtered_values, COLOURS)

        # Create a dictionary for statewide summaries
        state_names = []
        state_values = {}

        # Get the NSW results
        for state in STATES_LIST:
            max_year, filtered_parties, filtered_names, filtered_values = \
                get_summary(state)
            state_names.append(STATES_ABBR[state])
            state_values[STATES_ABBR[state]] = filtered_parties

        # print state_values['New South Wales']
        return {'year': '%s - %d' % (max_year_FED, int(max_year_FED) + 1),
                'summary': filtered_parties_FED,
                'state_names': state_names,
                'state_values': state_values,
                'chart': chart,
                }


class ImageView(generic.ListView):
    model = PartyInfo
    template_name = 'funds_tracker/logos.html'
    context_object_name = 'partyInfo'

    def get_queryset(self):
        return PartyInfo.objects.all().order_by('party')


def PartySummaryView(request, pk):
    party = PartyInfo.objects.filter(party=str(pk).strip(' '))
    years = Donation.objects.filter(party=pk).order_by('-year')\
        .values_list('year', flat=True).distinct()
    amounts_by_year = {}
    amounts = []
    for year in years:
        amounts_by_year[str(year)] = round(get_donation_year_total(pk, year), 0)
        amounts.append(amounts_by_year[str(year)])

    chart = generate_bar_chart(years, amounts)
    context = {
        'name': pk,
        'party': party,
        'years': years,
        'amounts_by_year': amounts_by_year,
        'chart': chart,
    }

    template_name = 'funds_tracker/partyView.html'

    return render(request, template_name, context)


def PartyYearView(request, pk, pk_y):
    partyInfo = Donation.objects.filter(party=str(pk).strip(' '),
                                        year=str(pk_y).strip(' ')).order_by('-amount')

    template_name = 'funds_tracker/detailView.html'

    names = []
    amounts = []
    amounts_by_name = {}
    amounts_by_value = {}

    for party in partyInfo:
        names.append(party.get_donor())
        amounts.append(party.amount)
        amounts_by_name[party.get_donor()] = party.amount
        amounts_by_value[party.amount] = party.get_donor()

    chart = generate_pie_chart(names[0:5], amounts[0:5], ['b', 'g', 'r', 'k'])
    context = {
        'party': pk,
        'year': pk_y,
        'names': names,
        'amounts': amounts,
        'amounts_by_name': amounts_by_name,
        'amounts_by_value': amounts_by_value,
        'chart': chart,
    }

    return render(request, template_name, context)
