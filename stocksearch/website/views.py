from django.shortcuts import render
from crawlers.models import Image, Tag
import operator
from functools import reduce
from django.db.models import Q
from django.db.models import Count
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.http import Http404, JsonResponse
from time import sleep;
import operator
import re
import watson
import distance
import pdb
from django.views.decorators.csrf import ensure_csrf_cookie
import math

@ensure_csrf_cookie
def home(request):
    per_page = 20
    page_num = 1
    images = Image.objects.all().exclude(tags__isnull=True).order_by('-id').prefetch_related('tags')[(per_page*page_num)-per_page:per_page*page_num]
    tags = Tag.objects.all().annotate(num_times=Count('image')).order_by('-num_times')[:10]
    origins = Image._meta.get_field('origin').choices
    context_dict = {'images':images,'tags':tags,'origins':origins}
    return render(request, 'home.html', context_dict)


@ensure_csrf_cookie
def search(request):
    all_origins = Image._meta.get_field('origin').choices
    all_origins = [origin[0] for origin in all_origins]
    query = request.GET.get('query', False)
    origins_checked = request.GET.getlist('origin') or all_origins
    page = request.GET.get('page', 1)

    images, amount = get_images_paginated(query, origins_checked, page)

    pages = int(math.ceil(amount / 20))
    if page >= pages:
        last_page = True;
    else:
        last_page = False;

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
                    'last_page': last_page
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

    images, amount = get_images_paginated(query, origins, page_num)
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


def get_images_paginated(query, origins, page_num):
    args = None
    queryset = Image.objects.all().exclude(tags__isnull=True)
    per_page = 20
    page_num = int(page_num)
    if origins:
        origins = [Q(origin=origin) for origin in origins]
        args = reduce(operator.or_, origins)
        queryset = Image.objects.filter(args)        

    if query.isdigit():
        pk = int(query)
        image = Image.objects.get(pk=pk)
        images = Image.objects.extra(select={'dist':'hamming_text(hash,%s)'},
                                     select_params=[image.hash]).exclude(pk=pk).order_by('-dist')[(per_page*page_num)-per_page:per_page*page_num]
        amount = len(images)
        return images, amount

    if query:
        images = watson.filter(queryset, query)
    else:
        images = watson.filter(queryset, query).order_by('-id')
    amount = images.count()
    images = images.prefetch_related('tags')[(per_page*page_num)-per_page:per_page*page_num]

    return images, amount

