from django.shortcuts import render


def listings(request):
    return render(request, 'listings/listings.html')


def listing(request, listing_id: int):
    return render(request, 'listings/listing.html')


def search(request):
    return render(request, 'listings/search.html')
