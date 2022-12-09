from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Listing


def listings(request):
    listings_ = Listing.objects.all()
    paginator = Paginator(listings_, 2)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id: int):
    return render(request, 'listings/listing.html')


def search(request):
    return render(request, 'listings/search.html')
