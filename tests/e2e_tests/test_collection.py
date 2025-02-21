from unittest import TestCase

from microsoft_store_scraper.features.collection import collection


class TestApp(TestCase):
    def test_e2e_scenario_1(self):
        for media_type in ["apps", "games"]:
            results = collection("TopPaid", media_type)

            for result in results:
                self.assertNotEqual("Free", result['priceInfo']["displayPrice"])

    def test_e2e_scenario_2(self):
        for media_type in ["apps", "games"]:
            results = collection("TopFree", media_type)

            for result in results:
                self.assertEqual("Free", result["displayPrice"])