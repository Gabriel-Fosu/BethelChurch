from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Sermon, Speaker, Series

# Create your views here.
def sermon_list(request):
    # Start with all published sermons
    sermons = Sermon.objects.filter(is_published=True)

    # get filter values from url
    search = request.GET.get('q', '')
    speaker_filter = request.GET.get('speaker', '')
    series_filter = request.GET.get('series', '')

    # apply filters if provided
    if search:
        sermons = sermons.filter(title__icontains=search)

    if speaker_filter:
        sermons = sermons.filter(speaker__id=speaker_filter)

    if series_filter:
        sermons = sermons.filter(series__id=series_filter)

    # paginate the results
    paginator = Paginator(sermons, 6)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # send everything to the template
    return render(request, 'sermons/sermon_list.html', {
        'sermons': page_obj,
        'speakers': Speaker.objects.all(),
        'series_list': Series.objects.all(),
        'search': search,
        'speaker_filter': speaker_filter,
        'series_filter': series_filter,
        'page_obj': page_obj,
        'paginator': paginator,
        'page' : page_obj.number,
        'total_pages': paginator.num_pages,
        'page_range': paginator.page_range,
        'total' : paginator.count,
        'is_homepage' : False,
    })

# ── SERMON RESULTS — AJAX ────────────────────────────────────
def sermon_results(request):
    # same filtering logic as above
    # but returns JSON instead of a full HTML page
    sermons = Sermon.objects.filter(is_published=True)

    search         = request.GET.get('q', '')
    speaker_filter = request.GET.get('speaker', '')
    series_filter  = request.GET.get('series', '')

    if search:
        sermons = sermons.filter(title__icontains=search)
    if speaker_filter:
        sermons = sermons.filter(speaker__id=speaker_filter)
    if series_filter:
        sermons = sermons.filter(series__id=series_filter)

    paginator   = Paginator(sermons, 6)
    page_number = request.GET.get('page', 1)
    page_obj    = paginator.get_page(page_number)

    # convert queryset to a list of dictionaries
    # because JsonResponse cannot send model objects directly
    sermons_data = []
    for sermon in page_obj:
        sermons_data.append({
            'title'     : sermon.title,
            'speaker'   : sermon.speaker.name if sermon.speaker else '',
            'date'      : sermon.date.strftime('%B %d, %Y'),
            'series'    : sermon.series.title if sermon.series else '',
            'scripture' : sermon.scripture_reference,
            'slug'      : sermon.slug,
        })

    return JsonResponse({
        'sermons'    : sermons_data,
        'total'      : paginator.count,
        'page'       : page_obj.number,
        'total_pages': paginator.num_pages,
    })


# ── SERMON DETAIL ────────────────────────────────────────────
def sermon_detail(request, slug):
    # get_object_or_404 means:
    # find the sermon with this slug
    # if it does not exist show a 404 page instead of crashing
    sermon = get_object_or_404(Sermon, slug=slug, is_published=True)

    # increment view count every time someone opens the sermon
    Sermon.objects.filter(pk=sermon.pk).update(
        view_count=sermon.view_count + 1
    )

    # find related sermons in the same series
    if sermon.series:
        related = Sermon.objects.filter(
            series=sermon.series,
            is_published=True
        ).exclude(pk=sermon.pk)[:3]
    else:
        related = Sermon.objects.filter(
            is_published=True
        ).exclude(pk=sermon.pk)[:3]

    return render(request, 'sermons/sermon_detail.html', {
        'sermon'          : sermon,
        'related_sermons' : related,
        'is_homepage'     : False,
    })