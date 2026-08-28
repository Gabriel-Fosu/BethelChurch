from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Ministry, SmallGroup, GroupInterest

# Create your views here.
def ministries_home(request):
    ministries = Ministry.objects.all()

    return render(request, 'ministries/ministries.html', {
        'ministries': ministries,
        'is_homepage': False
    })

def ministry_detail(request, slug):
    ministry = get_object_or_404(Ministry, slug=slug)

    # get all active small groups under this ministry
    groups = SmallGroup.objects.filter(
        ministry=ministry,
        is_active=True
    )

    return render(request, 'ministries/ministry_detail.html', {
        'ministry': ministry,
        'groups': groups,
        'is_homepage': False
    })

def group_list(request, ministry_slug):
    ministry = get_object_or_404(Ministry, slug=ministry_slug)
    groups = get_object_or_404(SmallGroup, ministry=ministry, is_active=True)

    return render(request, 'ministries/group_details.html', {
        'ministry': ministry,
        'groups': groups,
        'is_homepage': False
    })

def group_detail(request, ministry_slug, slug):
    ministry = get_object_or_404(Ministry, slug=ministry_slug)
    group = get_object_or_404(SmallGroup, ministry=ministry, slug=slug)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        if not name or not email:
            messages.error(request, 'Please enter a name and an email.')
            return redirect('group_detail', ministry_slug=ministry_slug, slug=slug)

        # save interest
        GroupInterest.objects.create(
            group=group,
            name=name,
            email=email,
            phone=phone,
        )

        # notify group leader
        if group.leader and group.leader.email:
            send_mail(
                subject=f'New Interest in {group.name}',
                message=(
                    f'{name} is interested in joining your group.\n\n'
                    f'Email: {email}\n'
                    f'Phone: {phone or "Not provided"}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[group.leader.email],
                fail_silently=True,
            )
        messages.success(
            request,
            f'Thank you {name}! The group leader will contact you soon.'
        )
        return redirect('group_detail', ministry_slug=ministry_slug, slug=slug)

    return render(request, 'ministries/group_detail.html', {
        'ministry': ministry,
        'group': group,
        'is_homepage': False
    })