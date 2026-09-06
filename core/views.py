from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from .models import PlannedVisit
from django.utils import timezone

# Create your views here.
def home(request):
    return render(request, 'core/home.html', {
        'is_homepage': True,
    })

def about(request):
    return render(request, 'core/about.html', {
        'is_homepage': False,
    })

def contact(request):
    if request.method == 'POST':
        # get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not message:
            messages.error(request, 'Please fill in your name, email and message.')
            return redirect('contact')

        # Route to the right email based on subject
        routing = {
            'Prayer Request': 'pastor@bethelbaptist.gh',
            'Pastoral Care': 'pastor@bethelbaptist.gh',
            'Giving & Finance': 'finance@bethelbaptist.gh',
            'Events & Bookings': 'events@bethelbaptist.gh',
            'Media & Sermons': 'media@bethelbaptist.gh',
        }

        # default goes to general inbox
        recipient = routing.get(subject, 'hello@bethelbaptist.gh')

        send_mail(
            subject= f'[{subject}] from {name}',
            message=(
                f'Name:    {name}\n'
                f'Email:   {email}\n'
                f'Phone:   {phone or "Not provided"}\n'
                f'Subject: {subject}\n\n'
                f'Message:\n{message}'
                f'Reply directly to: {email}'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient],
            fail_silently=True,
        )

        messages.success(
            request,
            f'Thank you {name}! Your message has been sent. We will get back to you soon.'
        )
        return redirect('contact')

    return render(request, 'core/contact.html', {
        'is_homepage': False,
    })

def visit(request):
    if request.method == 'POST':

        # get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        visit_date = request.POST.get('visit_date', '').strip()
        group_size = int(request.POST.get('group_size', 1))
        has_children = request.POST.get('has_children') == 'on'
        how_heard = request.POST.get('how_heard', '').strip()
        questions = request.POST.get('questions', '').strip()

        # basic validation
        if not name or not email or not visit_date:
            messages.error(request, 'Please fill in your name, email, and visit date.')
            return redirect('visit')

        # save to database
        planned_visit = PlannedVisit.objects.create(
            name=name,
            email=email,
            phone=phone,
            visit_date=visit_date,
            group_size=group_size,
            has_children=has_children,
            how_heard=how_heard,
            questions=questions,
        )

        # send welcome email to visitor
        send_mail(
            subject='We are looking forward to meeting you!',
            message=(
                f'Hi {name},\n\n'
                f'Thank you for letting us know you are planning to visit '
                f'Bethel Baptist Church!\n\n'
                f'Here are your visit details:\n'
                f'Date:    {visit_date}\n'
                f'Group:   {group_size} {"person" if group_size == 1 else "people"}\n\n'
                f'What to expect:\n'
                f'— Arrive 10 minutes early so we can welcome you personally\n'
                f'— Parking is available on the church grounds\n'
                f'— Service lasts approximately 90 minutes\n\n'
                f'If you have any questions before Sunday please reply to this email.\n\n'
                f'We cannot wait to meet you!\n\n'
                f'God bless,\n'
                f'The Bethel Baptist Church Team\n'
                f'hello@bethelbaptist.gh · +233 30 000 0000'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=True,
        )

        # notify church team
        send_mail(
            subject=f'New Planned Visit — {name} on {visit_date}',
            message=(
                f'A new visitor has registered to attend.\n\n'
                f'Name:          {name}\n'
                f'Email:         {email}\n'
                f'Phone:         {phone or "Not provided"}\n'
                f'Visit Date:    {visit_date}\n'
                f'Group Size:    {group_size}\n'
                f'Has Children:  {"Yes" if has_children else "No"}\n'
                f'How They Heard: {how_heard or "Not specified"}\n\n'
                f'Questions:\n{questions or "None"}\n\n'
                f'Mark as contacted in the admin panel when followed up.'
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=['hello@bethelbaptist.gh'],
            fail_silently=True,
        )

        messages.success(
            request,
            f'Thank you {name}! We are looking forward to meeting you. '
            f'A confirmation has been sent to {email}.'
        )
        return redirect('visit')

    return render(request, 'core/visit.html', {
        'is_homepage': False,
        'today': timezone.now().date().isoformat(),
    })


def live(request):
    return render(request, 'core/live.html', {
        'is_homepage': False,
    })

def project(request):
    return render(request, 'core/project.html', {
        'is_homepage': False,
    })

def gallery(request):
    return render(request, 'core/gallery.html', {
        'is_homepage': False,
    })

def error_404(request, exception):
    return render(request, 'core/404.html', status=404)

def error_500(request):
    return render(request, 'core/500.html', status=500)