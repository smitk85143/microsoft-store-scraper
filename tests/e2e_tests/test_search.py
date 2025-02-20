from unittest import TestCase

from microsoft_store_scraper.features.search import search


class TestSearch(TestCase):
    def test_e2e_scenario_1(self):
        """
        Check if apps are found based on the search query and if all app properies are correct.
        """
        results = search("ubuntu")

        self.assertGreater(len(results), 0)

        for result in results:
            if result["productId"] == "9pnksf5zn4sw":
                break

        self.assertTrue("Ubuntu 18.04.6 LTS" in result["title"])
        self.assertEqual("9pnksf5zn4sw", result["productId"])
        self.assertTrue("Install a complete Ubuntu terminal environment" in result["description"])
        self.assertTrue(1.0 < result["averageRating"] < 5.0)
        self.assertEqual(0, result["price"])
        self.assertEqual("Canonical Group Limited", result["developerName"])
        self.assertEqual(['Developer tools'], result["categories"])
        self.assertTrue(result["images"])


    def test_e2e_scenario_2(self):
        """
        Test for limited number of results.
        """
        n_hits = 3
        results = search("ubuntu", n_hits=n_hits)
        self.assertEqual(len(results), n_hits)


    def test_e2e_scenario_3(self):
        """
        Test for media type filter.
        """

        results = search("ubuntu", media_type="games")
        for result in results:
            self.assertNotEqual('Apps', result["productFamilyName"])

    def test_e2e_scenario_4(self):
        """
        Test for price type filter.
        """

        results = search("ubuntu", price_type="Paid")

        for result in results:
            self.assertNotEqual(0, result["price"])
