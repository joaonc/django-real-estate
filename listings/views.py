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
    queryset_list = Listing.objects.order_by('-list_date')

    if keywords := request.GET.get('keywords'):
        queryset_list = queryset_list.filter(description__icontains=keywords)

    if city := request.GET.get('city'):
        queryset_list = queryset_list.filter(city__iexact=city)

    if state := request.GET.get('state'):
        queryset_list = queryset_list.filter(state__iexact=state)

    if bedrooms := request.GET.get('bedrooms'):
        queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    if price := request.GET.get('price'):
        queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'listings': queryset_list,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'state_choices': state_choices,
        'values': request.GET,
    }

    return render(request, 'listings/search.html', context)
