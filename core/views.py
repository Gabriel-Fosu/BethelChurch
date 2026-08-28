from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings

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
    return render(request, 'core/visit.html', {
        'is_homepage': False,
    })

def live(request):
    return render(request, 'core/live.html', {
        'is_homepage': False,
    })

# def ministries(request):
#      return render(request, 'core/ministries.html', {
#          'is_homepage': False,
#      })

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