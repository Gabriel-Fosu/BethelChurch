from django.shortcuts import render
from .models import GalleryCategory, GalleryItem


def gallery(request):
    # get all categories that have at least one item
    categories = GalleryCategory.objects.prefetch_related('items').all()

    # filter by type if selected
    active_type = request.GET.get('type', '')

    # build category data with filtered items
    category_data = []
    for category in categories:
        items = category.items.all()
        if active_type in ['photo', 'video']:
            items = items.filter(type=active_type)
        if items.exists():
            category_data.append({
                'category': category,
                'items'   : items,
            })

    # uncategorised items
    uncategorised = GalleryItem.objects.filter(category=None)
    if active_type in ['photo', 'video']:
        uncategorised = uncategorised.filter(type=active_type)

    return render(request, 'gallery/gallery.html', {
        'is_homepage'   : False,
        'category_data' : category_data,
        'uncategorised' : uncategorised,
        'active_type'   : active_type,
        'all_categories': categories,
    })