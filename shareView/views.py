from django.shortcuts import render
from django.shortcuts import get_object_or_404, render, redirect
from django.utils import timezone
from django.views.generic.list import ListView
from .models import Share
from django.http import HttpResponseRedirect, HttpResponse, response


# Create your views here.




class ShareListView(ListView):
    model = Share
    template_name = 'shareView/index.html'

    def get_context_data(self, **kwargs):
        context = super(ShareListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


class SupervisionListView(ListView):
    model = Share
    template_name = 'shareView/supervision.html'

    def get_queryset(self):
        query_set = super(SupervisionListView, self).get_queryset();
        for obj in query_set:
            if obj.supervision_status == False:
                obj.supervision_status = "unchecked"
            else:
                obj.supervision_status = "checked"
        return query_set

    def get_context_data(self, **kwargs):
        context = super(SupervisionListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context


def addShare(request):
    if request.method == 'POST':
        share_code = request.POST['code']
        share_name = request.POST['name']
        price = request.POST['price']
        lot = request.POST['lot']
        stop_price = request.POST['stop_price']
        try:
            share = get_object_or_404(Share, share_code=share_code)
            share.share_name = share_name
            share.share_buy_price = price
            share.share_buy_amount = int(lot) * 100
            share.share_stop_price = stop_price
            share.save()
        except response.Http404:
            Share.objects.create(share_code=share_code, share_name=share_name, double_avg_crossed=False, share_buy_price=price, share_buy_amount=int(lot) * 100, share_stop_price=stop_price)
        return HttpResponseRedirect("/shareView/")
    return HttpResponseRedirect("/shareView/")


def deleteShare(request):
    share_code = request.POST['share_code']
    get_object_or_404(Share, share_code=share_code).delete()
    return HttpResponseRedirect("/shareView/")


def updateSupervision(request):
    if request.method == 'POST':
        code = request.POST['code']
        status = True if request.POST['status'] == 'true' else False
        obj = get_object_or_404(Share, share_code=code)
        obj.supervision_status = status
        obj.save()
    return HttpResponseRedirect("/shareView/supervision/")
