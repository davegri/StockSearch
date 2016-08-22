from django.shortcuts import render
from crawlers.models import Image, Tag
from .models import SearchQuery
import operator
from functools import reduce
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, JsonResponse, HttpResponse
from time import sleep;
import operator
import re
from watson import search as watson
import distance
import pdb
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import redirect

import math
from django.views.decorators.cache import cache_page

@ensure_csrf_cookie
@cache_page(60 * 60)
def home(request):
    per_page = 20
    page_num = 1
    images = Image.active.all().order_by('-id').prefetch_related('tags')[(per_page*page_num)-per_page:per_page*page_num]
    tags = Tag.objects.all().annotate(num_times=Count('image')).order_by('-num_times')[:10]
    origins = Image._meta.get_field('origin').choices
    last_id = Image.active.all().order_by('-id')[0].id
    total_image_count = Image.active.all().count()

    context_dict = {
    'images':images,
    'tags':tags,
    'origins':origins,
    'last_id':last_id,
    'total_image_count': total_image_count
    }

    return render(request, 'home.html', context_dict)


@cache_page(60 * 60 * 12)
def about(request):
    return render(request, 'about.html', {})


@ensure_csrf_cookie
def search(request):
    all_origins = Image._meta.get_field('origin').choices
    all_origins = [origin[0] for origin in all_origins]
    query = request.GET.get('query', False)
    origins_checked = request.GET.getlist('origin') or all_origins
    page = request.GET.get('page', 1)

    # log search in database
    search_query, created = SearchQuery.objects.get_or_create(text=query)
    if not created:
        search_query.amount += 1
        search_query.save(update_fields=['amount',])


    last_id = Image.objects.values('id').latest('id')['id']
    images, amount = get_images_paginated(query, origins_checked, page, last_id)
    pages = int(math.ceil(amount / 20))
    if page >= pages:
        last_page = True
    else:
        last_page = False

    if query.isdigit():
        comparison_image = Image.objects.get(pk=int(query))

    # get any current GET queries without the page modifier
    queries_without_page = request.GET.copy()
    if 'page' in queries_without_page.keys():
        del queries_without_page['page']


    all_origins = Image._meta.get_field('origin').choices
    context_dict = {
                    'results_amount': amount,
                    'query': query,
                    'all_origins': all_origins,
                    'origins_checked': origins_checked,
                    'images': images,
                    'params': queries_without_page,
                    'last_page': last_page,
                    'last_id': last_id
                    }
    return render(request, 'search.html', context_dict)

def duplicates(request):
    duplicate_images = []
    images = Image.objects.distinct('hash')
    for image in images:
        images2 = Image.objects.extra(where=['hamming_text(hash,%s)>0.9'], params=[image.hash]).exclude(pk=image.pk)
        for image2 in images2:
            duplicate_images.append([image, image2])
        if len(duplicate_images) > 200:
            break

    return render(request, 'duplicates.html', {'duplicates':duplicate_images})

    

def get_images_ajax(request):
    if not request.is_ajax():
        return render(request, 'home.html')

    query = request.POST.get('query')
    origins = request.POST.getlist('origin')
    page_num = request.POST.get('page')
    last_id = request.POST.get('last_id', None)

    images, amount = get_images_paginated(query, origins, page_num, last_id)
    pages = int(math.ceil(amount / 20))
    if int(page_num) >= pages:
        last_page = True;
    else:
        last_page = False;
    context = {
        'images':images,
        'last_page':last_page,
    }

    return render(request, '_images.html', context)


def get_images_paginated(query, origins, page_num, last_id=None):
    args = None
    queryset = Image.active.all()
    if last_id is not None:
        queryset = queryset.filter(id__lte=last_id)
    per_page = 20
    page_num = int(page_num)
    if origins and len(origins)<len(Image._meta.get_field('origin').choices):
        origins = [Q(origin=origin) for origin in origins]
        args = reduce(operator.or_, origins)
        queryset = queryset.filter(args)

    if query.isdigit():
        pk = int(query)
        image = Image.objects.get(pk=pk)
        images = queryset.filter(tags__in=image.tags.all()).\
                        annotate(num_common_tags=Count('id')).filter(num_common_tags__gte=2  ).order_by('-num_common_tags')
        # images = queryset.extra(select={'dist':'hamming_text(hash,%s)'}, where=['hamming_text(hash,%s)>0.6'], params=[image.hash,],
        #                              select_params=[image.hash,image.hash]).exclude(hash="").distinct()
    else:
        if query:
            images = watson.filter(queryset, query).distinct()
        else:
            images = watson.filter(queryset, query).order_by('-id').distinct()
    
    amount = images.count()
    images = images.prefetch_related('tags')[(per_page*page_num)-per_page:per_page*page_num]
    return images, amount

@staff_member_required
def hide(request, id):
    image = Image.objects.get(pk=id)
    image.hidden = True
    image.save()
    return redirect('home')

def increment_image_clicks(request):
    if not request.is_ajax():
        return render(request, 'home.html')
    id = request.POST.get('id')
    image = Image.objects.get(id=id)
    image.clicks += 1
    image.save(update_fields=['clicks',])
    return HttpResponse('1')
