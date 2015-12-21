#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : utilities.py

Purpose:

Created: 08-Dec-2015 05:14:14 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '08-Dec-2015 05:14:14 AEDT'
__license__ = 'MPL v2.0'

# LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# IMPORTS#####################################################################
from funds_tracker.models import Donation
import matplotlib.pyplot as plt
from StringIO import StringIO
import base64
import numpy as np
##############################################################################


def get_donation_year_total(party_name, party_year):
    return sum(Donation.objects.filter(party=party_name, year=party_year).
               values_list('amount', flat=True))


def generate_pie_chart(names, values, colours=None):
    patches, texts, autotexts = plt.pie(values,
                                        labels=names,
                                        autopct='%1.1f%%',
                                        radius=0.8,
                                        wedgeprops={'edgecolor': 'white',
                                                    'linewidth': 2},
                                        colors=colours)
    for t in texts:
        t.set_size('smaller')
        t.set_family('Arial')
    for t in autotexts:
        t.set_size('smaller')
        t.set_color('white')
        t.set_weight('bold')
    chart_buffer = StringIO()
    plt.savefig(chart_buffer, bbox_inches='tight', format="png")
    return base64.b64encode(chart_buffer.getvalue())


def generate_bar_chart(names, values, colour=None):
    N = len(names)
    ind = np.arange(N)
    fig, ax = plt.subplots()
    ax.bar(ind, values[::-1], color='b', align='center', edgecolor='blue')
    disp_names = tuple(map(str, names[::-1]))
    ax.set_xticks(ind)
    ax.set_xticklabels(disp_names, ha='center', minor=False)
    ax.axes.get_yaxis().set_visible(False)

    for spine in ax.spines.itervalues():
        spine.set_visible(False)
    for tic in ax.axes.get_xticklines():
        tic.set_visible(False)

    chart_buffer = StringIO()
    plt.savefig(chart_buffer, bbox_inches='tight', format="png")

    return base64.b64encode(chart_buffer.getvalue())
