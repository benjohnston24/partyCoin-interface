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
from funds_tracker.models import Donation, PartyInfo
##############################################################################


def get_donation_year_total(party_name, party_year):
    return sum(Donation.objects.filter(party=party_name, year=party_year).
               values_list('amount', flat=True))
