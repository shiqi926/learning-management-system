from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from rest_framework.response import Response

def get_by_pk(model_class, id, serializer, req):
    try:
        obj = model_class.objects.get(pk=id)
    except model_class.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serialized = serializer(obj, context={'request': req})
    return Response(serialized.data)

def get_all_paginated(model_class, page_limit, url, serializer, req):
    data = []
    nextPage = 1
    previousPage = 1
    objs = model_class.objects.all().order_by('id')
    page = req.GET.get('page', 1)
    paginator = Paginator(objs, page_limit)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        data = paginator.page(1)
    except EmptyPage:
        data = paginator.page(paginator.num_pages)

    serialized = serializer(data,context={'request': req} ,many=True)
    if data.has_next():
        nextPage = data.next_page_number()
    if data.has_previous():
        previousPage = data.previous_page_number()
    return Response({'data': serialized.data , 'count': paginator.count, 'numpages' : paginator.num_pages, 'nextlink': url + str(nextPage), 'prevlink': url + str(previousPage)})