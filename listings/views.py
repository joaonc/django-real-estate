from django.shortcuts import render

from .models import Listing


def listings(request):
    context = {
        'listings': Listing.objects.all()
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id: int):
    return render(request, 'listings/listing.html')


def search(request):
    return render(request, 'listings/search.html')
