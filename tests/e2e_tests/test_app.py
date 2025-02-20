from unittest import TestCase

from microsoft_store_scraper.features.app import app


class TestApp(TestCase):
    def test_e2e_scenario_1(self):
        result = app("9pnksf5zn4sw")
        self.assertEqual("Ubuntu 18.04.6 LTS", result["title"])
        self.assertEqual("Canonical Group Limited", result["publisherName"])
        self.assertEqual("26737450", result["publisherId"])
        self.assertEqual("Free", result["displayPrice"])
        self.assertEqual("Application", result["productType"])
        self.assertEqual("2022-05-10T14:30:27.0096999Z", result["releaseDateUtc"])
        self.assertEqual(['Developer tools'], result["categories"])
        self.assertEqual("2024-04-17T16:35:34Z", result["lastUpdateDateUtc"])
        self.assertEqual("https://www.ubuntu.com/wsl", result["appWebsiteUrl"])

    def test_e2e_scenario_2(self):
        result = app("9n14cvww52gg")

        self.assertEqual("$4.99", result["displayPrice"])