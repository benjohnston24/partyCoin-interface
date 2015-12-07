from django.test import TestCase
from utilities import get_donation_year_total

# Create your tests here.


class DonationTests(TestCase):

    def test_yearly_totals(self):
        self.assertEqual(get_donation_year_total(u'Liberal Party of Australia',
                                                 u'2008'), 2107077.76)
