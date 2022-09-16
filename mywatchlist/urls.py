from django.urls import path
from mywatchlist.views import show_watchlist_html, get_watchlist_json, get_watchlist_xml

app_name = 'mywatchlist'

urlpatterns = [
    path("html/", show_watchlist_html, name='show_watchlist_html'),
    path("xml/", get_watchlist_xml, name='get_watchlist_xml'),
    path("json/", get_watchlist_json, name='get_watchlist_json'),
]