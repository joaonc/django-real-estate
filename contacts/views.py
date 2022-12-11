from django.contrib import messages
from django.shortcuts import redirect

from contacts.models import Contact


def contact(request):
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has already made an inquiry
        if (
            int(user_id) > 0  # Could also use `request.user.id`
            and Contact.objects.all().filter(listing_id=listing_id, user_id=user_id).exists()
        ):
            messages.error(request, 'You have already made an inquiry for this listing')
            return redirect('/listings/' + listing_id)

        contact = Contact(
            listing=listing,
            listing_id=listing_id,
            name=name,
            email=email,
            phone=phone,
            message=message,
            user_id=user_id,
        )
        contact.save()

        messages.success(
            request,
            'Your request has been submitted, a realtor will get back to you soon.',
        )

        return redirect('/listings/' + listing_id)
