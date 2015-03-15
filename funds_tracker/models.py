from django.conf import settings
from django.db import models

# Create your models here.
class Donation(models.Model):
    year = models.CharField(max_length=20, default='')
    party = models.CharField(max_length=200, default='')
    donor = models.CharField(max_length=200, default='')
    address = models.CharField(max_length=200, default='')
    party_state = models.CharField(max_length=4, default='')
    state = models.CharField(max_length=3, default='')
    postcode = models.CharField(max_length=4, default='')
    donor_type = models.CharField(max_length=40, default='')
    amount = models.FloatField(default=0.0)

    def get_year(self):
        return self.year.__str__()

    def get_party(self):
        return self.party.__str__()

    def get_donor(self):
        return self.donor.__str__()

    def get_address(self):
        return self.address.__str__()

    def get_state(self):
        return self.state.__str__()

    def get_postcode(self):
        return self.postcode.__str__()

    def get_donor_type(self):
        return self.donor_type.__str__()

    def __str__(self):
        return '%s-%s:%s:$%0.2f' % (
               self.get_year(),
               self.get_party(),
               self.get_donor(),
               self.amount)


class PartyInfo(models.Model):
    party = models.CharField(max_length=200, default='')
    logo = models.CharField(max_length=500, default='')
    wiki_page = models.CharField(max_length=500, default='')
