from django.test import TestCase, Client

# Create your tests here.
class MyWatchlistAppTest(TestCase):
    def test_watchlist_html_response_ok(self):
        response = Client().get("/mywatchlist/html/")
        self.assertEqual(response.status_code, 200)

    def test_watchlist_xml_response_ok(self):
        response = Client().get("/mywatchlist/xml/")
        self.assertEqual(response.status_code, 200)

    def test_watchlist_json_response_ok(self):
        response = Client().get("/mywatchlist/json/")
        self.assertEqual(response.status_code, 200)