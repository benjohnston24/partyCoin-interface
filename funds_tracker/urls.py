#! /usr/bin/env python
"""!
-----------------------------------------------------------------------------
File Name : urls.py

Purpose: url handler for funds_tracker app

Created: 01-Mar-2015 23:32:20 AEDT
-----------------------------------------------------------------------------
Revision History



-----------------------------------------------------------------------------
S.D.G
"""
__author__ = 'Ben Johnston'
__revision__ = '0.1'
__date__ = '01-Mar-2015 23:32:20 AEDT'
__license__ = 'MPL v2.0'

# LICENSE DETAILS############################################################
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# IMPORTS#####################################################################
from django.conf import settings
from django.conf.urls import patterns, url
from django.conf.urls.static import static
from funds_tracker import views
##############################################################################

urlpatterns = patterns('',
                       url(r'^$', views.IndexView.as_view(), name='index'),
                       url(r'^logos/$', views.ImageView.as_view(),
                           name='funds-tracker-logos'),
                       url(r'^partyview/(?P<pk>.+)/$', views.PartySummaryView,
                           name='party-view'),
                       url(r'^party/(?P<pk>[^/]+)/year/(?P<pk_y>\w+)/$',
                           views.PartyYearView, name='party-year'),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                                    'document_root': settings.MEDIA_ROOT,
                                                    'show_indexes': True})
                       )
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
