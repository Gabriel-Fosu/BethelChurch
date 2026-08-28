from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Event, EventCategory, EventRegistration

# Create your views here.
def event_list(request):
    # only show published events that has not passed yet
    events = Event.objects.filter(
        is_published=True,
        date__gte=timezone.now()
    ).order_by('date')

    #filter by category if provided
    category_slug = request.GET.get('category')
    if category_slug:
        events = events.filter(category__slug=category_slug)


    return render(request, 'events/event_list.html', {
        'events': events,
        'catergories' : EventCategory.objects.all(),
        'selected_category': category_slug,
        'is_homepage' : False,
    })

def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug, is_published=True)

    if request.method == 'POST':

        # check if event is full before registering
        if event.is_full:
            messages.error(request, 'Sorry, this event is fully booked.')
            return redirect('event_detail', slug=slug)

        # get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        attendees = int(request.POST.get('attendees', 1))

        # basic validation
        if not name or not email:
            messages.error(request, 'Please fill in your name and email.')
            return redirect('event_detail', slug=slug)

        # check if already registered
        already_registered = EventRegistration.objects.filter(
            event=event,
            email=email
        ).exists()

        if already_registered:
            messages.warning(request, 'You have already registered for this event.')
            return redirect('event_detail', slug=slug)

        # create the registration
        EventRegistration.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone,
            attendees=attendees,
        )

        # send confirmation email
        send_mail(
            subject=f'Registration Confirmed: {event.title}',
            message=(
                f'Hi {name},\n\n'
                f'You have registered for {event.title}.\n\n'
                f'Date: {event.date.strftime("%A, %B %d, %Y at %I:%M %p")}\n'
                f'Location: {event.location}\n\n'
                f'We look forward to seeing you!\n\n'
                f'God bless,\nBethel Baptist Church'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        messages.success(
            request,
            f'You are registered! A confirmation has been sent to {email}.'
        )
        return redirect('event_detail', slug=slug)

    return render(request, 'events/event_detail.html', {
        'event': event,
        'is_homepage' : False,

    })