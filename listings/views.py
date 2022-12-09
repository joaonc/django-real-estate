from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from listings.choices import bedroom_choices, price_choices, state_choices

from .models import Listing


def listings(request):
    listings_ = Listing.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(listings_, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings,
    }

    return render(request, 'listings/listings.html', context)


def listing(request, listing_id: int):
    listing_ = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing_,
    }

    return render(request, 'listings/listing.html', context)


def search(request):

    listings_ = Listing.objects.all()

    context = {
        'listings': listings_,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
    }

    return render(request, 'listings/search.html', context)
