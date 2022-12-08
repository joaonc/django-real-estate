from django.contrib import admin

from .models import Listing


class ListingAdmin(admin.ModelAdmin):
    # Which properties from the listing to display as columns
    list_display = (
        'id',
        'title',
        'price',
        'list_date',
        'realtor',
        'is_published',
    )

    # Which properties are clickable to edit
    list_display_links = (
        'id',
        'title',
    )

    # Which properties can filter by
    list_filter = (
        'realtor',
        'is_published',
    )

    # Which properties are editable
    list_editable = ('is_published',)

    # Which properties are searchable
    search_fields = (
        'title',
        'description',
        'address',
        'city',
        'state',
        'price',
    )

    # Pagination
    list_per_page = 25


admin.site.register(Listing, ListingAdmin)
