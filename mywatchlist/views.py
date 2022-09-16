from django.shortcuts import render
from mywatchlist.models import MyWatchList
from django.http import HttpResponse
from django.core import serializers

# Create your views here.
def show_watchlist_html(request):
    data_watchlist = MyWatchList.objects.all()
    watchlist_message = ""

    if (MyWatchList.objects.filter(watched=True).count() >= MyWatchList.objects.filter(watched=False).count()):
        watchlist_message = "Selamat, kamu sudah banyak menonton!"
    else:
        watchlist_message = "Wah, kamu masih sedikit menonton!"

    context = {
        "watchlist": data_watchlist,
        "watchlist_message": watchlist_message,
    }

    return render(request, "watchlist.html", context)

def get_watchlist_xml(request):
    data_watchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("xml", data_watchlist), content_type="application/xml")

def get_watchlist_json(request):
    data_watchlist = MyWatchList.objects.all()
    return HttpResponse(serializers.serialize("json", data_watchlist), content_type="application/json")
