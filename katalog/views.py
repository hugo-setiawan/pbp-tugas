from multiprocessing import context
from django.shortcuts import render
from katalog.models import CatalogItem

def show_katalog(request):
    # get data from BarangKatalog
    data_item_catalog = CatalogItem.objects.all()

    context = {
        'list_item_catalog': data_item_catalog,
        'nama_student': 'Hugo Sulaiman Setiawan',
        'id_student': '2106707315'
    }

    # call render function with given data context
    return render(request, "katalog.html", context)