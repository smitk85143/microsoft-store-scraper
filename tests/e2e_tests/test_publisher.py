from unittest import TestCase

from microsoft_store_scraper.features.publisher import publisher


class TestApp(TestCase):
    def test_e2e_scenario_1(self):
        result = publisher("WhatsApp Inc")

        for product in result:
            self.assertEqual(product["publisherName"], "WhatsApp Inc")

        