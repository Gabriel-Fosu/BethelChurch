from django.shortcuts import render

# Create your views here.
def gallery(request):
    return render(request, 'gallery/gallery.html', {
        'is_homepage': False
    })

def gallery_category(request, category_slug):
    return render(request, 'gallery/gallery_category.html', {
        'is_homepage': False
    })