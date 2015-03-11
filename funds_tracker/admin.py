from django.contrib import admin
from funds_tracker.models import Donation, PartyInfo


class DonationAdmin(admin.ModelAdmin):
    fields = ['year', 'party', 'donor', 'address', 'party_state', 'state',
              'postcode', 'donor_type', 'amount']
    list_display = ('year', 'party', 'party_state', 'state', 'donor_type',
                    'amount')


class PartyInfoAdmin(admin.ModelAdmin):
    fields = ['party', 'logo', 'wiki_page']
    list_display = ('party', 'logo', 'wiki_page')


# Register your models here.
admin.site.register(Donation, DonationAdmin)
admin.site.register(PartyInfo, PartyInfoAdmin)
