import decimal
import copy
import os
import base64
from io import BytesIO

from django.shortcuts import render, redirect, reverse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import Http404, FileResponse, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.http import Http404, FileResponse, HttpResponse, HttpResponseForbidden, HttpResponseNotFound
from django.core.paginator import Paginator
from django.db.models import Sum, Min
from datetime import datetime, timedelta
from dal import autocomplete
from .models import Request
from .models import Goods
from .models import Bid
from .models import House
from .models import Content
from .models import Supplier
from .models import Archive
from .models import ArchiveDetail
from .models import Object
from .models import Estimate
from .models import Phase
from .models import Delivery
from .models import Prepayment
from .models import Sample
from .models import SampleDetail
from .models import Order
from .models import OrderDetail
from .models import Earning
from .models import Account
from .models import CashRegister
from .models import SubCash
from .models import Contract
from .models import Turnover
from .models import User
from .models import Setting
from .models import ContractImage
from .forms import RequestForm
from .forms import DetailsForm
from .forms import BidForm
from .forms import BidEditForm
from .forms import ContentsForm
from .forms import ArchEditForm
from .forms import ArchiveDetailForm
from .forms import ReportForm
from .forms import BidsForm
from .forms import HouseDetailModelForm
from .forms import BidsSearchForm
from .forms import SearchForm
from .forms import PrepaymentForm
from .forms import ConcreteDeliveryForm
from .forms import TForm
from .forms import HouseForm
from .forms import HouseModelForm
from .forms import SupplierModelForm
from .forms import ObjectModelForm
from .forms import ConcreteForm
from .forms import SupplierReportForm
from .forms import SampleDetailForm
from .forms import SampleForm
from .forms import OrderForm
from .forms import OnApprovalForm
from .forms import OrderDetailModelForm
from .forms import EstimateModelForm
from .forms import PhaseModelForm
from .forms import OrdersForm
from .forms import ResolveForm
from .forms import OrderDetailForm
from .forms import ProcessingForm
from .forms import ReceivingForm
from .forms import ClosingForm
from .forms import SuppliersForm
from .forms import EstimatesForm
from .forms import PhasesForm
from .forms import SupplierRemoveModelForm
from .forms import ExportForm
from .forms import BalanceForm
from .forms import SubCashesForm
from .forms import SubCashForm
from .forms import SubCashFormEdit
from .forms import ExpenseContentFormEdit
from .forms import AccountsForm
from .forms import AccountForm
from .forms import AccountFormEdit
from .forms import EarningForm
from .forms import ContractsForm
from .forms import ContractForm
from .forms import TurnoverForm
from .forms import TurnoverPerformedForm
from .forms import ContractEditForm
from .forms import ContractsExportForm
from .forms import TurnoverCommentOnlyForm
from .forms import ContractChangeForm
from .forms import ContractReceiptForm
from .forms import ImageUploadForm
from .forms import ContractCommentForm

import datetime
from datetime import datetime as mydatetime
from .forms import BookModelForm
from bootstrap_modal_forms.generic import BSModalCreateView
from bootstrap_modal_forms.generic import BSModalUpdateView
from bootstrap_modal_forms.generic import BSModalFormView
from django.urls import reverse_lazy
import xlsxwriter
import io
from django.db.models import F
from django.db.models import Q
from django.db.models import Count
from django.db.models.functions import Cast
from django.db.models import Max
from django.db.models import BooleanField, CharField, Value
from django.db import transaction
from django.db.models import Subquery

import time
from PIL import Image as PImage


class GoodsAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated():
            return Goods.objects.none()

        qs = Goods.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class HousesAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if self.request.user.is_authenticated():
            return House.objects.none()

        qs = House.objects.all()

        if self.q:
            qs = qs.filter(object_id=self.q)

        return qs


class SuppliersAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):

        if not self.request.user.is_authenticated:
            return Supplier.objects.none()

        qs = Supplier.objects.filter(hidden=False)

        if self.q:
            qs = qs.filter(name__icontains=self.q)

        return qs


@login_required
def requests(request):
    page_number = request.GET.get('page')
    myrequests = Request.objects.filter(owner=request.user).order_by('-id')
    paginator = Paginator(myrequests, 10)
    # page_obj = paginator.get_page(page_number)

    try:
        page_ = paginator.page(page_number)
    except:
        page_ = paginator.page(1)
        page_number = 1

    return render(request, 'project/index.html',
                  {'title': 'Requests page', 'myrequests': page_.object_list, 'page': page_number, 'pages': paginator,
                   'page_': page_})


@login_required
def one_request(request, request_id):
    request_ = Request.objects.get(id=request_id)
    if request_.owner != request.user:
        raise Http404
    details_ = request_.details_set.order_by('-id')
    return render(request, 'project/onerequest.html',
                  {'title': 'One request page', 'request_': request_, 'details_': details_})


@login_required
def details_add(request, request_id):
    error = ''
    request_ = Request.objects.get(id=request_id)
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            new_goods_ = form.save(commit=False)
            new_goods_.request = request_
            # new_goods_.goods = request.user
            new_goods_.save()
            return HttpResponseRedirect(reverse('project:onerequest', args=[request_.id]))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/addetails.html', context)
    form = DetailsForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'project/addetails.html', context)


@login_required
def new_request(request):
    error = ''
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            new_request_ = form.save(commit=False)
            now = datetime.datetime.now()
            new_request_.date = now
            new_request_.status = 'c'
            new_request_.owner = request.user
            new_request_.save()
            return redirect('project:requests')
        else:
            error = 'Неверные данные формы'
    form = RequestForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'project/addrequest.html', context)


@login_required
def bids(request):
    page_number = request.GET.get('page')
    is_manager = request.user.groups.filter(name='managers').exists()
    if is_manager:
        mybids = Bid.objects.filter(deleted=False).order_by('id')
    else:
        mybids = Bid.objects.filter(owner=request.user, deleted=False).order_by('id')
    paginator = Paginator(mybids, 10)
    # page_obj = paginator.get_page(page_number)

    try:
        page_ = paginator.page(page_number)
    except:
        page_ = paginator.page(1)
        page_number = 1

    return render(request, 'project/bids.html',
                  {'title': 'Заявки', 'mybids': page_.object_list, 'page': page_number, 'pages': paginator,
                   'page_': page_})


@login_required
def fill_signed_bids_(request):
    bids = Bid.objects.filter(deleted=False, locked=True)
    with transaction.atomic():
        for item in bids:
            wcnt = item.content_set.filter(deleted=False, type='b').count()
            tcnt = item.content_set.filter(deleted=False, type='c').count()
            if wcnt == 0 and tcnt > 0:
                Bid.objects.filter(id=item.id).update(highlighted=True, supervision=True, supervisor='-')

    return render(request, 'project/fastbids.html', {'title': 'выполнено'})


@login_required
def fill_delivered_bids_(request):
    bids = Bid.objects.filter(deleted=False, locked=True)
    with transaction.atomic():
        for item in bids:
            materials = item.content_set.filter(deleted=False, type='a').count()
            #tcnt = item.content_set.filter(deleted=False, type='c').count()
            if materials > 0:
                Bid.objects.filter(id=item.id).update(highlighted=False, supervision=True, supervisor='+')

    return render(request, 'project/fastbids.html', {'title': 'выполнено'})


@login_required
def transfer_object(request):
    object_ = Object.objects.get(id=37)
    #print(object_)

    objects2 = Object.objects.all().using('extended')
    #print(objects2)

    newobject = Object(name=object_.name)
    newobject.save(using='extended')
    #print(newobject)

    house_id = {}
    houses = object_.house_set.all()
    for house in houses:
        newhouse = House(name=house.name, object=newobject)
        newhouse.save(using='extended')
        house_id[house.id] = newhouse.id

    if True:
        oldbids = Bid.objects.filter(deleted=False, object=object_)
        for bid in oldbids:
            #user = User.objects.filter
            newbid = Bid(title=bid.title, date=bid.date, object=newobject, owner_id=bid.owner.id, locked=bid.locked,
                         deleted=bid.deleted, number=bid.number, highlighted=bid.highlighted,
                         supervision=bid.supervision, supervisor=bid.supervisor)
            newbid.save(using='extended')
            oldcontent = bid.content_set.filter(deleted=False)
            for c in oldcontent:
                newcontent = Content(title=c.title, date=c.date, type=c.type, cash=c.cash, quantity=c.quantity,
                                     measure=c.measure, price=c.price, comment=c.comment, bid=newbid,
                                     house_id=house_id[c.house.id], deleted=c.deleted, supplier_id=c.supplier.id,
                                     phase_id=c.phase.id, estimate_id=c.estimate.id, history=c.history, subcash=c.subcash,
                                     credit_account=c.credit_account, expense_account=c.expense_account,
                                     prepaid=c.prepaid)
                newcontent.save(using='extended')
            bid.deleted = True
            bid.save()

        olddelivery = Delivery.objects.filter(deleted=False, object=object_)
        for d in olddelivery:
            newdelivery = Delivery(comment=d.comment, date=d.date, volume=d.volume, price=d.price, pumpcomment=d.pumpcomment,
                                   pumpsummary=d.pumpsummary, deliveryvolume=d.deliveryvolume, deliveryprice=d.deliveryprice,
                                   concrete_grade=d.concrete_grade, pile=d.pile, deleted=d.deleted, house_id=house_id[d.house.id],
                                   object=newobject, owner_id=d.owner.id, supplier_id=d.supplier.id, verified=d.verified, history=d.history)
            newdelivery.save(using='extended')
            d.deleted = True
            d.save()



    #oldbids = Bid.objects.filter(deleted=False)
    #for bid in oldbids:


    return render(request, 'project/fastbids.html', {'title': 'выполнено'})


@login_required
def fill_performed_turnovers_(request):
    turnovers = Turnover.objects.filter(deleted=False, performed=True)
    with transaction.atomic():
        for item in turnovers:
           Turnover.objects.filter(id=item.id).update(actualdate=item.date)

    return render(request, 'project/fastbids.html', {'title': 'выполнено'})


@login_required
def fill_completed_contracts_(request):
    contracts = Contract.objects.filter(deleted=False, status='d')
    with transaction.atomic():
        for item in contracts:
           Contract.objects.filter(id=item.id).update(receipt=True, onhand=True)

    return render(request, 'project/fastbids.html', {'title': 'выполнено'})

@login_required
def filtered_bids_(request):
    start = time.time()
    mybids = Bid.objects.filter(deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
    #print('Time -: ', time.time() - start)

    start = time.time()
    #for item in mybids:
    #    summary = item.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(
    #        summary=Sum('total_price'))

    #ss = Bid.objects.filter(id__in=Subquery)

    select = Content.objects.values('bid_id').annotate(total_price=F('quantity') * F('price')).filter(deleted=False, total_price=400000)
    ss = Bid.objects.filter(id__in=Subquery(select.values('bid_id')))

    #sel = Bid.objects.filter(deleted=False).annotate(total_price=F('quantity') * F('price')) #content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price'))

#    sss = Content.objects.values('bid_id').filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    sss = Content.objects.values('bid_id').filter(deleted=False, bid__deleted=False).annotate(summary=Sum(F('quantity') * F('price')))


    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()

    mybids = Bid.objects.filter(deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

    row = 1
    for item in mybids:
        #row += 1
        content = item.content_set.filter(deleted=False)
        for cnt in content:
            worksheet.write(row, 0, item.number)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")))
            worksheet.write(row, 2, item.title)
            worksheet.write(row, 3, item.object.name)
            worksheet.write(row, 4, item.owner.username)

            worksheet.write(row, 5, cnt.house.name)
            worksheet.write(row, 6, cnt.title)
            worksheet.write(row, 7, cnt.get_type_display())
            worksheet.write(row, 8, cnt.get_cash_display())
            worksheet.write(row, 9, cnt.quantity)
            worksheet.write(row, 10, cnt.price)
            worksheet.write(row, 11, cnt.get_measure_display())
            worksheet.write(row, 12, cnt.supplier.name)
            worksheet.write(row, 13, cnt.phase.name)
            worksheet.write(row, 14, cnt.estimate.name)
            worksheet.write(row, 15, cnt.comment)
            row += 1

    workbook.close()
    buffer.seek(0)
    filename = 'report23.xlsx'
    response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

    #print('Time --: ', time.time() - start)

    #print(sss)

    #for item in ss:
    #    print(item)

    #return render(request, 'project/fastbids.html')

@login_required
def filtered_bids(request):
    is_special = request.user.groups.filter(name='special').exists()
    is_seller = request.user.groups.filter(name='sellers').exists()
    is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    sellergroup = request.user.groups.filter(name__contains='sellersgroup').exists()
    #print(sellergroup)
    #only = request.user.groups.count()
    if (is_seller and sellergroup) or is_headofsales:
        return HttpResponseRedirect(reverse('project:contracts'))
    rollback = '&'.join(request.GET.urlencode().split('&')[1:])
    if rollback: rollback = '&' + rollback
    #start = time.time()
    filtered_object = 0
    filtered_sum = 0.0
    author = 0
    choice_filter = '0'
    unlocked_only = False
    undelivered_only = False
    page_number = request.GET.get('page')
    #number =
    #object_id = 0
    is_manager = request.user.groups.filter(name='managers').exists()
    user = request.user
    #print(user)

    if request.method == 'POST':
        form = BidsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #print(cd['testdate'])
            filter_object = cd['filter_object']
            filtered_sum = cd['summary']
            out_str = '?page=1'
            if filter_object is None:
                filtered_object = 0
                out_str += '&f=0'
                #return HttpResponseRedirect(reverse('project:bids')+'?page=1' + '&f=' + str(filtered_object))
            else:
                filtered_object = filter_object.id
                out_str += '&f=' + str(filtered_object)
                #return HttpResponseRedirect(reverse('project:bids') + '?page=1' + '&f=' + str(filtered_object))
            summary = 0
            try:
                summary = float(filtered_sum)
                out_str += '&s=' + str(summary)
            except:
                pass
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)
            author = cd['author']
            if author:
                out_str += '&a=' + str(author.id)
            choice_filter = cd['choice_filter']
            if choice_filter:
                out_str += '&c=' + str(choice_filter)
            return HttpResponseRedirect(reverse('project:bids') + out_str)
    else:
        if 'f' in request.GET:
            filtered_object_str = request.GET.get('f', 0)
            try:
                filtered_object = int(filtered_object_str)
            except:
                filtered_object = 0

            if is_manager:
                if filtered_object == 0:
                    #mybids = Bid.objects.filter(deleted=False).order_by('-number')
                    #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False ORDER BY n DESC")
                    mybids = Bid.objects.filter(deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
                else:
                    #mybids = Bid.objects.filter(deleted=False, object__id=filtered_object).order_by('-number', '-id')
                    #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False AND object_id=%s ORDER BY n DESC", [filtered_object,])
                    mybids = Bid.objects.filter(deleted=False, object__id=filtered_object).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
            else:
                if filtered_object == 0:
                    #mybids = Bid.objects.filter(owner=request.user, deleted=False).order_by('-number', '-id')
                    #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False AND owner_id=%s ORDER BY n DESC", [request.user.id,])
                    mybids = Bid.objects.filter(owner=request.user, deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
                else:
                    #mybids = Bid.objects.filter(owner=request.user, deleted=False, object__id=filtered_object).order_by('-number', '-id')
                    #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False AND object_id=%s AND owner_id=%s ORDER BY n DESC",[filtered_object, request.user.id,])
                    mybids = Bid.objects.filter(owner=request.user, deleted=False, object__id=filtered_object).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

        else:
            if is_manager:
                #mybids = Bid.objects.filter(deleted=False).order_by('-number', '-id')
                #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False ORDER BY n DESC")
                start = time.time()
                mybids = Bid.objects.filter(deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
                #print('Time 0: ', time.time() - start)
            else:
                #mybids = Bid.objects.filter(owner=request.user, deleted=False).order_by('-number', '-id')
                #mybids = Bid.objects.raw("SELECT *, '0'+CAST(number as text) as n FROM project_bid WHERE deleted=False AND owner_id=%s ORDER BY n DESC",[request.user.id,])
                mybids = Bid.objects.filter(owner=request.user, deleted=False).extra({'n': "10000+CAST(number as TEXT)"}).order_by( '-n')

        if 's' in request.GET:
            filtered_sum_str = request.GET.get('s', 0.0)
            try:
                filtered_sum = float(filtered_sum_str)
            except:
                filtered_sum = 0.0
            if filtered_sum > 0:
                #select = Content.objects.values('bid_id').annotate(total_price=F('quantity') * F('price')).filter(deleted=False, total_price=filtered_sum)
                sss = Content.objects.values('bid_id').filter(deleted=False, bid__deleted=False).annotate(summary=Sum(F('quantity') * F('price'))).filter(deleted=False, summary=filtered_sum)
                mybids = mybids.filter(deleted=False, id__in=Subquery(sss.values('bid_id')))

        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = None
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = None

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = None
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
        else:
            date_to = None

        if date_from:
            mybids = mybids.filter(date__gte=date_from) #
        if date_to:
            date_to_delta = date_to + datetime.timedelta(days=1)
            mybids = mybids.filter(date__lt=date_to_delta) #
        #print(mybids)
        if 'a' in request.GET:
            filtered_user_str = request.GET.get('a', 0)
            try:
                author = int(filtered_user_str)
            except:
                author = 0
        if author > 0:
            mybids = mybids.filter(owner_id=author)

        if 'c' in request.GET:
            choice_filter_str = request.GET.get('c', '0')
            try:
                choice_filter = choice_filter_str
            except:
                choice_filter = '0'
        if choice_filter == '1': # Оплаченные и доставленные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a',
                                              bid__supervision=True).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            countain = countain.filter(Q(bid__locked=True) & Q(prepaid=False))
            cu = countain.values('bid_id')
            mybids = mybids.filter(id__in=cu).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

        elif choice_filter == '2': # Доставленные но неоплаченные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a',
                                              bid__supervision=True).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            countain = countain.filter(Q(bid__locked=False) & Q(prepaid=True))
            cu = countain.values('bid_id')
            mybids = mybids.filter(id__in=cu).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

        elif choice_filter == '3':  # Оплаченные и недоставленные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a',
                                              bid__supervision=False).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            countain = countain.filter(Q(bid__locked=True) & Q(prepaid=False))
            cu = countain.values('bid_id')
            mybids = mybids.filter(id__in=cu).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
        elif choice_filter == '4': # Не доставленные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a',
                                              bid__supervision=False).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            countain = countain.filter(Q(bid__locked=True) | (Q(bid__locked=False) & Q(prepaid=True)))
            cu = countain.values('bid_id')
            mybids = mybids.filter(id__in=cu).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

        elif choice_filter == '5':  # Доставленные и оплаченные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a',
                                              bid__supervision=True).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            countain = countain.filter(Q(bid__locked=True) & Q(prepaid=True))
            cu = countain.values('bid_id')
            mybids = mybids.filter(id__in=cu).extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
        elif choice_filter == '6': # Не оплаченные
            countain = Content.objects.filter(deleted=False, bid__deleted=False, type='a', prepaid=True,
                                              bid__supervision=False).values("bid_id").annotate(
                total=Count("bid_id")).order_by("-bid_id")
            cu = countain.values('bid_id')
            mybids = mybids.filter(deleted=False, locked=False)
            mybids = mybids.exclude(id__in=cu)
        elif choice_filter == '7': # Возвращённые
            mybids = mybids.filter(deleted=False, refunded=True)

        if not is_special:
            mybids = mybids.exclude(hidden=True)

        paginator = Paginator(mybids, 10)
        # page_obj = paginator.get_page(page_number)

        try:
            page_ = paginator.page(page_number)
        except:
            page_ = paginator.page(1)
            page_number = 1

    #page_ = 1
    form = BidsForm(initial={'filter_object': filtered_object, 'summary': str(filtered_sum),
                             'datefrom': date_from, 'dateto': date_to, 'author': author, 'choice_filter': choice_filter})

    #stop = time.time()
    #print('Time: ', stop - start)

    mybids_page = []
    # print(unlocked_only)
    #start = time.time()
    for item in page_.object_list:
        summary = item.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
        workcount = item.content_set.filter(deleted=False, type='b').count()
        techcount = item.content_set.filter(deleted=False, type='c').count()
        materials = item.content_set.filter(deleted=False, type='a').count()
        not_prepaid = item.content_set.filter(deleted=False, type='a', prepaid=True).count()
        try:
            item.summary = float(summary['summary'])
            item.workcount = workcount
            item.techcount = techcount
            item.materials = materials
            item.not_prepaid = not_prepaid
            #print(workcount)
        except:
            item.summary = 0
            item.workcount = 0
            item.techcount = 0
            item.materials = 0
            item.not_prepaid = 0
        mybids_page.append(item)

        # print(item)
        """
        if filtered_sum == 0.0:
            if unlocked_only:
                if not item.locked:
                    mybids_page.append(item)
            else:
                mybids_page.append(item)
        else:
            if item.summary == filtered_sum:
                if unlocked_only:
                    if not item.locked:
                        mybids_page.append(item)
                else:
                    mybids_page.append(item)
        """

    #return render(request, 'project/filtered.html', {'form': form, 'title': 'Отчёт'})

    #start = time.time()

    #print(page_.object_list)

    render_ = render(request, 'project/filtered.html',
                  {'form': form, 'title': 'Заявки', 'mybids': mybids_page, 'page': page_number, 'pages': paginator, #page_.object_list
                   'page_': page_, 'object': filtered_object, 'summary': str(filtered_sum), 'choice_filter': choice_filter, 'rollback': rollback})
    #stop = time.time()
    #print('Time: ', stop - start)

    return render_


@login_required
def filtered_contracts(request):
    rollback = '&'.join(request.GET.urlencode().split('&')[1:])
    if rollback: rollback = '&' + rollback
    #start = time.time()
    filtered_object = 0
    filtered_house = 0
    author = 0
    choice_filter = '0'
    contract_type = '0'
    contract_number = ''
    client_name = ''
    receipt = '0'
    onhand = '0'
    datenow = datetime.datetime.now()
    page_number = request.GET.get('page')
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    sellergroup = request.user.groups.filter(name__contains='sellersgroup')
    if sellergroup:
        sellergroup = sellergroup[0].name

    user = request.user

    if request.method == 'POST':
        form = ContractsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            filter_object = cd['object']
            out_str = '?page=1'
            if filter_object is None:
                filtered_object = 0
                out_str += '&f=0'
            else:
                filtered_object = filter_object.id
                out_str += '&f=' + str(filtered_object)
            filter_house = cd['house']
            if filter_house is None:
                filtered_house = 0
                out_str += '&h=0'
            else:
                filtered_house = filter_house.id
                out_str += '&h=' + str(filtered_house)
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)
            author = cd['author']
            if author:
                out_str += '&a=' + str(author.id)
            choice_filter = cd['choice_filter']
            if choice_filter:
                out_str += '&c=' + str(choice_filter)
            contract_type = cd['contract_type']
            if contract_type:
                out_str += '&t=' + str(contract_type)
            receipt = cd['receipt']
            if receipt:
                out_str += '&r=' + str(receipt)
            onhand = cd['onhand']
            if onhand:
                out_str += '&on=' + str(onhand)
            contract_number = cd['number']
            if contract_number:
                out_str += '&n=' + str(contract_number)
            client_name = cd['client']
            if client_name:
                out_str += '&b=' + str(client_name)
            return HttpResponseRedirect(reverse('project:contracts') + out_str)
    else:

        mycontracts = Contract.objects.filter(deleted=False).order_by('-id')

        if 'f' in request.GET:
            filtered_object_str = request.GET.get('f', 0)
            try:
                filtered_object = int(filtered_object_str)
            except:
                filtered_object = 0

            if filtered_object != 0:
                mycontracts = mycontracts.filter(deleted=False, object__id=filtered_object).order_by('-id')

        if 'h' in request.GET:
            filtered_house_str = request.GET.get('h', 0)
            try:
                filtered_house = int(filtered_house_str)
            except:
                filtered_house = 0

            if filtered_house != 0:
                mycontracts = mycontracts.filter(house__id=filtered_house)

        contracts_in_archive = get_settings('contracts_in_archive', 3)
        if is_headofsales:
            sellers = User.objects.filter(groups__name=sellergroup).values('id')
            if contracts_in_archive:
                mycontracts = mycontracts.filter(~Q(status='d'), revoked=False, owner__id__in=sellers).order_by('-id')
            else:
                mycontracts = mycontracts.filter(owner__id__in=sellers).order_by('-id')
        elif is_accountant or is_boss:
            pass
        else:
            if contracts_in_archive:
                mycontracts = mycontracts.filter(~Q(status='d'), revoked=False, owner=request.user).order_by('-id')
            else:
                mycontracts = mycontracts.filter(owner=request.user).order_by('-id')

        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = None
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = None

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = None
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
        else:
            date_to = None

        if date_from:
            mycontracts = mycontracts.filter(date__gte=date_from) #
        if date_to:
            date_to_delta = date_to + datetime.timedelta(days=1)
            mycontracts = mycontracts.filter(date__lt=date_to_delta) #
        #print(mybids)
        if 'a' in request.GET:
            filtered_user_str = request.GET.get('a', 0)
            try:
                author = int(filtered_user_str)
            except:
                author = 0
        if author > 0:
            mycontracts = mycontracts.filter(owner_id=author)
        if 'c' in request.GET:
            choice_filter_str = request.GET.get('c', '0')
            try:
                choice_filter = choice_filter_str
            except:
                choice_filter = '0'
        if choice_filter != '0':
            if choice_filter == 'e':
                contracts = mycontracts.values('id')
                filteredcontracts = Turnover.objects.filter(deleted=False, performed=False, contract__id__in=contracts, type__lt=100).values('contract__id').annotate(min=Min('date'))
                selected = filteredcontracts.filter(min__lt=datenow).values('contract__id')
                mycontracts = mycontracts.filter(~Q(status='a'), id__in=selected)
            else:
                if choice_filter == 'f':
                    contracts = mycontracts.values('id')
                    mycontracts = mycontracts.filter(~Q(reservation_type='a'), id__in=contracts)
                else:
                    if choice_filter == 'g':
                        contracts = mycontracts.values('id')
                        dateminus14days = datenow - datetime.timedelta(days=14)
                        mycontracts = mycontracts.filter(~Q(reservation_type='a'), reservation_date__lt=dateminus14days, id__in=contracts)
                    else:
                        if choice_filter == 'h':
                            contracts = mycontracts.values('id')
                            mycontracts = mycontracts.filter(revoked=True, id__in=contracts)
                        else:
                            mycontracts = mycontracts.filter(status=choice_filter)

        if 't' in request.GET:
            contract_type = request.GET.get('t', '0')
        if contract_type != '0':
            mycontracts = mycontracts.filter(type=contract_type)

        if 'r' in request.GET:
            receipt = request.GET.get('r', '0')
        if receipt != '0':
            if receipt == 'a':
                mycontracts = mycontracts.filter(receipt=True)
            else:
                mycontracts = mycontracts.filter(receipt=False)

        if 'on' in request.GET:
            onhand = request.GET.get('on', '0')
        if onhand != '0':
            if onhand == 'a':
                mycontracts = mycontracts.filter(onhand=True)
            else:
                mycontracts = mycontracts.filter(onhand=False)

        if 'n' in request.GET:
            contract_number = request.GET.get('n', '')
        if contract_number:
            mycontracts = mycontracts.filter(number__contains=contract_number)

        if 'b' in request.GET:
            client_name = request.GET.get('b', '')
        if client_name:
            mycontracts = mycontracts.filter(client__contains=client_name)

        totalsquare = mycontracts.filter(deleted=False, revoked=False).aggregate(summary=Sum('square'))
        if totalsquare['summary']:
            totalsquare = round(totalsquare['summary'], 2)
        else:
            totalsquare = 0.00

        totalplannedamount = mycontracts.filter(deleted=False, revoked=False).annotate(total_amount=F('price') - F('agency_discount') - F('developer_discount')).aggregate(summary=Sum('total_amount'))
        if totalplannedamount['summary']:
            totalplannedamount = round(totalplannedamount['summary'], 2)
        else:
            totalplannedamount = 0.00

        mycontracts2 = mycontracts.filter(revoked=False)
        contracts = mycontracts2.values('id')
        totalreceivedamount = Turnover.objects.filter(deleted=False, performed=True, contract__id__in=contracts, type__lt=100).aggregate(summary=Sum('amount'))
        if totalreceivedamount['summary']:
            totalreceivedamount = round(totalreceivedamount['summary'], 2)
        else:
            totalreceivedamount = 0.00

        totalplannedcommission = mycontracts.filter(deleted=False, revoked=False).annotate(total_amount=F('seller_commission') + F('agency_commission')).aggregate(summary=Sum('total_amount'))
        if totalplannedcommission['summary']:
            totalplannedcommission = round(totalplannedcommission['summary'], 2)
        else:
            totalplannedcommission = 0.00
        totalreceivedcommission = Turnover.objects.filter(deleted=False, performed=True, contract__id__in=contracts, type__gte=100).aggregate(summary=Sum('amount'))
        if totalreceivedcommission['summary']:
            totalreceivedcommission = round(totalreceivedcommission['summary'], 2)
        else:
            totalreceivedcommission = 0.00

        totalebt = Turnover.objects.filter(deleted=False, performed=False, contract__id__in=contracts, type__lt=100, date__lte=datenow, contract__status__gt='a').aggregate(summary=Sum('amount'))
        if totalebt['summary']:
            totalebt = round(totalebt['summary'], 2)
        else:
            totalebt = 0.00


        paginator = Paginator(mycontracts, 10)
        # page_obj = paginator.get_page(page_number)

        try:
            page_ = paginator.page(page_number)
        except:
            page_ = paginator.page(1)
            page_number = 1

        for item in page_.object_list:
            unperformed = item.turnover_set.filter(deleted=False, performed=False).count()
            income = item.turnover_set.filter(deleted=False, performed=True, type__lt=100).aggregate(summary=Sum('amount'))['summary']
            paid = item.turnover_set.filter(deleted=False, performed=True, type__gte=100).aggregate(summary=Sum('amount'))['summary']
            withimages = item.contractimage_set.filter(deleted=False).count()
            item.withimages = withimages

            min_date = item.turnover_set.filter(deleted=False, performed=False, type__lt=100).aggregate(min=Min('date'))['min']
            #print(min_date)
            if min_date and min_date < datenow and item.status != 'a':
                item.alarm = True
            else:
                item.alarm = False

            item.unperformed = unperformed
            if income:
                item.income = round(income, 2)
            else:
                item.income = 0.0
            if paid:
                item.paid = round(paid, 2)
            else:
                item.paid = 0.0
            income_equal = (float(item.price - item.agency_discount - item.developer_discount) - float(item.income)) == 0
            paid_equal = (float(item.agency_commission + item.seller_commission) - float(item.paid)) == 0
            item.income_equal = income_equal
            item.paid_equal = paid_equal
            #print(item.income, item.paid)

    form = ContractsForm(initial={'object': filtered_object, 'house': filtered_house, 'datefrom': date_from, 'dateto': date_to,
                                  'author': author, 'choice_filter': choice_filter, 'contract_type': contract_type,
                                  'client': client_name, 'number': contract_number, 'receipt': receipt, 'onhand': onhand})

    mycontracts_page = []
    render_ = render(request, 'project/contracts.html',
                  {'form': form, 'title': 'Контракты', 'mycontracts': page_, 'page': page_number, 'pages': paginator,
                   'page_': page_, 'object': filtered_object, 'rollback': rollback, 'totalsquare': totalsquare,
                   'totalplannedamount': totalplannedamount, 'totalreceivedamount': totalreceivedamount,
                   'totalplannedcommission': totalplannedcommission, 'totalreceivedcommission': totalreceivedcommission,
                   'datenow': datenow, 'totalebt': totalebt})
    #stop = time.time()
    #print('Time: ', stop - start)

    return render_

@login_required
def one_bid(request, bid_id):
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    extended = request.GET.get('x')
    selected_supplier = request.GET.get('supplier')
    selected_house = request.GET.get('h', None)
    if selected_house or selected_supplier:
        if selected_house:
            rollback = request.GET.urlencode() + '#panelsStayOpen-heading-' + selected_house
        elif selected_supplier:
            rollback = request.GET.urlencode()
    else:
        #rollback = ''
        rollback = request.GET.urlencode()
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    undelivered_only = request.GET.get('u')
    bid_ = Bid.objects.get(id=bid_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    if bid_.owner != request.user and not is_manager:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    contents_ = bid_.content_set.filter(deleted=False).order_by('type')
    summary_ = bid_.content_set.filter(deleted=False).aggregate(summary=Sum('price'))
    summary = bid_.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    # summary = contents_.objects.aggregate(sum=Sum('price'))
    is_manager = request.user.groups.filter(name='managers').exists()

    prev_ = request.META.get('HTTP_REFERER')

    return render(request, 'project/onebid.html',
                  {'title': 'Заявка №'+str(bid_.number), 'bid_': bid_, 'contents_': contents_, 'sum': summary,
                   'is_manager': is_manager, 'prev': prev_, 'page': page_number, 'object': object_id, 'number': number, 'sum_filter': sum_filter, 'unlocked_only': unlocked_only, 'undelivered_only': undelivered_only, 'extended': extended, 'selected_supplier': selected_supplier, 'rollback': rollback})


def is_same_headofsales(request, contract):
    is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    if is_headofsales:
        sellergroup = request.user.groups.filter(name__contains='sellersgroup')
        if sellergroup:
            sellergroup = sellergroup[0].name
            sellers = User.objects.filter(groups__name=sellergroup).values('id')
            sell = []
            for item in sellers:
                sell.append(item['id'])
            if contract.owner.id in sell:
                return True
    return False


@login_required
def one_contract(request, contract_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page', 1)
    object_id = request.GET.get('f')
    contract = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    #is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    is_headofsales = is_same_headofsales(request, contract)
    if contract.deleted:
        raise Http404
    if contract.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    contracts_in_archive = get_settings('contracts_in_archive', 3)
    if contracts_in_archive and contract.status == 'd' and not is_accountant and not is_boss:
        raise Http404

    datenow = datetime.datetime.now()
    #contents_ = bid_.content_set.filter(deleted=False).order_by('type')
    #summary = bid_.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    incoming = contract.turnover_set.filter(deleted=False, type__lt=100).order_by('date')
    comm_ex = contract.turnover_set.filter(deleted=False, type=100).order_by('date')
    comm_ag = contract.turnover_set.filter(deleted=False, type=101).order_by('date')

    unperformed = contract.turnover_set.filter(deleted=False, performed=False).count()
    performed = contract.turnover_set.filter(deleted=False, performed=True).count()
    income = contract.turnover_set.filter(deleted=False, performed=True, type__lt=100).aggregate(summary=Sum('amount'))['summary']
    paid = contract.turnover_set.filter(deleted=False, performed=True, type__gte=100).aggregate(summary=Sum('amount'))['summary']
    contract.unperformed = unperformed
    contract.performed = performed
    if income:
        contract.income = round(income, 2)
    else:
        contract.income = 0.0
    if paid:
        contract.paid = round(paid, 2)
    else:
        contract.paid = 0.0
    income_equal = (float(contract.price - contract.agency_discount - contract.developer_discount) - float(contract.income)) == 0
    paid_equal = (float(contract.agency_commission + contract.seller_commission) - float(contract.paid)) == 0
    contract.income_equal = income_equal
    contract.paid_equal = paid_equal

    return render(request, 'project/onecontract.html',
                  {'title': '', 'contract': contract, 'page': page_number, 'object': object_id, 'rollback': rollback,
                   'incoming': incoming, 'comm_ex': comm_ex, 'comm_ag': comm_ag, 'datenow': datenow})


@login_required
def view_image(request, contract_id, image_id):
    rollback = request.GET.urlencode()
    contract = Contract.objects.get(id=contract_id)
    image = ContractImage.objects.get(id=image_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = is_same_headofsales(request, contract)
    #print("--------------------->", contract.delete, '---', contract.revoked)
    if contract.deleted or contract.revoked:
        raise Http404
    if image.deleted:
        raise Http404
    if contract.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404

    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #print(BASE_DIR, image.image.path)
    filename = image.image.path

    #print(filename)
    with open(filename, "rb") as img_file:
        b64_string = base64.b64encode(img_file.read()).decode('utf-8')

    return render(request, 'project/viewimage.html',
                  {'title': '', 'contract': contract, 'image': image, 'filename': filename, 'imgbase': b64_string, 'rollback': rollback})


@login_required
def delete_image(request, contract_id, image_id):
    rollback = request.GET.urlencode()
    contract = Contract.objects.get(id=contract_id)
    image = ContractImage.objects.get(id=image_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if image.deleted:
        raise Http404
    is_headofsales = is_same_headofsales(request, contract)
    if contract.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404


    image.deleted = True
    image.save()

    return HttpResponseRedirect(reverse('project:contractreceipt', args=[contract.id])+'?' + str(rollback))


@login_required
def contents_add(request, bid_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    error = ''
    bid_ = Bid.objects.get(id=bid_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    if bid_.owner != request.user and not is_manager:
        raise Http404
    if bid_.locked:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    if request.method == 'POST':
        form = ContentsForm(request.POST, objectid=bid_.object)
        if form.is_valid():
            new_contents_ = form.save(commit=False)
            new_contents_.bid = bid_
            # now = datetime.datetime.now()
            # new_contents_.date = now
            #if new_contents_.type == 'd':
            #    new_contents_.quantity = 1
            new_contents_.save()
            return HttpResponseRedirect(reverse('project:onebid', args=[bid_.id])+'?'+str(rollback))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'bid': bid_,
                'title': 'Заявка №' + str(bid_.number),
                'page': page_number,
                'object': object_id,
                'number': number,
                'sum_filter': sum_filter,
                'unlocked_only': unlocked_only,
                'rollback': rollback
            }
            return render(request, 'project/addcontents.html', context)
    form = ContentsForm(objectid=bid_.object)
    context = {
        'form': form,
        'error': error,
        'bid': bid_,
        'title': 'Заявка №' + str(bid_.number),
        'page': page_number,
        'object': object_id,
        'number': number,
        'sum_filter': sum_filter,
        'unlocked_only': unlocked_only,
        'rollback': rollback
    }
    return render(request, 'project/addcontents.html', context)


@login_required
def contents_edit(request, content_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    error = ''
    content_ = Content.objects.get(id=content_id)
    bid_ = content_.bid
    is_manager = request.user.groups.filter(name='managers').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if bid_.deleted:
        raise Http404
    if bid_.owner != request.user and not is_manager:
        raise Http404
    if bid_.locked and not is_boss:
        raise Http404
    if content_.deleted:
        raise Http404
    if request.method == 'POST':
        form = ContentsForm(request.POST, instance=content_, objectid=bid_.object)
        if form.is_valid():

            #now = datetime.datetime.now()
            #form.date = now
            #if content_.type == 'd':
            #    content_.quantity = 1
            form.save()
#            new_contents_ = form.save(commit=True)
#            new_contents_.bid = bid_
#            now = datetime.datetime.now()
#            new_contents_.date = now
#            new_contents_.save()
            return HttpResponseRedirect(reverse('project:onebid', args=[bid_.id])+'?'+str(rollback))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'bid': bid_,
                'content': content_,
                'title': 'Заявка №'+str(bid_.number),
                'page': page_number,
                'object': object_id,
                'number': number,
                'copy': False,
                'sum_filter': sum_filter,
                'unlocked_only': unlocked_only,
                'rollback': rollback
            }
            return render(request, 'project/editcontents.html', context)
    data = {'house': content_.house, 'title': content_.title, 'date': content_.date, 'type': content_.type,
            'cash': content_.cash,
            'quantity': content_.quantity, 'measure': content_.measure, 'price': content_.price,
            'supplier': content_.supplier, 'phase': content_.phase, 'estimate':content_.estimate, 'comment': content_.comment, 'prepaid': content_.prepaid}
    form = ContentsForm(data, objectid=bid_.object)
    context = {
        'form': form,
        'error': error,
        'bid': bid_,
        'content': content_,
        'title': 'Заявка №'+str(bid_.number),
        'page': page_number,
        'object': object_id,
        'number': number,
        'copy': False,
        'sum_filter': sum_filter,
        'unlocked_only': unlocked_only,
        'rollback': rollback
    }
    return render(request, 'project/editcontents.html', context)


@login_required
def contents_copy(request, content_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    error = ''
    content_ = Content.objects.get(id=content_id)
    bid_ = content_.bid
    is_manager = request.user.groups.filter(name='managers').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if bid_.deleted:
        raise Http404
    if bid_.owner != request.user and not is_manager:
        raise Http404
    if bid_.locked and not is_boss:
        raise Http404
    if content_.deleted:
        raise Http404
    if request.method == 'POST':
        form = ContentsForm(request.POST, objectid=bid_.object)
        if form.is_valid():
            new_contents_ = form.save(commit=False)
            new_contents_.bid = bid_
            if content_.type == 'd':
                content_.quantity = 1
            form.save()
            return HttpResponseRedirect(reverse('project:onebid', args=[bid_.id])+'?'+ str(rollback))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'bid': bid_,
                'content': content_,
                'title': 'Заявка №'+str(bid_.number),
                'page': page_number,
                'object': object_id,
                'number': number,
                'copy': True,
                'sum_filter': sum_filter,
                'unlocked_only': unlocked_only,
                'rollback': rollback
            }
            return render(request, 'project/editcontents.html', context)
    data = {'house': None, 'title': content_.title, 'date': content_.date, 'type': content_.type,
            'cash': content_.cash,
            'quantity': content_.quantity, 'measure': content_.measure, 'price': content_.price,
            'supplier': content_.supplier, 'phase': content_.phase, 'estimate': content_.estimate, 'comment': content_.comment}
    form = ContentsForm(data, objectid=bid_.object)
    context = {
        'form': form,
        'error': error,
        'bid': bid_,
        'content': content_,
        'title': 'Заявка №'+str(bid_.number),
        'page': page_number,
        'object': object_id,
        'number': number,
        'copy': True,
        'sum_filter': sum_filter,
        'unlocked_only': unlocked_only,
        'rollback': rollback
    }
    return render(request, 'project/editcontents.html', context)


@login_required
def new_bid(request):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    error = ''
    if request.method == 'POST':
        form = BidForm(request.POST)
        if form.is_valid():
            num_ = form.cleaned_data['number']
            found_bid = Bid.objects.filter(deleted=False, number=num_)
            if found_bid:
                error = 'Уже есть заявка с номером ' + num_ + '!'
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Новая заявка',
                    'page': page_number,
                    'object': object_id,
                    'number': number,
                    'sum_filter': sum_filter,
                    'unlocked_only': unlocked_only
                }
                return render(request, 'project/addbid.html', context)
            else:
                new_bid_ = form.save(commit=False)
                now = datetime.datetime.now()
                new_bid_.date = now
                new_bid_.owner = request.user
                new_bid_.save()
                # return redirect('project:bids')
                return HttpResponseRedirect(reverse('project:onebid', args=[new_bid_.id])+'?' + rollback) #) page='+str(page_number)+'&f='+str(object_id)+'&q='+str(number)+'&s='+str(sum_filter)+'&l='+str(unlocked_only))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новая заявка',
                'page': page_number,
                'object': object_id,
                'number': number,
                'sum_filter': sum_filter,
                'unlocked_only': unlocked_only
            }
            return render(request, 'project/addbid.html', context)

    max_bid_number = Bid.objects.filter(deleted=False).extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')[0]
    try:
        max_bid = str(int(max_bid_number.n) - 10000000 + 1)
    except:
        max_bid = ''

    #print(max_bid)

    form = BidForm(initial={'number': max_bid,})
    context = {
        'form': form,
        'error': error,
        'title': 'Новая заявка',
        'page': page_number,
        'object': object_id,
        'sum_filter': sum_filter,
        'unlocked_only': unlocked_only,
        'rollback': rollback
    }
    return render(request, 'project/addbid.html', context)

def rollback_return(request):
    rollback = request.GET.urlencode()
    number = request.GET.get('q')
    extended = request.GET.get('x')
    supplier = request.GET.get('supplier')
    try:
        supplier = int(supplier)
    except:
        supplier = 0
    if number:
        return HttpResponseRedirect(reverse('project:found') + '?' + str(rollback))
    elif extended:
        return HttpResponseRedirect(reverse('project:phasereport') + '?' + str(rollback))
    elif supplier:
        return HttpResponseRedirect(reverse('project:supplierdetailreport', args=[supplier]) + '?' + str(rollback))
    else:
        return HttpResponseRedirect(reverse('project:bids')+'?'+str(rollback))


@login_required
def bid_lock(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    cnt = bid_.content_set.filter(deleted=False, type='b').count()
    if bid_.deleted:
        raise Http404
    if not is_manager:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    if not bid_.highlighted and not bid_.supervision and cnt>0:
        raise Http404
    bid_.locked = True
    bid_.save()
    return rollback_return(request)

@login_required
def bid_unlock(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    if not is_manager:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    bid_.locked = False
    if bid_.supervision:
        bid_.supervision = False
    bid_.save()
    return rollback_return(request)

@login_required
def bid_mark(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    #is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    if request.user != bid_.owner:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404

    wcnt = bid_.content_set.filter(deleted=False, type='b').count()
    tcnt = bid_.content_set.filter(deleted=False, type='c').count()

    if wcnt == 0 and tcnt > 0:
        bid_.supervision = True
        bid_.supervisor = '-'

    bid_.highlighted = True
    bid_.save()
    return rollback_return(request)


@login_required
def bid_unmark(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    if bid_.deleted:
        raise Http404
    if bid_.locked:
        raise Http404
    if not is_boss:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    #if is_manager:
    #    raise Http404
    bid_.highlighted = False
    bid_.supervision = False
    bid_.supervisor = ''
    bid_.save()
    return rollback_return(request)


@login_required
def bid_hide(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    if bid_.deleted:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if not is_special:
        raise Http404

    bid_.hidden = True
    bid_.save()
    return rollback_return(request)


@login_required
def bid_unhide(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    if bid_.deleted:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if not is_special:
        raise Http404

    bid_.hidden = False
    bid_.save()
    return rollback_return(request)


@login_required
def bid_refund(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    if bid_.deleted:
        raise Http404
    if not bid_.locked:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if not is_special:
        raise Http404

    bid_.refunded = True
    bid_.save()
    return rollback_return(request)


@login_required
def bid_cancel_refund(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    if bid_.deleted:
        raise Http404
    if not bid_.locked:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if not is_special:
        raise Http404

    bid_.refunded = False
    bid_.save()
    return rollback_return(request)


@login_required
def bid_delivery(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    not_prepaid = bid_.content_set.filter(deleted=False, type='a', prepaid=True).count()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    if (not bid_.locked and not_prepaid == 0):
        raise Http404
    if not is_boss and not is_manager and bid_.owner != request.user:
        raise Http404
    bid_.highlighted = False
    bid_.supervision = True
    bid_.save()
    return rollback_return(request)


@login_required
def bid_sign(request, bid_id):
    bid_ = Bid.objects.get(id=bid_id)
    is_supervisor = request.user.groups.filter(name='supervisors').exists()
    if bid_.deleted:
        raise Http404
    if not bid_.highlighted:
        raise Http404
    if not is_supervisor:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    bid_.supervision = True
    bid_.supervisor = request.user.last_name + ' ' + request.user.first_name
    bid_.save()
    return rollback_return(request)


@login_required
def contents_delete(request, content_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    content_ = Content.objects.get(id=content_id)
    bid_ = content_.bid

    if bid_.deleted:
        raise Http404

    is_manager = request.user.groups.filter(name='managers').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if bid_.owner != request.user and not is_manager:
        raise Http404
    if bid_.locked and not is_boss:
        raise Http404

    content_.deleted = True
    content_.save()
    return HttpResponseRedirect(reverse('project:onebid', args=[bid_.id])+'?' + str(rollback))


@login_required
def bid_del(request, bid_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    bid_ = Bid.objects.get(id=bid_id)
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    #is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.owner != request.user:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    if bid_.locked or bid_.highlighted or bid_.supervision:
        raise Http404
    # удалять может только сотрудник (не менеджер!)

    bid_.deleted = True
    bid_.save()
    return HttpResponseRedirect(reverse('project:bids')+'?'+str(rollback))


@login_required
def bid_edit(request, bid_id):
    rollback = request.GET.urlencode()
    page_number = request.GET.get('page')
    object_id = request.GET.get('f')
    number = request.GET.get('q')
    sum_filter = request.GET.get('s')
    unlocked_only = request.GET.get('l')
    error = ''
    bid_ = Bid.objects.get(id=bid_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if bid_.deleted:
        raise Http404
    if bid_.owner != request.user and not is_manager:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404
    if bid_.locked:
        raise Http404
    if bid_.deleted:
        raise Http404
    if request.method == 'POST':
        form = BidEditForm(request.POST, instance=bid_)
        if form.is_valid():
            num_ = form.cleaned_data['number']
            found_bid = Bid.objects.filter(~Q(id=bid_.id), deleted=False, number=num_)
            if found_bid:
                error = 'Уже есть заявка с номером ' + str(bid_.number) + '!'
                context = {
                    'form': form,
                    'error': error,
                    'bid': bid_,
                    'title': 'Заявка №' + str(bid_.number),
                    'page': page_number,
                    'object': object_id,
                    'number': number,
                    'sum_filter': sum_filter,
                    'unlocked_only': unlocked_only,
                    'rollback': rollback
                }
                return render(request, 'project/editbid.html', context)
            else:
                form.save()
                return HttpResponseRedirect(reverse('project:onebid', args=[bid_.id])+'?'+str(rollback))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'bid': bid_,
                'title': 'Заявка №'+str(bid_.number),
                'page': page_number,
                'object': object_id,
                'number': number,
                'sum_filter': sum_filter,
                'unlocked_only': unlocked_only,
                'rollback': rollback
            }
            return render(request, 'project/editbid.html', context)
    data = {'number': bid_.number, 'title': bid_.title, 'object': bid_.object, 'owner': bid_.owner,
                    'locked': bid_.locked, 'deleted': bid_.deleted, 'highlighted': bid_.highlighted}
    form = BidEditForm(data)
    context = {
        'form': form,
        'error': error,
        'bid': bid_,
        'title': 'Заявка №' + str(bid_.number),
        'page': page_number,
        'object': object_id,
        'number': number,
        'sum_filter': sum_filter,
        'unlocked_only': unlocked_only,
        'rollback': rollback
    }
    return render(request, 'project/editbid.html', context)


@login_required
def contract_report(request, contract_id):
    def row_height(l1, l2):
        l = max(l1, l2) #// + 12
        h = l // 28 + 1
        return 16 * h

    def amount_space_separator(amount):
        amount = '{:,}'.format(amount).replace(',', ' ')
        if amount[-2:] == '.0': amount = amount + '0'
        return amount

    contract_ = Contract.objects.get(id=contract_id)

    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    contracts_in_archive = get_settings('contracts_in_archive', 3)
    if contracts_in_archive and contract_.status == 'd' and not is_accountant and not is_boss:
        raise Http404

    income = contract_.turnover_set.filter(deleted=False, performed=True, type__lt=100).aggregate(summary=Sum('amount'))['summary']
    paid = contract_.turnover_set.filter(deleted=False, performed=True, type__gte=100).aggregate(summary=Sum('amount'))['summary']

    all_income = contract_.turnover_set.filter(deleted=False, performed=True, type__lt=100).order_by('date')
    comm_ex = contract_.turnover_set.filter(deleted=False, performed=True, type=100).order_by('date')
    comm_ag = contract_.turnover_set.filter(deleted=False, performed=True, type=101).order_by('date')

    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.set_portrait()
    worksheet.set_margins(1.0, 0.5, 0.55, 0.55)
    cell_format_bold = workbook.add_format({
        'bold': 1,
        'border': 0,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'font': 'Times New Roman',
        'text_wrap': True})
    cell_format = workbook.add_format({
        'bold': 0,
        'border': 0,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'font': 'Times New Roman',
        'text_wrap': True})
    cell_format_bold_underline = workbook.add_format({
        'bold': 1,
        'border': 0,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'underline': 1,
        'font': 'Times New Roman',
        'text_wrap': True})
    worksheet.set_column(0, 0, 90)
        #segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
       #worksheet.write_rich_string('I' + str(row + 1), *segments)
    worksheet.write(0, 0, contract_.date.strftime("%d.%m.%Y") + "г. " +contract_.get_type_display()+ "-" + contract_.number+ " " + contract_.object.name + ", Литер " + contract_.house.name.replace('Дом', '').replace('№','').replace(' ', '') + ", апартамент " + contract_.apartment + " " + contract_.title, cell_format_bold)
    worksheet.set_row(0, 30)
    worksheet.write(1, 0, "Клиент: " + contract_.client, cell_format_bold)
    worksheet.set_row(1, 20)
    worksheet.write(2, 0, "агент(агенство): " + contract_.agency, cell_format_bold)
    worksheet.set_row(2, 20)
    worksheet.write(3, 0, "Менеджер ОП: " + contract_.owner.last_name + " " + contract_.owner.first_name, cell_format)
    worksheet.set_row(3, 20)
    worksheet.write(4, 0, "Помещение: " + contract_.apartment, cell_format_bold)
    worksheet.set_row(4, 20)

    worksheet.write(5, 0, "Площадь: " + str(contract_.square) + " кв.м", cell_format_bold)
    worksheet.set_row(5, 20)
    worksheet.write(6, 0, "Цена по шахматке: " + amount_space_separator(contract_.price) + " руб", cell_format_bold)
    worksheet.set_row(6, 20)
    worksheet.write(7, 0, "Скидка АН: " + amount_space_separator(contract_.agency_discount) + " руб", cell_format_bold)
    worksheet.set_row(7, 20)

    worksheet.write(8, 0, "Скидка застройщика: " + amount_space_separator(contract_.developer_discount) + " руб", cell_format_bold)
    worksheet.set_row(8, 20)
    worksheet.write(9, 0, "Итого сумма контракта: " + amount_space_separator(contract_.price - contract_.agency_discount - contract_.developer_discount) + " руб", cell_format_bold)
    worksheet.set_row(9, 30)
    #worksheet.write(10, 0, "Скидка АН: " + contract_.agency_discount, cell_format_bold)
    #worksheet.write(11, 0, "Скидка АН: " + contract_.agency_discount, cell_format_bold)
    #worksheet.write(12, 0, "Скидка АН: " + contract_.agency_discount, cell_format_bold)
    i = 10
    for item in all_income:
        worksheet.write(i, 0, item.comment, cell_format)
        #worksheet.set_row(i, 20)
        i += 1

    worksheet.write(i, 0, "Комиссия ОП:", cell_format_bold_underline)
    worksheet.set_row(i, 40)
    i += 1
    worksheet.write(i, 0, contract_.seller_commission_calc + " = " + amount_space_separator(contract_.seller_commission) + " руб", cell_format)
    worksheet.set_row(i, 20)
    i += 1
    for item in comm_ex:
        worksheet.write(i, 0, item.comment, cell_format)
        #worksheet.set_row(i, 20)
        i += 1

    worksheet.write(i, 0, "Комиссия АН:", cell_format_bold_underline)
    worksheet.set_row(i, 40)
    i += 1
    worksheet.write(i, 0, contract_.agency_commission_calc + " = " + amount_space_separator(contract_.agency_commission) + " руб", cell_format)
    worksheet.set_row(i, 20)
    i += 1
    for item in comm_ag:
        worksheet.write(i, 0, item.comment, cell_format)
        #worksheet.set_row(i, 20)
        i += 1

    worksheet.write(i, 0, "Итого комиссии: " + amount_space_separator(contract_.agency_commission + contract_.seller_commission) + " руб", cell_format_bold)
    worksheet.set_row(i, 40)
    i += 1
    worksheet.write(i, 0, "На руки застройщику: " + amount_space_separator(contract_.price - contract_.agency_discount - contract_.developer_discount - contract_.agency_commission - contract_.seller_commission) + " руб", cell_format_bold)
    worksheet.set_row(i, 40)
    i += 1

    worksheet.write(i, 0, "Комиссию выдал: _____________", cell_format_bold)
    worksheet.set_row(i, 40)
    i += 1
    worksheet.write(i, 0, "Комиссию принял: ____________", cell_format_bold)
    worksheet.set_row(i, 20)
    i += 1
    workbook.close()
    buffer.seek(0)

    #return FileResponse(buffer, as_attachment=True, filename='report'+str(bid_.id)+'.xlsx')

    filename = 'report'+str(contract_.id)+'.xlsx'
    response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

@login_required
def bid_report(request, bid_id):
    def row_height(l1, l2):
        l = max(l1, l2) #// + 12
        h = l // 28 + 1
        return 16 * h

    bid_ = Bid.objects.get(id=bid_id)

    if bid_.deleted:
        raise Http404
    is_special = request.user.groups.filter(name='special').exists()
    if bid_.hidden and not is_special:
        raise Http404

    contents_ = bid_.content_set.filter(deleted=False).order_by('type')
    summary = bid_.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    if summary["summary"] is None:
        summary = {'summary': 0}
    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.set_landscape()
    worksheet.set_margins(0.5, 0.5, 0.55, 0.55)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'yellow'})
    cell_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vbottom',
        'fg_color': 'yellow',
        'color': 'red',
        'font_size': 10})
    col_widths = [10, 10.5, 28, 7, 7, 7.5, 10, 12, 28]
    if bid_.refunded:
        worksheet.merge_range('A1:I1', 'Заявка №' + str(bid_.number) + '(Оформлен возврат). Объект: ' + bid_.object.name,
                              workbook.add_format(
                                  {'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'red',
                                   'font_size': 14}))
    else:
        worksheet.merge_range('A1:I1', 'Заявка №'+str(bid_.number)+'. Объект: ' + bid_.object.name, workbook.add_format({'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'yellow', 'font_size': 14}))
    header1 = ['№ дома', 'дата', 'Материалы', 'нал/б нал', 'Объем', 'ед', 'Стоимость', 'Сумма', 'поставщик/комментарий']
    for col_num, data in enumerate(header1):
        worksheet.set_column(col_num, col_num, col_widths[col_num])
        worksheet.write(1, col_num, data, cell_format)

    row = 2
    cell_format_yellow = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'yellow',
        'color': 'black',
        'font_size': 10,
        'text_wrap': True})
    cell_format_yellow_center = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vbottom',
        'fg_color': 'yellow',
        'color': 'black',
        'font_size': 10,
        'text_wrap': True})
    cell_format_white = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'text_wrap': True})
    cell_format_white_center = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'center',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'text_wrap': True})
    cell_format_white_right = workbook.add_format({
        'bold': 0,
        'border': 1,
        'align': 'right',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10,
        'text_wrap': True})
    count = 0
    # материалы
    summ_ = 0.0
    quantity = 0
    for item in contents_:
        if item.type == 'a':
            worksheet.write(row, 0, item.house.name, cell_format_yellow_center)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")), cell_format_white_center)
            worksheet.write(row, 2, item.title, cell_format_white)
            length1 = len(item.title)
            if item.cash == 'y':
                worksheet.write(row, 3, 'нал', cell_format_white_right)
            else:
                if item.cash == 'b':
                    worksheet.write(row, 3, 'бартер', cell_format_white_right)
                else:
                    worksheet.write(row, 3, 'б нал', cell_format_white_right)
            worksheet.write(row, 4, item.quantity, cell_format_white_right)
            quantity += item.quantity
            summ_ = summ_ + float(item.price * item.quantity)
            worksheet.write(row, 5, item.get_measure_display(), cell_format_white_right)
            worksheet.write(row, 6, item.price, workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 7, item.price * item.quantity, workbook.add_format({'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 8, item.comment, cell_format_white_right)
            red_ = workbook.add_format({'color': 'red', 'font_size': 10})
            black_ = workbook.add_format(
                {'color': 'black', 'font_size': 10})
            align_ = workbook.add_format({'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})
            commentstr = item.supplier.name + '/' + item.comment
            #worksheet.write(row, 8, commentstr, cell_format_white_right)
            segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
            worksheet.write_rich_string('I' + str(row+1), *segments)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))
            row += 1
            count += 1
    for col_num, data in enumerate(header1):
        worksheet.write(row, col_num, '', cell_format_white)
    worksheet.write(row, 0, '', cell_format_yellow)
    if count > 0:
        worksheet.write(row, 3, 'Подитог:', workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
        worksheet.write(row, 4, quantity, cell_format_white_right)
        worksheet.write(row, 7, summ_, workbook.add_format(
        {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 10, 'text_wrap': True}))
    row += 1


    header1 = ['№ дома', 'дата', 'Строительно монтажные работы', 'нал/б нал', 'Объем', 'ед', 'Стоимость', 'Сумма', 'поставщик/комментарий']
    for col_num, data in enumerate(header1):
        worksheet.set_column(col_num, col_num, col_widths[col_num])
        worksheet.write(row, col_num, data, cell_format)

    row += 1
    count = 0
    # работы
    summ_ = 0.0
    quantity = 0
    for item in contents_:
        if item.type == 'b':
            worksheet.write(row, 0, item.house.name, cell_format_yellow_center)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")), cell_format_white_center)
            worksheet.write(row, 2, item.title, cell_format_white)
            length1 = len(item.title)
            if item.cash == 'y':
                worksheet.write(row, 3, 'нал', cell_format_white_right)
            else:
                if item.cash == 'b':
                    worksheet.write(row, 3, 'бартер', cell_format_white_right)
                else:
                    worksheet.write(row, 3, 'б нал', cell_format_white_right)
            worksheet.write(row, 4, item.quantity, cell_format_white_right)
            quantity += item.quantity
            summ_ = summ_ + float(item.price * item.quantity)
            worksheet.write(row, 5, item.get_measure_display(), cell_format_white_right)
            worksheet.write(row, 6, item.price, workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 7, item.price * item.quantity, workbook.add_format({'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 8, item.comment, cell_format_white_right)
            red_ = workbook.add_format({'color': 'red', 'font_size': 10})
            black_ = workbook.add_format(
                {'color': 'black', 'font_size': 10})
            align_ = workbook.add_format({'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})
            commentstr = item.supplier.name + '/' + item.comment
            #worksheet.write(row, 8, commentstr, cell_format_white_right)
            segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
            worksheet.write_rich_string('I' + str(row+1), *segments)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))
            row += 1
            count += 1

    for col_num, data in enumerate(header1):
        worksheet.write(row, col_num, '', cell_format_white)
    worksheet.write(row, 0, '', cell_format_yellow)
    if count > 0:
        worksheet.write(row, 3, 'Подитог:', workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
        worksheet.write(row, 4, quantity, cell_format_white_right)
        worksheet.write(row, 7, summ_, workbook.add_format(
        {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 10, 'text_wrap': True}))
    row += 1

    header1 = ['№ дома', 'дата', 'Техника', 'нал/б нал', 'Время', 'ч/д', 'Стоимость', 'Сумма', 'поставщик/комментарий']
    for col_num, data in enumerate(header1):
        worksheet.set_column(col_num, col_num, col_widths[col_num])
        worksheet.write(row, col_num, data, cell_format)

    row += 1
    count = 0
    summ_ = 0.0
    quantity = 0
    # техника
    for item in contents_:
        if item.type == 'c':
            worksheet.write(row, 0, item.house.name, cell_format_yellow_center)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")), cell_format_white_center)
            worksheet.write(row, 2, item.title, cell_format_white)
            length1 = len(item.title)
            if item.cash == 'y':
                worksheet.write(row, 3, 'нал', cell_format_white_right)
            else:
                if item.cash == 'b':
                    worksheet.write(row, 3, 'бартер', cell_format_white_right)
                else:
                    worksheet.write(row, 3, 'б нал', cell_format_white_right)
            worksheet.write(row, 4, item.quantity, cell_format_white_right)
            quantity += item.quantity
            summ_ = summ_ + float(item.price * item.quantity)
            worksheet.write(row, 5, item.get_measure_display(), cell_format_white_right)
            worksheet.write(row, 6, item.price, workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 7, item.price * item.quantity, workbook.add_format({'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            red_ = workbook.add_format({'color': 'red', 'font_size': 10})
            black_ = workbook.add_format(
                {'color': 'black', 'font_size': 10})
            align_ = workbook.add_format({'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})
            commentstr = item.supplier.name + '/' + item.comment
            #worksheet.write(row, 8, commentstr, cell_format_white_right)
            segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
            worksheet.write_rich_string('I' + str(row+1), *segments)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))
            row += 1
            count += 1
    for col_num, data in enumerate(header1):
        worksheet.write(row, col_num, '', cell_format_white)
    worksheet.write(row, 0, '', cell_format_yellow)
    if count > 0:
        worksheet.write(row, 3, 'Подитог:', workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
        worksheet.write(row, 4, quantity, cell_format_white_right)
        worksheet.write(row, 7, summ_, workbook.add_format(
        {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 10, 'text_wrap': True}))
    row += 1

    #row += 1
    #worksheet.merge_range('C'+str(row)+':D'+str(row), '', merge_format)
    #orksheet.merge_range('E'+str(row)+':H'+str(row), '', merge_format)
    ####worksheet.write(row, 0, '', cell_format_yellow)
    #worksheet.merge_range('I'+str(row)+':I'+str(row), '', merge_format)




    #####

    count = 0
    for item in contents_:
        if item.type == 'f':
            count += 1

    if count > 0:
        header2 = ['№ дома', 'дата', 'Прочие расходы', 'нал/б нал', 'Кол-во', 'ед.изм.', 'Стоимость', 'Сумма', 'поставщик/комментарий']
        for col_num, data in enumerate(header2):
            worksheet.set_column(col_num, col_num, col_widths[col_num])
            worksheet.write(row, col_num, data, cell_format)
        row += 1

    count = 0
    # прочие расходы
    summ_ = 0.0
    quantity = 0
    for item in contents_:
        if item.type == 'f':
            worksheet.write(row, 0, item.house.name, cell_format_yellow_center)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")), cell_format_white_center)
            worksheet.write(row, 2, item.title, cell_format_white)
            length1 = len(item.title)
            if item.cash == 'y':
                worksheet.write(row, 3, 'нал', cell_format_white_right)
            else:
                if item.cash == 'b':
                    worksheet.write(row, 3, 'бартер', cell_format_white_right)
                else:
                    worksheet.write(row, 3, 'б нал', cell_format_white_right)
            worksheet.write(row, 4, item.quantity, cell_format_white_right)
            quantity += item.quantity
            summ_ = summ_ + float(item.price * item.quantity)
            worksheet.write(row, 5, item.get_measure_display(), cell_format_white_right)
            worksheet.write(row, 6, item.price, workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 7, item.price * item.quantity, workbook.add_format({'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            red_ = workbook.add_format({'color': 'red', 'font_size': 10})
            black_ = workbook.add_format(
                {'color': 'black', 'font_size': 10})
            align_ = workbook.add_format({'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})
            commentstr = item.supplier.name + '/' + item.comment
            #worksheet.write(row, 8, commentstr, cell_format_white_right)
            segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
            worksheet.write_rich_string('I' + str(row+1), *segments)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))
            row += 1
            count += 1

    for col_num, data in enumerate(header1):
        worksheet.write(row, col_num, '', cell_format_white)
    worksheet.write(row, 0, '', cell_format_yellow)
    if count > 0:
        worksheet.write(row, 3, 'Подитог:', workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
        worksheet.write(row, 4, quantity, cell_format_white_right)
        worksheet.write(row, 7, summ_, workbook.add_format(
        {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 10, 'text_wrap': True}))
        row += 1

    row += 1
    worksheet.merge_range('C'+str(row)+':D'+str(row), '', merge_format)
    worksheet.merge_range('E'+str(row)+':H'+str(row), '', merge_format)
    worksheet.write(row, 8, '', merge_format)
    #worksheet.merge_range('I'+str(row)+':I'+str(row), '', merge_format)

    #row += 1

    header1 = ['№ дома', 'дата', 'Доставка', '', 'Стоимость', '', '','', 'поставщик/комментарий']
    for col_num, data in enumerate(header1):
        worksheet.write(row-1, col_num, data, cell_format)

    count = 0
    #row += 1
    # доставка
    summ_ = 0.0
    quantity = 0
    for item in contents_:
        if item.type == 'd' or item.type == 'e':
            worksheet.write(row, 0, item.house.name, cell_format_yellow_center)
            worksheet.write(row, 1, item.date.strftime(("%d.%m.%Y")), cell_format_white_center)

            worksheet.merge_range('C' + str(row+1) + ':D' + str(row+1), item.title, cell_format_white)
            length1 = len(item.title)
            worksheet.write(row, 4, item.quantity, cell_format_white_right)
            quantity += item.quantity
            summ_ = summ_ + float(item.price * item.quantity)
            worksheet.write(row, 5, 'шт.', cell_format_white_right)
            worksheet.write(row, 6, item.price, workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            worksheet.write(row, 7, item.price * item.quantity, workbook.add_format({'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
#            worksheet.merge_range('E' + str(row+1) + ':F' + str(row+1), item.price, workbook.add_format(
#                {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom',
#                 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
#            worksheet.merge_range('E' + str(row+1) + ':H' + str(row+1), item.price, workbook.add_format(
#                {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom',
#                 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            #worksheet.merge_range('I' + str(row+1) + ':I' + str(row+1), item.comment, cell_format_white_right)
            red_ = workbook.add_format({'color': 'red', 'font_size': 10})
            black_ = workbook.add_format(
                {'color': 'black', 'font_size': 10})
            align_ = workbook.add_format({'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})
            commentstr = item.supplier.name + '/' + item.comment
            #worksheet.write(row, 8, commentstr, cell_format_white_right)
            segments = [red_, item.supplier.name, '/', black_, item.comment, align_]
            worksheet.write_rich_string('I' + str(row+1), *segments)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))

            row += 1
            count += 1

    for col_num, data in enumerate(header1):
        worksheet.write(row, col_num, '', cell_format_white)
    worksheet.write(row, 0, '', cell_format_yellow)
    if count > 0:
        worksheet.write(row, 3, 'Подитог:', workbook.add_format(
            {'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
        worksheet.write(row, 4, quantity, cell_format_white_right)
        worksheet.write(row, 7, summ_, workbook.add_format(
        {'num_format': '#,##0.00', 'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 10, 'text_wrap': True}))
        row += 1
    #row += 1
    if count == 0:
        worksheet.write(row, 0, '', cell_format_yellow)
        worksheet.write(row, 1, '', cell_format_white)
        worksheet.merge_range('C' + str(row + 1) + ':D' + str(row + 1), '', cell_format_white)
        worksheet.merge_range('E' + str(row + 1) + ':H' + str(row + 1), '', cell_format_white)
        #worksheet.merge_range('I' + str(row + 1) + ':I' + str(row + 1), '', cell_format_white)
        worksheet.write(row, 8, '', cell_format_white)
        row += 1
    row += 1
    # if summary["summary"] > 0:
    worksheet.merge_range('A'+str(row)+':I'+str(row), 'Сумма, итого: ' + '{:10,.2f}'.format(summary["summary"]).replace(',', ' '), workbook.add_format({'bold': 1, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'yellow', 'font_size': 12}))

    if bid_.highlighted:
        worksheet.write(row + 2, 1, 'Принято прорабом: '+bid_.owner.last_name + ' '+ bid_.owner.first_name, workbook.add_format(
        {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 12, 'text_wrap': False}))
    if bid_.supervision and bid_.supervisor != '-' and bid_.supervisor != '+':
        worksheet.write(row + 3, 1, 'Принято технадзором: '+bid_.supervisor, workbook.add_format(
        {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 12, 'text_wrap': False}))

    worksheet.write(row + 4, 1, 'Согласовано:', workbook.add_format(
        {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'white',
         'color': 'black', 'font_size': 12, 'text_wrap': False}))
    #worksheet.write(row + 4, 1, 'Смета (этап строительства): ' + bid_.phase.name, workbook.add_format(
    #    {'bold': 1, 'border': 0, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'white',
    #     'color': 'black', 'font_size': 12, 'text_wrap': False}))

    #for i in range(2, row-1):
    #    worksheet.

    workbook.close()
    buffer.seek(0)

    #return FileResponse(buffer, as_attachment=True, filename='report'+str(bid_.id)+'.xlsx')

    filename = 'report'+str(bid_.id)+'.xlsx'
    response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response




@login_required
def archive(request):
    page_number = request.GET.get('page')
    is_manager = request.user.groups.filter(name='managers').exists()
    if is_manager:
        myarchive = Archive.objects.filter(deleted=False).order_by('-number')
    else:
        myarchive = Archive.objects.filter(owner=request.user, deleted=False).order_by('-number')
    paginator = Paginator(myarchive, 10)
    # page_obj = paginator.get_page(page_number)

    try:
        page_ = paginator.page(page_number)
    except:
        page_ = paginator.page(1)
        page_number = 1

    return render(request, 'project/archive.html',
                  {'title': 'Архивные заявки', 'myarchive': page_.object_list, 'page': page_number, 'pages': paginator,
                   'page_': page_})


@login_required
def one_archive_item(request, arch_id):
    #print('->'+str(p))
    page_number = request.GET.get('page')
    number = request.GET.get('q')
    if number == 'None':
        number = None
    arch_ = Archive.objects.get(id=arch_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if arch_.deleted:
        raise Http404
    if arch_.owner != request.user and not is_manager:
        raise Http404
    contents_ = arch_.archivedetail_set.filter(deleted=False).order_by('id')
    summary_ = arch_.archivedetail_set.filter(deleted=False).aggregate(summary=Sum('summary'))
    #summary = arch_.content_set.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    # summary = contents_.objects.aggregate(sum=Sum('price'))
    is_manager = request.user.groups.filter(name='managers').exists()

    prev_ = request.META.get('HTTP_REFERER')

    return render(request, 'project/onearchitem.html',
                  {'title': 'Архивная заявка №'+str(arch_.number), 'arch_': arch_, 'contents_': contents_, 'sum': summary_, 'is_manager': is_manager, 'page': page_number, 'number': number})


@login_required
def arch_edit(request, arch_id):
    page_number = request.GET.get('page')
    number = request.GET.get('q')
    error = ''
    arch_ = Archive.objects.get(id=arch_id)
    is_manager = request.user.groups.filter(name='managers').exists()
    if arch_.deleted:
        raise Http404
    if not is_manager:
        raise Http404
    if request.method == 'POST':
        form = ArchEditForm(request.POST, instance=arch_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:onearchiveitem', args=[arch_.id])+'?page='+str(page_number)+'&q='+str(number))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'arch': arch_,
                'title': 'Заявка №'+str(arch_.number),
                'page': page_number,
                'number': number
            }
            return render(request, 'project/editarch.html', context)
    data = {'number': arch_.number, 'title': arch_.title, 'object': arch_.object, 'owner': arch_.owner,
                    'deleted': arch_.deleted, 'highlighted': arch_.highlighted}
    form = ArchEditForm(data)
    context = {
        'form': form,
        'error': error,
        'arch': arch_,
        'title': 'Заявка №' + str(arch_.number),
        'page': page_number,
        'number': number
    }
    return render(request, 'project/editarch.html', context)


@login_required
def details_edit(request, detail_id):
    page_number = request.GET.get('page')
    number = request.GET.get('q')
    error = ''
    content_ = ArchiveDetail.objects.get(id=detail_id)
    arch_ = content_.archive
    is_manager = request.user.groups.filter(name='managers').exists()
    if arch_.deleted:
        raise Http404
    if not is_manager:
        raise Http404
    if content_.deleted:
        raise Http404
    if request.method == 'POST':
        form = ArchiveDetailForm(request.POST, instance=content_, objectid=arch_.object)
        if form.is_valid():
            new_details_ = form.save(commit=False)
            cd = form.cleaned_data
            new_supplier = cd['new_supplier']
            supplier = Supplier.objects.get(id=new_supplier.id)
            new_details_.supplier = supplier.name
            new_details_.new_supplier = supplier

            form.save()
#            new_contents_ = form.save(commit=True)
#            new_contents_.bid = bid_
#            now = datetime.datetime.now()
#            new_contents_.date = now
#            new_contents_.save()
            return HttpResponseRedirect(reverse('project:onearchiveitem', args=[arch_.id])+'?page='+str(page_number)+'&q='+str(number))
            #return HttpResponseRedirect(reverse('project:onearchiveitem', args=[arch_.id], kwargs={'arch_id':arch_.id, 'p': page_number}))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'arch': arch_,
                'content': content_,
                'title': 'Архивная заявка №'+str(arch_.number),
                'page': page_number,
                'number': number
            }
            return render(request, 'project/editdetails.html', context)
    data = {'house': content_.house, 'title': content_.title, 'date': content_.date,
            'cash': content_.cash, 'spending': content_.spending, 'materials': content_.materials,
            'cost': content_.cost, 'foreman': content_.foreman,
            'quantity': content_.quantity, 'measure': content_.measure, 'summary': content_.summary,
            'supplier': content_.supplier, 'new_supplier': content_.new_supplier, 'phase': content_.phase, 'estimate': content_.estimate, 'comment': content_.comment}
    form = ArchiveDetailForm(data, objectid=arch_.object)
    context = {
        'form': form,
        'error': error,
        'arch': arch_,
        'content': content_,
        'title': 'Архивная заявка №'+str(arch_.number),
        'page': page_number,
        'number': number
    }
    return render(request, 'project/editdetails.html', context)


def get_object_concrete_summary():
    return 0

#@login_required
def get_report_data(datefrom, dateto, estimate, phase, concrete_only, barter_only):
    #datefrom = datetime.date(2022, 2, 8)
    #dateto = datetime.date(2022, 2, 8)

    #print(str(datefrom)+'<->'+str(dateto))
    objects_ = Object.objects.filter().order_by('-id')

    if estimate:
        if barter_only:
            summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__object__name').annotate(summary=Sum('summary'))
            summary2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__object__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__object__name').annotate(summary=Sum('summary'))
            summary2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__object__name').annotate(summary=Sum(F('quantity') * F('price')))
    else:
        if barter_only:
            summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, cash='b').values('house__object__id', 'house__object__name').annotate(summary=Sum('summary'))
            summary2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, cash='b').values('house__object__id','house__object__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__object__name').annotate(summary=Sum('summary'))
            summary2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values(
        'house__object__id', 'house__object__name').annotate(summary=Sum(F('quantity') * F('price')))
    summary3 = summary1.union(summary2, all=True).order_by('house__object__id')

    if estimate:
        if barter_only:
            details1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum('summary'))
            details2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            details1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum('summary'))
            details2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum(F('quantity') * F('price')))
    else:
        if barter_only:
            details1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom,date__lte=dateto, cash='b').values('house__object__id','house__id','house__name').annotate(summary=Sum('summary'))
            details2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, cash='b').values('house__object__id', 'house__id','house__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            details1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom,date__lte=dateto).values('house__object__id','house__id','house__name').annotate(summary=Sum('summary'))
            details2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum(F('quantity') * F('price')))
    details3 = details1.union(details2, all=True).order_by('house__object__id', 'house__id')

    if estimate:
        if barter_only:
            subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum('summary'))
            subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id, cash='b').values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum('summary'))
            subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, estimate__id=estimate.id).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum(F('quantity') * F('price')))
    else:
        if barter_only:
            subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto, cash='b').values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum('summary'))
            subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto, cash='b').values('house__object__id', 'house__id','estimate__id', 'estimate__name').annotate(summary=Sum(F('quantity') * F('price')))
        else:
            subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name').annotate(summary=Sum('summary'))
            subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id','estimate__id', 'estimate__name').annotate(summary=Sum(F('quantity') * F('price')))


    subdetails3 = subdetails1.union(subdetails2, all=True).order_by('house__object__id', 'house__id', 'estimate__id')

    # ------------------
    delivery_obj = []
    if not barter_only:
        delivery_obj = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('object__id', 'object__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id'))

    delivery_obj_ = []
    objectid = 0
    counter = -1
    for item in delivery_obj:
        if item['object__id'] != objectid:
            objectid = item['object__id']
            delivery_obj_.append({'object__id': objectid, 'total_sum': item['total_sum'],
                              'object__name': item['object__name']})
            counter += 1
        else:
            delivery_obj_[counter]['total_sum'] += item['total_sum']

    #print(delivery_obj_)
    # ------------------
    delivery_house = []
    if not barter_only:
        delivery_house = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('house__id', 'object__id', 'house__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id', 'house__id'))

    delivery_house_ = []
    houseid = 0
    counter = -1
    for item in delivery_house:
        if item['house__id'] != houseid:
            houseid = item['house__id']
            delivery_house_.append({'house__id': houseid, 'object__id': item['object__id'], 'total_sum': item['total_sum'],
                              'house__name': item['house__name']})
            counter += 1
        else:
            delivery_house_[counter]['total_sum'] += item['total_sum']

    #print(delivery_house_)

    # если пользователь выбрал опцию "только бетон"
    if concrete_only:
        data = []
        for item in delivery_obj_:
            data.append({'house__object__id': item['object__id'], 'house__object__name': item['object__name'], 'summary': item['total_sum']})

        prev = 0
        data2 = []
        data4 = []
        for item in delivery_house_:
            if item['house__id'] != prev:
                prev = item['house__id']
                data2.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'house__name': item['house__name'], 'summary': item['total_sum']})
                data4.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'estimate__name': 'Бетон', 'estimate__id': 0,
                          'summary': item['total_sum']})
            else:
                data2[len(data2) - 1]['summary'] += item['total_sum']

        summary_volume = (
            Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(summary=Sum('volume')))

        return data, data2, data4, summary_volume['summary']

    # если пользователь НЕ выбрал опцию "только бетон"

    data = []
    prev = 0
    for item in summary3:
        if item['house__object__id'] != prev:
            prev = item['house__object__id']
            data.append({'house__object__id': prev, 'house__object__name': item['house__object__name'], 'summary': item['summary']})
            # если не указана никакая смета, то добавляем сумму бетона к каждому объекту (если она есть)
            if not estimate:
                for obj in delivery_obj_:
                    if obj['object__id'] == item['house__object__id']:
                        data[len(data) - 1]['summary'] += obj['total_sum']
        else:
            data[len(data)-1]['summary'] += item['summary']

    data2 = []
    if not estimate:
        # если не указана никакая смета, то здесь надо добавить объекты, по которым есть только бетон
        for obj in delivery_obj_:
            found = False
            for item in data:
                if item['house__object__id'] == obj['object__id']:
                    found = True
            if not found:
                data.append({'house__object__id': obj['object__id'], 'house__object__name': obj['object__name'], 'summary': obj['total_sum']})
                #data2.append({'house__object__id': obj['object__id'], 'house__object__name': obj['object__name'], 'summary': obj['total_sum']})

    prev = 0

    for item in details3:
        if item['house__id'] != prev:
            prev = item['house__id']
            data2.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'], 'house__name': item['house__name'], 'summary': item['summary']})
            # если не указана никакая смета, то добавляем сумму бетона к каждому дому (если она есть)
            if not estimate:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data2[len(data2) - 1]['summary'] += obj['total_sum']
        else:
            data2[len(data2)-1]['summary'] += item['summary']
    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон
    if not estimate:
        for house in delivery_house_:
            found = False
            for item in data2:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data2.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'house__name': house['house__name'], 'summary': house['total_sum']})

    data4 = []
    prev = 0
    house = 0
    for item in subdetails3:
        if item['estimate__id'] != prev or item['house__id'] != house:
            data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'estimate__name': item['estimate__name'], 'estimate__id': item['estimate__id'], 'phase__id': 0, 'summary': item['summary']})

            # если не указана никакая смета, то добавляем сумму бетона как отдельную смету к каждому дому (если она есть)
            if not estimate and item['house__id'] != house:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'estimate__name': 'Бетон', 'estimate__id': 0, 'phase__id': 0,
                          'summary': obj['total_sum']})
            house = item['house__id']
            prev = item['estimate__id']
        else:
            data4[len(data4) - 1]['summary'] += item['summary']
    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон (чтобы отобразилась кнопка "Бетон")
    if not estimate:
        for house in delivery_house_:
            found = False
            for item in data4:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data4.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'estimate__name': 'Бетон', 'estimate__id': 0, 'phase__id': 0,
                              'summary': house['total_sum']})
                #data2.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                #              'house__name': house['house__name'], 'summary': house['total_sum']})
    #---------------------------------------------------------------------
    #print(len(subdetails3))
    #print(subdetails3)
    data3 = []
    temp = []
    previtem = {'house__id': 0}
    for item in subdetails3:
        #if item['house__object__id']==23: # and item['house__id']==136:
            #print('------------------------------------------>')
        #print(str(item['house__object__id'])+'---->'+str(item['house__id']))
        # тот же дом
        if item['house__id'] == previtem['house__id']:
            # добавляем строку по смете
            temp.append([item['estimate__id'], item['estimate__name'], item['summary']])
        # перешли к следующему дому
        else:
            # не первый дом в списке, надо сохранить в итоговый массив
            if previtem['house__id'] != 0:
                temp.sort()
                #print(str(item['house__object__id'])+'->'+str(item['house__id']))
                #print(temp)
                prev = 0
                for tempitem in temp:
                        if tempitem[0] != prev:
                            prev = tempitem[0]
                            data3.append(
                                {'house__object__id': previtem['house__object__id'],
                                 'house__id': previtem['house__id'],
                                 'estimate__id': previtem['estimate__id'],
                                 'estimate__name': tempitem[1], 'summary': tempitem[2]})
                        else:
                            data3[len(data3) - 1]['summary'] += tempitem[2]

                temp = []
                temp.append([item['estimate__id'], item['estimate__name'], item['summary']])
                previtem = item
            # перый дом
            else:
                previtem = item
                temp.append([item['estimate__id'], item['estimate__name'], item['summary']])

    #print('----->')

    if not barter_only:
        summary_volume = (
        Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(
            summary=Sum('volume')))
    else:
        summary_volume = {'summary': 0}

    return data, data2, data4, summary_volume['summary']


def get_report_data2(datefrom, dateto, estimate, phase, type_, concrete_only, barter_only, exclusion, special):
    #datefrom = datetime.date(2022, 2, 8)
    #dateto = datetime.date(2022, 2, 8)

    #print(str(datefrom)+'<->'+str(dateto))
    objects_ = Object.objects.filter().order_by('-id')

    all_subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum('summary'))
    if special:
        all_subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum(F('quantity') * F('price')))
    else:
        all_subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, bid__hidden=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum(F('quantity') * F('price')))

    if barter_only:
        all_subdetails1 = all_subdetails1.filter(cash='b')
        all_subdetails2 = all_subdetails2.filter(cash='b')
    if estimate:
        all_subdetails1 = all_subdetails1.filter(estimate__id=estimate.id)
        all_subdetails2 = all_subdetails2.filter(estimate__id=estimate.id)
    if phase:
        all_subdetails1 = all_subdetails1.filter(phase__id=phase)
        all_subdetails2 = all_subdetails2.filter(phase__id=phase)
    if type_ != '0':
        all_subdetails1 = all_subdetails1.filter(type=type_)
        all_subdetails2 = all_subdetails2.filter(type=type_)

    if exclusion == '1':
        all_subdetails1 = all_subdetails1.exclude(type='f', phase__id=6, estimate__id=84)
        all_subdetails2 = all_subdetails2.exclude(type='f', phase__id=6, estimate__id=84)

    subdetails3 = all_subdetails1.union(all_subdetails2, all=True).order_by('house__object__id', 'house__id', 'estimate__id', 'phase__id', 'type')


    #all_details1 = all_subdetails1.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'house__name').annotate(summary=Sum('summary'))
    #all_details2 = all_subdetails2.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values( 'house__object__id', 'house__id', 'house__name').annotate(summary=Sum('summary'))
    all_details1 = all_subdetails1.values('house__object__id', 'house__id', 'house__name', 'summary')
    all_details2 = all_subdetails2.values('house__object__id', 'house__id', 'house__name', 'summary')
    details3 = all_details1.union(all_details2, all=True).order_by('house__object__id', 'house__id')
    #print(details3)
    #print(all_details3)

    all_summary1 = all_subdetails1.values('house__object__id', 'house__object__name', 'summary')
    all_summary2 = all_subdetails2.values('house__object__id', 'house__object__name', 'summary')
    summary3 = all_summary1.union(all_summary2, all=True).order_by('house__object__id')
    #print(summary3)
    #print(all_summary3)

    #if estimate or phase:
    #    return summary3, details3, subdetails3, 0


    # ------------------
    delivery_obj = []
    if not barter_only and not estimate and not phase and type_ == '0':
        delivery_obj = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('object__id', 'object__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id'))

    delivery_obj_ = []
    objectid = 0
    counter = -1
    for item in delivery_obj:
        if item['object__id'] != objectid:
            objectid = item['object__id']
            delivery_obj_.append({'object__id': objectid, 'total_sum': item['total_sum'],
                              'object__name': item['object__name']})
            counter += 1
        else:
            delivery_obj_[counter]['total_sum'] += item['total_sum']

    #print(delivery_obj_)
    # ------------------
    delivery_house = []
    if not barter_only and not estimate and not phase and type_ == '0':
        delivery_house = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('house__id', 'object__id', 'house__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id', 'house__id'))

    delivery_house_ = []
    houseid = 0
    counter = -1
    for item in delivery_house:
        if item['house__id'] != houseid:
            houseid = item['house__id']
            delivery_house_.append({'house__id': houseid, 'object__id': item['object__id'], 'total_sum': item['total_sum'],
                              'house__name': item['house__name']})
            counter += 1
        else:
            delivery_house_[counter]['total_sum'] += item['total_sum']

    #print('--->',delivery_house_)
    #for item in delivery_house_:
    #    if item['house__id'] == 214:
    #        print(item['object__id'], item['house__name'], item['total_sum'])

    # если пользователь выбрал опцию "только бетон"
    if concrete_only:
        data = []
        for item in delivery_obj_:
            data.append({'house__object__id': item['object__id'], 'house__object__name': item['object__name'], 'summary': item['total_sum']})

        prev = 0
        data2 = []
        data4 = []
        for item in delivery_house_:
            if item['house__id'] != prev:
                prev = item['house__id']
                data2.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'house__name': item['house__name'], 'summary': item['total_sum']})
                data4.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'estimate__name': 'Бетон', 'estimate__id': 0,
                          'summary': item['total_sum']})
            else:
                data2[len(data2) - 1]['summary'] += item['total_sum']

        summary_volume = (
            Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(summary=Sum('volume')))

        return data, data2, data4, summary_volume['summary']

    # если пользователь НЕ выбрал опцию "только бетон"

    data = []
    prev = 0
    for item in summary3:
        if item['house__object__id'] != prev:
            prev = item['house__object__id']
            data.append({'house__object__id': prev, 'house__object__name': item['house__object__name'], 'summary': item['summary']})
            # если не указана никакая смета, то добавляем сумму бетона к каждому объекту (если она есть)
            if not estimate:
                for obj in delivery_obj_:
                    if obj['object__id'] == item['house__object__id']:
                        data[len(data) - 1]['summary'] += obj['total_sum']
        else:
            data[len(data)-1]['summary'] += item['summary']

    data2 = []
    if not estimate or not phase or type_ == '0':
        # если не указана никакая смета, то здесь надо добавить объекты, по которым есть только бетон
        for obj in delivery_obj_:
            found = False
            for item in data:
                if item['house__object__id'] == obj['object__id']:
                    found = True
            if not found:
                data.append({'house__object__id': obj['object__id'], 'house__object__name': obj['object__name'], 'summary': obj['total_sum']})
                #data2.append({'house__object__id': obj['object__id'], 'house__object__name': obj['object__name'], 'summary': obj['total_sum']})

    prev = 0

    # собираем дома в кучу
    for item in details3:
        if item['house__id'] != prev:
            prev = item['house__id']
            data2.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'], 'house__name': item['house__name'], 'summary': item['summary']})
            # если не указана никакой фильтр по смете, то добавляем сумму бетона к каждому дому (если она есть)
            if not estimate:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data2[len(data2) - 1]['summary'] += obj['total_sum']
        else:
            data2[len(data2)-1]['summary'] += item['summary']
    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон
    if not estimate or not phase or type_ == '0':
        for house in delivery_house_:
            found = False
            for item in data2:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data2.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'house__name': house['house__name'], 'summary': house['total_sum']})

    data4 = []
    prev = -1
    house = 0

    #print(subdetails3)

    for item in subdetails3:
        if item['estimate__id'] != prev or item['house__id'] != house:

            # если не указана никакая смета, то добавляем сумму бетона как отдельную смету к каждому дому (если она есть)
            if not estimate and item['house__id'] != house:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'estimate__name': 'Бетон', 'estimate__id': 0, 'phase__id': 0,
                          'summary': obj['total_sum']})

            house = item['house__id']
            prev = item['estimate__id']
            data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'estimate__name': item['estimate__name'], 'estimate__id': item['estimate__id'], 'phase__id': item['phase__id'], 'summary': item['summary']})

        else:
            # информацию по бетону НЕ надо суммировать, остальные можно (и нужно)
            if data4[len(data4) - 1]['estimate__id'] != 0:
                data4[len(data4) - 1]['summary'] += item['summary']



    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон (чтобы отобразилась кнопка "Бетон")
    if not estimate or not phase or type_ == '0':
        for house in delivery_house_:
            found = False
            for item in data4:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data4.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'estimate__name': 'Бетон', 'estimate__id': 0, 'phase__id': 0,
                              'summary': house['total_sum']})
                #data2.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                #              'house__name': house['house__name'], 'summary': house['total_sum']})
    """
    #---------------------------------------------------------------------
    #print(len(subdetails3))
    #print(subdetails3)
    data3 = []
    temp = []
    previtem = {'house__id': 0}
    for item in subdetails3:
        #if item['house__object__id']==23: # and item['house__id']==136:
            #print('------------------------------------------>')
        #print(str(item['house__object__id'])+'---->'+str(item['house__id']))
        # тот же дом
        if item['house__id'] == previtem['house__id']:
            # добавляем строку по смете
            temp.append([item['estimate__id'], item['estimate__name'], item['summary']])
        # перешли к следующему дому
        else:
            # не первый дом в списке, надо сохранить в итоговый массив
            if previtem['house__id'] != 0:
                temp.sort()
                #print(str(item['house__object__id'])+'->'+str(item['house__id']))
                #print(temp)
                prev = 0
                for tempitem in temp:
                        if tempitem[0] != prev:
                            prev = tempitem[0]
                            data3.append(
                                {'house__object__id': previtem['house__object__id'],
                                 'house__id': previtem['house__id'],
                                 'estimate__id': previtem['estimate__id'],
                                 'estimate__name': tempitem[1], 'summary': tempitem[2]})
                        else:
                            data3[len(data3) - 1]['summary'] += tempitem[2]

                temp = []
                temp.append([item['estimate__id'], item['estimate__name'], item['summary']])
                previtem = item
            # перый дом
            else:
                previtem = item
                temp.append([item['estimate__id'], item['estimate__name'], item['summary']])
    """

    if estimate or phase or type_ != '0' or barter_only:
        summary_volume = {'summary': 0}
    else:
        summary_volume = (
            Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(
            summary=Sum('volume')))
    #if not barter_only or concrete_only or not estimate or not phase or type != '0':
    #    summary_volume = (
    #    Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(
    #        summary=Sum('volume')))
    #else:
    #    summary_volume = {'summary': 0}

    return data, data2, data4, summary_volume['summary']


def get_report_data3(datefrom, dateto, estimate, phase, type_, concrete_only, barter_only, closed_only, exclusion, special):
    start = time.time()

    objects_ = Object.objects.filter().order_by('-id')

    all_subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum('summary'))
    if special:
        all_subdetails2 = Content.objects.filter(deleted=False, bid__refunded=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum(F('quantity') * F('price')))
    else:
        all_subdetails2 = Content.objects.filter(deleted=False, bid__refunded=False, bid__deleted=False, bid__hidden=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__id', 'estimate__id', 'estimate__name', 'phase__id', 'phase__name', 'type').annotate(summary=Sum(F('quantity') * F('price')))
    if closed_only:
        all_subdetails2 = all_subdetails2.filter(bid__locked=True)
    if barter_only:
        all_subdetails1 = all_subdetails1.filter(cash='b')
        all_subdetails2 = all_subdetails2.filter(cash='b')
    if estimate:
        all_subdetails1 = all_subdetails1.filter(estimate__id=estimate.id)
        all_subdetails2 = all_subdetails2.filter(estimate__id=estimate.id)
    if phase:
        all_subdetails1 = all_subdetails1.filter(phase__id=phase)
        all_subdetails2 = all_subdetails2.filter(phase__id=phase)
    if type_ != '0':
        all_subdetails1 = all_subdetails1.filter(type=type_)
        all_subdetails2 = all_subdetails2.filter(type=type_)

    if exclusion == '1':
        all_subdetails1 = all_subdetails1.exclude(type='f', phase__id=6, estimate__id=84)
        all_subdetails2 = all_subdetails2.exclude(type='f', phase__id=6, estimate__id=84)

    subdetails3 = all_subdetails1.union(all_subdetails2, all=True).order_by('house__object__id', 'house__id', 'phase__id', 'estimate__id',  'type')

    all_details1 = all_subdetails1.values('house__object__id', 'house__id', 'house__name', 'summary')
    all_details2 = all_subdetails2.values('house__object__id', 'house__id', 'house__name', 'summary')
    details3 = all_details1.union(all_details2, all=True).order_by('house__object__id', 'house__id')

    all_summary1 = all_subdetails1.values('house__object__id', 'house__object__name', 'summary')
    all_summary2 = all_subdetails2.values('house__object__id', 'house__object__name', 'summary')
    summary3 = all_summary1.union(all_summary2, all=True).order_by('house__object__id')

    # ----------- если не выбрано никаких фильтров, то выбираем доставку бетона
    delivery_obj = []
    if not barter_only and not estimate and not phase and type_ == '0':
        delivery_obj = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('object__id', 'object__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id'))

    delivery_obj_ = []
    objectid = 0
    counter = -1
    for item in delivery_obj:
        if item['object__id'] != objectid:
            objectid = item['object__id']
            delivery_obj_.append({'object__id': objectid, 'total_sum': item['total_sum'],
                              'object__name': item['object__name']})
            counter += 1
        else:
            delivery_obj_[counter]['total_sum'] += item['total_sum']

    # ------------------
    delivery_house = []
    if not barter_only and not estimate and not phase and type_ == '0':
        delivery_house = (Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values('house__id', 'object__id', 'house__name').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F(
            'deliveryvolume')).order_by('object__id', 'house__id'))

    delivery_house_ = []
    houseid = 0
    counter = -1
    for item in delivery_house:
        if item['house__id'] != houseid:
            houseid = item['house__id']
            delivery_house_.append({'house__id': houseid, 'object__id': item['object__id'], 'total_sum': item['total_sum'],
                              'house__name': item['house__name']})
            counter += 1
        else:
            delivery_house_[counter]['total_sum'] += item['total_sum']

    # если пользователь выбрал опцию "только бетон"
    if concrete_only:
        data = []
        for item in delivery_obj_:
            data.append({'house__object__id': item['object__id'], 'house__object__name': item['object__name'], 'summary': item['total_sum']})

        prev = 0
        data2 = []
        data4 = []
        for item in delivery_house_:
            if item['house__id'] != prev:
                prev = item['house__id']
                data2.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'house__name': item['house__name'], 'summary': item['total_sum']})
                data4.append({'house__object__id': item['object__id'], 'house__id': item['house__id'],
                          'phase__name': 'Бетон', 'phase__id': 0,
                          'summary': item['total_sum']})
            else:
                data2[len(data2) - 1]['summary'] += item['total_sum']

        summary_volume = (
            Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(summary=Sum('volume')))

        return data, data2, data4, summary_volume['summary']

    # если пользователь НЕ выбрал опцию "только бетон"

    data = []
    prev = 0
    for item in summary3:
        if item['house__object__id'] != prev:
            prev = item['house__object__id']
            data.append({'house__object__id': prev, 'house__object__name': item['house__object__name'], 'summary': item['summary']})
            # если не указана никакая смета, то добавляем сумму бетона к каждому объекту (если она есть)
            if not estimate:
                for obj in delivery_obj_:
                    if obj['object__id'] == item['house__object__id']:
                        data[len(data) - 1]['summary'] += obj['total_sum']
        else:
            data[len(data)-1]['summary'] += item['summary']

    data2 = []
    if not estimate or not phase or type_ == '0':
        # если не указана никакая смета, то здесь надо добавить объекты, по которым есть только бетон
        for obj in delivery_obj_:
            found = False
            for item in data:
                if item['house__object__id'] == obj['object__id']:
                    found = True
            if not found:
                data.append({'house__object__id': obj['object__id'], 'house__object__name': obj['object__name'], 'summary': obj['total_sum']})

    prev = 0

    # собираем дома в кучу
    for item in details3:
        if item['house__id'] != prev:
            prev = item['house__id']
            data2.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'], 'house__name': item['house__name'], 'summary': item['summary']})
            # если не указан никакой фильтр по смете, то добавляем сумму бетона к каждому дому (если она есть)
            if not estimate:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data2[len(data2) - 1]['summary'] += obj['total_sum']
        else:
            data2[len(data2)-1]['summary'] += item['summary']
    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон
    if not estimate or not phase or type_ == '0':
        for house in delivery_house_:
            found = False
            for item in data2:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data2.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'house__name': house['house__name'], 'summary': house['total_sum']})

    data4 = []
    prev = -1
    house = 0

    for item in subdetails3:
        if item['phase__id'] != prev or item['house__id'] != house:

            # если не указана никакая смета, то добавляем сумму бетона как отдельную смету к каждому дому (если она есть)
            if not estimate and item['house__id'] != house:
                for obj in delivery_house_:
                    if obj['house__id'] == item['house__id']:
                        data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'phase__name': 'Бетон', 'phase__id': 0, 'estimate__id': 0,
                          'summary': obj['total_sum']})

            house = item['house__id']
            prev = item['phase__id']
            data4.append({'house__object__id': item['house__object__id'], 'house__id': item['house__id'],
                          'phase__name': item['phase__name'], 'phase__id': item['phase__id'], 'estimate__id': item['estimate__id'], 'summary': item['summary']})

        else:
            # информацию по бетону НЕ надо суммировать, остальные можно (и нужно)
            if data4[len(data4) - 1]['phase__id'] != 0:
                data4[len(data4) - 1]['summary'] += item['summary']



    # если не указана никакая смета, то здесь надо добавить дома, по которым есть только бетон (чтобы отобразилась кнопка "Бетон")
    if not estimate or not phase or type_ == '0':
        for house in delivery_house_:
            found = False
            for item in data4:
                if item['house__id'] == house['house__id']:
                    found = True
            if not found:
                data4.append({'house__object__id': house['object__id'], 'house__id': house['house__id'],
                              'phase__name': 'Бетон', 'phase__id': 0, 'estimate__id': 0,
                              'summary': house['total_sum']})

    if estimate or phase or type_ != '0' or barter_only:
        summary_volume = {'summary': 0}
    else:
        summary_volume = (
            Delivery.objects.filter(deleted=False, date__gte=datefrom, date__lte=dateto).values().aggregate(summary=Sum('volume')))

    #print('Time --: ', time.time() - start)
    return data, data2, data4, summary_volume['summary']


@login_required
def view_test(request):
    DateFrom = None
    DateTo = None
    context = None
    is_manager = request.user.groups.filter(name='managers').exists()
    if not is_manager:
        raise Http404

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            #print('!!!!!!!!!')
            cd = form.cleaned_data
            #print('!!!!!!!!!')
            data, data2, data4 = get_report_data(cd['datefrom'], cd['dateto'])
            #form = ReportForm()
            context = {
                'form': form,
                'title': 'Отчёт',
                'objects': data,
                'details': data2,
                'subdetails': data4
            }
            return render(request, 'project/report.html', context)
    else:
        form = ReportForm()
        if 'submitted' in request.GET:
            DateFrom = form.cleaned_data['datefrom']
            #print('$$$$')
            #print(form.cleaned_data)
            data, data2, data4 = get_report_data(form.cleaned_data['datefrom'], form.cleaned_data['dateto'])
            context = {
                'form': form,
                'title': 'Отчёт',
                'objects': data,
                'details': data2,
                'subdetails': data4
            }



    #form = ReportForm()

    #data, data2, data4 = get_report_data(None, None)
    # ---------------------------------------------------------------------



    return render(request, 'project/report.html', context)


def CorrectDate(date):
    #format = "%Y-%m-d"
    format = "%Y-%m-%d"
    if date is None:
        return False
    try:
        datetime.datetime.strptime(date, format)
        return True
    except ValueError:
        return False


@login_required
def report_old(request):
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    concrete_only = False
    barter_only = False
    date_from = None
    date_to = None
    estimate_ = None
    estimate = None
    phase = None
    date_from_str = ''
    date_to_str = ''
    estimate_str = ''
    data, data2, data4 = None, None, None
    summary, summary_volume = 0,0

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #print(cd['testdate'])
            estimate = cd['estimate']
            if estimate:
                estimate_id = estimate.id
            else:
                estimate_id = 0
            phase = cd['phase']
            if phase:
                phase_id = phase.id
            else:
                phase_id = 0
            concrete_only = cd['concrete_only']
            barter_only = cd['barter_only']

            return HttpResponseRedirect(reverse('project:report')+'?from=' + str(cd['datefrom'])+'&to='+ str(cd['dateto'])+'&e='+ str(estimate_id)+'&p='+ str(phase_id)+'&c='+str(concrete_only)+'&b='+str(barter_only))
    else:
        if 'b' in request.GET:
            barter_only_str = request.GET.get('b', 'False')
            if barter_only_str == 'True':
                barter_only = True
            else:
                barter_only = False
        if 'c' in request.GET:
            concrete_only_str = request.GET.get('c', 'False')
            if concrete_only_str == 'True':
                concrete_only = True
            else:
                concrete_only = False
        if 'e' in request.GET:
            estimate_str = request.GET.get('e', None)
            try:
                estimate_ = int(estimate_str)
                estimate = Estimate.objects.get(id=estimate_)
            except:
                estimate_ = 0
                estimate = None
        if 'p' in request.GET:
            phase_str = request.GET.get('p', None)
            try:
                phase_ = int(phase_str)
                phase = Phase.objects.get(id=phase_)
            except:
                phase_ = 0
                phase = None

        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)

            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = datetime.date(2020, 1, 1)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")

            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = datetime.date(2024, 12, 31)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

            #print(date_from)
            #print(date_to)

            data, data2, data4, summary_volume = get_report_data(date_from, date_to, estimate, phase, concrete_only, barter_only)
            date_from_str = date_from.strftime("%Y-%m-%d")
            date_to_str = date_to.strftime("%Y-%m-%d")

            for item in data:
                summary += item['summary']

            #print('---------------->', summary_volume)

        form = ReportForm(initial={'datefrom': date_from, 'dateto': date_to, 'estimate': estimate, 'phase': phase, 'concrete_only': concrete_only, 'barter_only': barter_only})
    return render(request, 'project/report.html', {'form': form, 'title': 'Отчёт',
                                                 'datefrom_': date_from_str,
                                                 'dateto_': date_to_str,
                                                 'objects': data,
                                                 'details': data2,
                                                 'subdetails': data4,
                                                 'summary': summary,
                                                 'barter_only': barter_only,
                                                 'summary_volume': summary_volume})


@login_required
def report(request):
    is_manager = request.user.groups.filter(name='managers').exists()

    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    exclusion = '0'
    exclusion_ = '0'
    concrete_only = False
    barter_only = False
    date_from = None
    date_to = None
    estimate_ = None
    estimate = None
    phase_ = None
    phase = None
    type_ = None
    date_from_str = ''
    date_to_str = ''
    estimate_str = ''
    data, data2, data4 = None, None, None
    summary, summary_volume = 0,0

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #print(cd['testdate'])
            estimate = cd['estimate']
            if estimate:
                estimate_id = estimate.id
            else:
                estimate_id = 0
            phase = cd['phase']
            if phase:
                phase_id = phase.id
            else:
                phase_id = 0
            type_ = cd['type_']
            #if type_ == '0':
             #   type_ = 'None'
            concrete_only = cd['concrete_only']
            barter_only = cd['barter_only']

            exclusion = cd['exclusion']

            return HttpResponseRedirect(reverse('project:report')+'?from=' + str(cd['datefrom'])+'&to='+ str(cd['dateto'])+'&e='+ str(estimate_id)+'&p='+ str(phase_id)+'&t='+ str(type_)+'&c='+str(concrete_only)+'&b='+str(barter_only)+'&x='+str(exclusion))
    else:
        if 'b' in request.GET:
            barter_only_str = request.GET.get('b', 'False')
            if barter_only_str == 'True':
                barter_only = True
            else:
                barter_only = False
        if 'c' in request.GET:
            concrete_only_str = request.GET.get('c', 'False')
            if concrete_only_str == 'True':
                concrete_only = True
            else:
                concrete_only = False
        if 'e' in request.GET:
            estimate_str = request.GET.get('e', None)
            try:
                estimate_ = int(estimate_str)
                estimate = Estimate.objects.get(id=estimate_)
            except:
                estimate_ = 0
                estimate = None
        if 'p' in request.GET:
            phase_str = request.GET.get('p', None)
            try:
                phase_ = int(phase_str)
                phase = Phase.objects.get(id=phase_)
            except:
                phase_ = 0
                phase = None
        if 't' in request.GET:
            type_ = request.GET.get('t', '0')

        if 'x' in request.GET:
            exclusion_ = request.GET.get('x', '0')

        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)

            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = datetime.date(2020, 1, 1)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")

            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = datetime.date(2024, 12, 31)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

            #print(date_from)
            #print(date_to)

            data, data2, data4, summary_volume = get_report_data2(date_from, date_to, estimate, phase_, type_, concrete_only, barter_only, exclusion_, is_special)
            date_from_str = date_from.strftime("%Y-%m-%d")
            date_to_str = date_to.strftime("%Y-%m-%d")

            for item in data:
                summary += item['summary']

            #print('---------------->', phase)

        form = ReportForm(initial={'datefrom': date_from, 'dateto': date_to, 'estimate': estimate, 'phase': phase, 'type_': type_, 'concrete_only': concrete_only, 'barter_only': barter_only, 'exclusion': exclusion_})
    return render(request, 'project/report.html', {'form': form, 'title': 'Отчёт',
                                                 'datefrom_': date_from_str,
                                                 'dateto_': date_to_str,
                                                 'objects': data,
                                                 'details': data2,
                                                 'subdetails': data4,
                                                 'summary': summary,
                                                 'phase': phase_,
                                                 'type_': type_,
                                                 'barter_only': barter_only,
                                                 'exclusion': exclusion_,
                                                 'summary_volume': summary_volume})


@login_required
def phase_report(request):
    start = time.time()
    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    exclusion = '0'
    exclusion_ = '0'
    concrete_only = False
    barter_only = False
    closed_only = False
    date_from = None
    date_to = None
    estimate_ = None
    estimate = None
    phase_ = None
    phase = None
    type_ = None
    date_from_str = ''
    date_to_str = ''
    estimate_str = ''
    data, data2, data4 = None, None, None
    summary, summary_volume = 0,0
    selected_object = 0
    selected_house = 0

    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            #print(cd['testdate'])
            estimate = cd['estimate']
            if estimate:
                estimate_id = estimate.id
            else:
                estimate_id = 0
            phase = cd['phase']
            if phase:
                phase_id = phase.id
            else:
                phase_id = 0
            type_ = cd['type_']
            #if type_ == '0':
             #   type_ = 'None'
            concrete_only = cd['concrete_only']
            barter_only = cd['barter_only']
            closed_only = cd['closed_only']

            exclusion = cd['exclusion']

            return HttpResponseRedirect(reverse('project:phasereport')+'?from=' + str(cd['datefrom'])+'&to='+ str(cd['dateto'])+'&e='+ str(estimate_id)+'&p='+ str(phase_id)+'&t='+ str(type_)+'&c='+str(concrete_only)+'&b='+str(barter_only)+'&d='+str(closed_only)+'&x='+str(exclusion))
    else:
        if 'd' in request.GET:
            closed_only_str = request.GET.get('d', 'False')
            if closed_only_str == 'True':
                closed_only = True
            else:
                closed_only = False
        if 'b' in request.GET:
            barter_only_str = request.GET.get('b', 'False')
            if barter_only_str == 'True':
                barter_only = True
            else:
                barter_only = False
        if 'c' in request.GET:
            concrete_only_str = request.GET.get('c', 'False')
            if concrete_only_str == 'True':
                concrete_only = True
            else:
                concrete_only = False
        if 'e' in request.GET:
            estimate_str = request.GET.get('e', None)
            try:
                estimate_ = int(estimate_str)
                estimate = Estimate.objects.get(id=estimate_)
            except:
                estimate_ = 0
                estimate = None
        if 'p' in request.GET:
            phase_str = request.GET.get('p', None)
            try:
                phase_ = int(phase_str)
                phase = Phase.objects.get(id=phase_)
            except:
                phase_ = 0
                phase = None
        if 't' in request.GET:
            type_ = request.GET.get('t', '0')

        if 'x' in request.GET:
            exclusion_ = request.GET.get('x', '0')
        if 'o' in request.GET:
            selected_object_str = request.GET.get('o', None)
            try:
                selected_object = int(selected_object_str)
            except:
                selected_object = 0
        if 'h' in request.GET:
            selected_house_str = request.GET.get('h', None)
            try:
                selected_house = int(selected_house_str)
            except:
                selected_house = 0
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)

            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = datetime.date(2020, 1, 1)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")

            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = datetime.date(2024, 12, 31)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

            #print(date_from)
            #print(date_to)

            data, data2, data4, summary_volume = get_report_data3(date_from, date_to, estimate, phase_, type_, concrete_only, barter_only, closed_only, exclusion_, is_special)
            date_from_str = date_from.strftime("%Y-%m-%d")
            date_to_str = date_to.strftime("%Y-%m-%d")

            for item in data:
                summary += item['summary']

        #print('Time calculation: ', time.time() - start)

        form = ReportForm(initial={'datefrom': date_from, 'dateto': date_to, 'estimate': estimate, 'phase': phase, 'type_': type_, 'concrete_only': concrete_only, 'barter_only': barter_only, 'closed_only': closed_only, 'exclusion': exclusion_})

    #print(data2)
    start = time.time()
    rnd = render(request, 'project/phasereport.html', {'form': form, 'title': 'Отчёт',
                                                 'datefrom_': date_from_str,
                                                 'dateto_': date_to_str,
                                                 'objects': data,
                                                 'details': data2,
                                                 'subdetails': data4,
                                                 'summary': summary,
                                                 'estimate': estimate_,
                                                 'phase': phase,
                                                 'type_': type_,
                                                 'concrete_only': concrete_only,
                                                 'closed_only': closed_only,
                                                 'barter_only': barter_only,
                                                 'exclusion': exclusion_,
                                                 'selected_object': selected_object,
                                                 'selected_house': selected_house,
                                                 'summary_volume': summary_volume})
    #print('Time render: ', time.time() - start)

    return rnd

def YesNoAnswer(flag):
    if flag: return "Да"
    else: return "Нет"

def Print2xls(worksheet, row, data):
    for i, item in enumerate(data):
        worksheet.write(row, i, item)

@login_required
def bids_export(request):
    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    date_from = None
    date_to = None
    date_from_str = ''
    date_to_str = ''
    object_id = 0
    house_id = 0
    concrete = 0

    if request.method == 'POST':
        form = ExportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            scope = cd['like']
            object_ = cd['object']
            house_ = cd['house']
            concrete_too = cd['concrete_included']
            out_str = '?scope='+scope
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)
            if object_:
                out_str += '&o=' + str(object_.id)
            if house_:
                out_str += '&h=' + str(house_.id)
            if concrete_too:
                out_str += '&c=1'
            else:
                out_str += '&c=0'

            return HttpResponseRedirect(reverse('project:bidsexport') + out_str)
    else:
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = None
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = None

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = None
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d") + datetime.timedelta(days=1)
        else:
            date_to = None

        if 'o' in request.GET:
            try:
                object_ = request.GET.get('o', 0)
                object_id = int(object_)
            except:
                object_id = 0
        if 'h' in request.GET:
            try:
                house_ = request.GET.get('h', 0)
                house_id = int(house_)
            except:
                house_id = 0

        if 'c' in request.GET:
            try:
                concrete_ = request.GET.get('c', 0)
                concrete = int(concrete_)
            except:
                concrete = 1

        if 'scope' in request.GET:
            scope = request.GET.get('scope', 'option1')
            if scope == 'option2':
                date_option = False
            else:
                date_option = True

            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer)
            worksheet = workbook.add_worksheet()

            cell_format_yellow = workbook.add_format({
                'bold': 0,
                'border': 0,
                'align': 'left',
                'valign': 'vbottom',
                'fg_color': '#B5DEDB',
                'color': 'black',
                'font_size': 10,
                'text_wrap': False})

            if date_option:
                if is_special:
                    mybids = Bid.objects.filter(deleted=False).order_by('-date')
                else:
                    mybids = Bid.objects.filter(deleted=False, hidden=False).order_by('-date')
                myarchive = Archive.objects.filter(deleted=False).order_by('-date')
                concretedelivery = Delivery.objects.filter(deleted=False).order_by('-date')

                if date_from:
                    mybids = mybids.filter(date__gte=date_from)
                    myarchive = myarchive.filter(date__gte=date_from)
                    concretedelivery = concretedelivery.filter(date__gte=date_from)
                if date_to:
                    mybids = mybids.filter(date__lt=date_to)
                    myarchive = myarchive.filter(date__lt=date_to)
                    concretedelivery = concretedelivery.filter(date__lt=date_to)
                if object_id != 0:
                    mybids = mybids.filter(object_id=object_id)
                    myarchive = myarchive.filter(object_id=object_id)
                    concretedelivery = concretedelivery.filter(object_id=object_id)
                if house_id != 0:
                    concretedelivery = concretedelivery.filter(house_id=house_id)

                header = ['№ заявки', 'Дата заявки', 'Описание', 'Объект', 'Исполнитель', 'Дата работ/поставки', '№ дома', 'Примечание', 'Вид расходов', 'нал/безнал', 'Кол-во', 'Стоимость', 'Сумма', 'Ед. изм', 'Поставщик', 'Этап', 'Смета', 'Комментарий', 'Заблокирована', 'Подпись прораба', 'Подпись технадзора', 'Подписал', 'Оформлен возврат']
                for i, h in enumerate(header):
                    worksheet.write(0, i, h)
                row = 1
                counter = 0
                for item in mybids:
                    if concrete == 1:
                        while counter < len(concretedelivery) and concretedelivery[counter].date > item.date:
                            Print2xls(worksheet, row, ["", "", "", concretedelivery[counter].object.name,
                                                  concretedelivery[counter].owner.username, concretedelivery[counter].date.strftime(("%d.%m.%Y")), concretedelivery[counter].house.name, "",
                                                  "Бетон", "", concretedelivery[counter].volume, "",
                                                  concretedelivery[counter].price * concretedelivery[counter].volume + concretedelivery[counter].pumpsummary + concretedelivery[counter].pumptransfer + concretedelivery[counter].downtime * concretedelivery[counter].downtimecost + concretedelivery[counter].deliveryprice * concretedelivery[counter].deliveryvolume, "", '['+str(concretedelivery[counter].supplier.id)+']' + concretedelivery[counter].supplier.name,
                                                  "", "", concretedelivery[counter].comment, "",
                                                  "", "", "", ""])
                            row += 1
                            counter += 1

                    if house_id != 0:
                        content = item.content_set.filter(deleted=False, house_id=house_id)
                    else:
                        content = item.content_set.filter(deleted=False)
                    for cnt in content:
                        if item.supervisor == '-':
                            supervision = 'Нет'
                        else:
                            supervision = YesNoAnswer(item.supervision)

                        Print2xls(worksheet, row, [item.number, item.date.strftime(("%d.%m.%Y")), item.title, item.object.name,
                                                   item.owner.username, cnt.date.strftime(("%d.%m.%Y")), cnt.house.name, cnt.title,
                                                   cnt.get_type_display(), cnt.get_cash_display(), cnt.quantity, cnt.price,
                                                   cnt.price * cnt.quantity, cnt.get_measure_display(), '['+str(cnt.supplier.id)+']' + cnt.supplier.name,
                                                   cnt.phase.name, cnt.estimate.name, cnt.comment, YesNoAnswer(item.locked),
                                                   YesNoAnswer(item.highlighted), supervision, item.supervisor, YesNoAnswer(item.refunded)])
                        row += 1

                if concrete == 1:
                    while counter < len(concretedelivery):
                        Print2xls(worksheet, row, ["", "", "",
                                                   concretedelivery[counter].object.name,
                                                   concretedelivery[counter].owner.username, concretedelivery[counter].date.strftime(("%d.%m.%Y")),
                                                   concretedelivery[counter].house.name, "",
                                                   "Бетон", "", concretedelivery[counter].volume, "",
                                                   concretedelivery[counter].price * concretedelivery[counter].volume +
                                                   concretedelivery[counter].pumpsummary + concretedelivery[
                                                       counter].deliveryprice * concretedelivery[
                                                       counter].deliveryvolume + concretedelivery[counter].pumptransfer + concretedelivery[counter].downtime * concretedelivery[counter].downtimecost, "",
                                                   '[' + str(concretedelivery[counter].supplier.id) + ']' +
                                                   concretedelivery[counter].supplier.name,
                                                   "", "", concretedelivery[counter].comment, "",
                                                   "", "", "", ""])
                        row += 1
                        counter += 1

                for item in myarchive:
                    if house_id != 0:
                        archivedetail = item.archivedetail_set.filter(deleted=False, house_id=house_id)
                    else:
                        archivedetail = item.archivedetail_set.filter(deleted=False)
                    for cnt in archivedetail:
                        Print2xls(worksheet, row, ['(а)' + item.number, item.date.strftime(("%d.%m.%Y")), item.title, item.object.name,
                                                   item.owner.username, cnt.date.strftime(("%d.%m.%Y")), cnt.house.name, cnt.title,
                                                   cnt.get_type_display(), cnt.get_cash_display(), "", "",
                                                   cnt.summary, cnt.measure, '['+str(cnt.new_supplier.id)+']' + cnt.new_supplier.name,
                                                   cnt.phase.name, cnt.estimate.name, cnt.comment, "Да", "Нет", "Нет", "", "", ""])
                        row += 1
            else:
                if is_special:
                    mycontent = Content.objects.filter(deleted=False, bid__deleted=False).order_by('-bid__date')
                else:
                    mycontent = Content.objects.filter(deleted=False, bid__deleted=False, bid__hidden=False).order_by('-bid__date')
                myarchive = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False).order_by('-archive__date')
                concretedelivery = Delivery.objects.filter(deleted=False).order_by('-date')
                if date_from:
                    mycontent = mycontent.filter(date__gte=date_from)
                    myarchive = myarchive.filter(date__gte=date_from)
                    concretedelivery = concretedelivery.filter(date__gte=date_from)
                if date_to:
                    mycontent = mycontent.filter(date__lt=date_to)
                    myarchive = myarchive.filter(date__lt=date_to)
                    concretedelivery = concretedelivery.filter(date__lt=date_to)
                if object_id != 0:
                    mycontent = mycontent.filter(bid__object_id=object_id)
                    myarchive = myarchive.filter(archive__object_id=object_id)
                    concretedelivery = concretedelivery.filter(object_id=object_id)
                if house_id != 0:
                    mycontent = mycontent.filter(house_id=house_id)
                    myarchive = myarchive.filter(house_id=house_id)
                    concretedelivery = concretedelivery.filter(house_id=house_id)

                header = ['№ заявки', 'Дата заявки', 'Описание', 'Объект', 'Исполнитель', 'Дата работ/поставки', '№ дома', 'Примечание', 'Вид расходов', 'нал/безнал', 'Кол-во', 'Стоимость', 'Сумма', 'Ед. изм', 'Поставщик', 'Этап', 'Смета', 'Комментарий', 'Заблокирована', 'Подпись прораба', 'Подпись технадзора', 'Подписал', 'Оформлен возврат']
                for i, h in enumerate(header):
                    worksheet.write(0, i, h)
                row = 1
                counter = 0
                for item in mycontent:
                    if concrete == 1:
                        while counter < len(concretedelivery) and concretedelivery[counter].date > item.bid.date:
                            Print2xls(worksheet, row, ["", "", "", concretedelivery[counter].object.name,
                                                  concretedelivery[counter].owner.username, concretedelivery[counter].date.strftime(("%d.%m.%Y")), concretedelivery[counter].house.name, "",
                                                  "Бетон", "", concretedelivery[counter].volume, "",
                                                  concretedelivery[counter].price * concretedelivery[counter].volume + concretedelivery[counter].pumpsummary + concretedelivery[counter].deliveryprice * concretedelivery[counter].deliveryvolume + concretedelivery[counter].pumptransfer + concretedelivery[counter].downtime * concretedelivery[counter].downtimecost, "", '['+str(concretedelivery[counter].supplier.id)+']' + concretedelivery[counter].supplier.name,
                                                  "", "", concretedelivery[counter].comment, "",
                                                  "", "", "", ""])
                            row += 1
                            counter += 1

                    if item.bid.supervisor == '-':
                        supervision = 'Нет'
                    else:
                        supervision = YesNoAnswer(item.bid.supervision)

                    Print2xls(worksheet, row, [item.bid.number, item.bid.date.strftime(("%d.%m.%Y")), item.bid.title, item.bid.object.name,
                                                   item.bid.owner.username, item.date.strftime(("%d.%m.%Y")), item.house.name, item.title,
                                                   item.get_type_display(), item.get_cash_display(), item.quantity, item.price,
                                                   item.price * item.quantity, item.get_measure_display(), '['+str(item.supplier.id)+']' + item.supplier.name,
                                                   item.phase.name, item.estimate.name, item.comment, YesNoAnswer(item.bid.locked),
                                                   YesNoAnswer(item.bid.highlighted), supervision, item.bid.supervisor, YesNoAnswer(item.bid.refunded)])
                    row += 1

                if concrete == 1:
                    while counter < len(concretedelivery):
                        Print2xls(worksheet, row, ["", "", "",
                                                   concretedelivery[counter].object.name,
                                                   concretedelivery[counter].owner.username, concretedelivery[counter].date.strftime(("%d.%m.%Y")),
                                                   concretedelivery[counter].house.name, "",
                                                   "Бетон", "", concretedelivery[counter].volume, "",
                                                   concretedelivery[counter].price * concretedelivery[counter].volume +
                                                   concretedelivery[counter].pumpsummary + concretedelivery[
                                                       counter].deliveryprice * concretedelivery[
                                                       counter].deliveryvolume + concretedelivery[counter].pumptransfer + concretedelivery[counter].downtime * concretedelivery[counter].downtimecost, "",
                                                   '[' + str(concretedelivery[counter].supplier.id) + ']' +
                                                   concretedelivery[counter].supplier.name,
                                                   "", "", concretedelivery[counter].comment, "",
                                                   "", "", "", ""])
                        row += 1
                        counter += 1

                for item in myarchive:
                        Print2xls(worksheet, row, ['(а)' + item.archive.number, item.archive.date.strftime(("%d.%m.%Y")), item.archive.title, item.archive.object.name,
                                                   item.archive.owner.username, item.date.strftime(("%d.%m.%Y")), item.house.name, item.title,
                                                   item.get_type_display(), item.get_cash_display(), "", "",
                                                   item.summary, item.measure, '['+str(item.new_supplier.id)+']' + item.new_supplier.name,
                                                   item.phase.name, item.estimate.name, item.comment, "Да", "Нет", "Нет", "", ""])
                        row += 1

            workbook.close()
            buffer.seek(0)
            filename = 'report23.xlsx'
            response = HttpResponse(
                buffer,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response
        else:
            form = ExportForm(initial={'datefrom': date_from, 'dateto': date_to, 'like': 'option1', 'object': object_id, 'house': house_id, 'concrete_included': 0})
            return render(request, 'project/bidsexport.html', {'form': form, 'title': 'Выгрузка данных',
                                'datefrom_': date_from_str,
                                'dateto_': date_to_str})


@login_required
def contracts_export(request):
    is_boss = request.user.groups.filter(name='bosses').exists()

    if not is_boss:
        raise Http404

    date_from = None
    date_to = None
    date_from_str = ''
    date_to_str = ''

    if request.method == 'POST':
        form = ContractsExportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            out_str = '?data=all'
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)

            return HttpResponseRedirect(reverse('project:contractsexport') + out_str)
    else:
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = None
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = None

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = None
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d") + datetime.timedelta(days=1)
        else:
            date_to = None

        if 'data' in request.GET:
            buffer = io.BytesIO()
            workbook = xlsxwriter.Workbook(buffer)
            worksheet = workbook.add_worksheet()

            cell_format_yellow = workbook.add_format({
                'bold': 0,
                'border': 0,
                'align': 'left',
                'valign': 'vbottom',
                'fg_color': '#B5DEDB',
                'color': 'black',
                'font_size': 10,
                'text_wrap': False,
                'num_format': '#,##0.00'})

            if True:

                mycontracts = Contract.objects.filter(deleted=False).order_by('-date') #extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')

                if date_from:
                    mycontracts = mycontracts.filter(date__gte=date_from)
                if date_to:
                    mycontracts = mycontracts.filter(date__lt=date_to)

                datenow = datetime.datetime.now()

                header = ['Cтатус', 'Тип договора', '№ договора', 'Дата', 'Описание', 'Объект', 'Дом', 'Кв', 'Площадь', 'Клиент', 'Телефон',
                          'Агентство', 'Телефон', 'Цена по шахматке', 'Скидка АН', 'Скидка застройщика',
                          'Расчет комиссии экс', 'Сумма комиссии экс', 'Расчет комиссии АН', 'Сумма комиссии АН',
                          'Всего комиссии', 'На руки застройщику', 'Стоимость за м2', 'ДЗ',
                          'Всего поступило', 'Всего выплачено',
                          'Рассрочка', 'Чек', 'Оригинал', 'Бронь', 'Дата брони', 'Аннулирован', 'Комментарий', 'Исполнитель']
                for i, h in enumerate(header):
                    worksheet.write(0, i, h)
                row = 1
                for item in mycontracts:
                        worksheet.write(row, 0, item.get_status_display())
                        worksheet.write(row, 1, item.get_type_display())
                        worksheet.write(row, 2, item.number)
                        worksheet.write(row, 3, item.date.strftime(("%d.%m.%Y")))
                        worksheet.write(row, 4, item.title)
                        worksheet.write(row, 5, item.object.name)
                        worksheet.write(row, 6, item.house.name)
                        worksheet.write(row, 7, item.apartment)
                        worksheet.write(row, 8, item.square)
                        worksheet.write(row, 9, item.client)
                        worksheet.write(row, 10, item.clientphone)
                        worksheet.write(row, 11, item.agency)
                        worksheet.write(row, 12, item.agencyphone)
                        worksheet.write(row, 13, item.price)
                        worksheet.write(row, 14, item.agency_discount)
                        worksheet.write(row, 15, item.developer_discount)
                        worksheet.write(row, 16, item.seller_commission_calc)
                        worksheet.write(row, 17, item.seller_commission)
                        worksheet.write(row, 18, item.agency_commission_calc)
                        worksheet.write(row, 19, item.agency_commission)

                        worksheet.write(row, 20, item.agency_commission + item.seller_commission)
                        worksheet.write(row, 21, item.price - item.agency_discount - item.developer_discount - item.agency_commission - item.seller_commission)
                        worksheet.write(row, 22, round((item.price - item.agency_discount - item.developer_discount - item.agency_commission - item.seller_commission) / item.square, 2), cell_format_yellow)

                        totalebt = item.turnover_set.filter(deleted=False, performed=False,
                                                           type__lt=100, date__lte=datenow).aggregate(summary=Sum('amount'))['summary']

                        worksheet.write(row, 23, totalebt)

                        income = item.turnover_set.filter(deleted=False, performed=True, type__lt=100).aggregate(
                            summary=Sum('amount'))['summary']
                        paid = item.turnover_set.filter(deleted=False, performed=True, type__gte=100).aggregate(
                            summary=Sum('amount'))['summary']


                        worksheet.write(row, 24, income)
                        worksheet.write(row, 25, paid)

                        worksheet.write(row, 26, item.installment)
                        if item.receipt:
                            worksheet.write(row, 27, "Да")
                        else:
                            worksheet.write(row, 27, "Нет")
                        if item.onhand:
                            worksheet.write(row, 28, "Да")
                        else:
                            worksheet.write(row, 28, "Нет")
                        worksheet.write(row, 29, item.get_reservation_type_display())
                        if item.reservation_date:
                            worksheet.write(row, 30, item.reservation_date.strftime(("%d.%m.%Y")))
                        if item.revoked:
                            worksheet.write(row, 31, "Да")
                            worksheet.write(row, 32, item.comment)
                        else:
                            worksheet.write(row, 31, "Нет")

                        worksheet.write(row, 33, item.owner.username)
                        row += 1

            workbook.close()
            buffer.seek(0)
            filename = 'contracts.xlsx'
            response = HttpResponse(
                buffer,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response
        else:
            form = ContractsExportForm(initial={'datefrom': date_from, 'dateto': date_to})
            return render(request, 'project/contractsexport.html', {'form': form, 'title': 'Выгрузка данных',
                                'datefrom_': date_from_str,
                                'dateto_': date_to_str})


@login_required
def supplier_report(request):
    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    date_from = None
    date_to = None
    filtered_supplier = None
    supplier = None
    date_from_str = ''
    date_to_str = ''
    #data, data2, data4 = None, None, None
    details = []
    error = ''

    if request.method == 'POST':
        form = SupplierReportForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            out_str = '?page=1'
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)

            supplier = cd['filter_supplier']
            if supplier is None:
                out_str += '&s=0'
            else:
                out_str += '&s=' + str(supplier.id)
            return HttpResponseRedirect(reverse('project:supplierreport') + out_str)
    else:
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = datetime.date(2020, 1, 1)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = datetime.date(2020, 1, 1)

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = datetime.date(2024, 12, 31)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
        else:
            date_to = datetime.date(2024, 12, 31)

        if 's' in request.GET:
            filtered_supplier_str = request.GET.get('s', 0)
            try:
                filtered_supplier = int(filtered_supplier_str)
            except:
                filtered_supplier = 0
        else:
            filtered_supplier = 0

        if 'e' in request.GET:
            error = request.GET.get('e', '0')
            if error == '1':
                error = 'Ошибка переназначения поставщика!'


        if filtered_supplier > 0:
            supplier_name = Supplier.objects.filter(id=filtered_supplier).order_by('id')
            if supplier_name:
                subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=date_from,
                                                           date__lte=date_to, new_supplier__id=filtered_supplier).values(
                    s=F('new_supplier_id'), f=F('new_supplier_id__name')).annotate(summary=Sum('summary'), cnt=Count('new_supplier_id'))
                subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=date_from,
                                                     date__lte=date_to, supplier__id=filtered_supplier).values(s=F('supplier_id'),
                                                                               f=F('supplier_id__name')).annotate(
                    summary=Sum(F('quantity') * F('price')), cnt=Count('supplier_id'))
                if not is_special:
                    subdetails2 = subdetails2.exclude(bid__hidden=True)

                concrete_delivery = Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier) \
                    .values(s=F('supplier_id'), f=F('supplier_id__name')) \
                    .annotate(total_sum=Sum(
                    F('price') * F('volume') + F('pumpsummary') + F('deliveryprice') * F('deliveryvolume') + F('pumptransfer') + F('downtime') * F('downtimecost')), cnt=Count('supplier_id'))

                concrete_payments = Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier) \
                    .values(s=F('supplier_id'), f=F('supplier_id__name')) \
                    .annotate(total_sum=-1 * Sum(F('summary')), cnt=Count('supplier_id'))

            else:
                print('not found')
        else:
            subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=date_from, date__lte=date_to).values(
                s=F('new_supplier_id'), f=F('new_supplier_id__name')).annotate(summary=Sum('summary'), cnt=Count('new_supplier_id'))
            subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=date_from,
                                                 date__lte=date_to).values(s=F('supplier_id'), f=F('supplier_id__name')).annotate(summary=Sum(F('quantity') * F('price')), cnt=Count('supplier_id'))
            if not is_special:
                subdetails2 = subdetails2.exclude(bid__hidden=True)

            concrete_delivery = Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to)\
                .values(s=F('supplier_id'), f=F('supplier_id__name')) \
                .annotate(summary=Sum(F('price') * F('volume') + F('pumpsummary') + F('deliveryprice') * F('deliveryvolume') + F('pumptransfer') + F('downtime') * F('downtimecost')), cnt=Count('supplier_id'))

            concrete_payments = Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to)\
                .values(s=F('supplier_id'), f=F('supplier_id__name')) \
                .annotate(summary=-1 * Sum(F('summary')), cnt=Count('supplier_id'))

        subdetails3 = subdetails1.union(subdetails2, concrete_delivery, concrete_payments, all=True).order_by('s')

        #print(subdetails3)

            #print("------------------------------------------")
        if True:

            details = []
            id = 0
            counter = -1
            for item in subdetails3:
                if item['s'] != id:
                    id = item['s']
                    if item['summary'] < 0:
                        item['prepayment'] = item['summary']
                        item['summary'] = 0.0
                    else:
                        item['prepayment'] = 0.0
                    item['count'] = item['cnt']
                    details.append(item)
                    counter += 1
                else:
                    # поступление/реализация
                    if item['summary'] > 0:
                        details[counter]['summary'] += item['summary']
                    else:
                        details[counter]['prepayment'] = item['summary']
                    details[counter]['count'] += item['cnt']
            #print(details)

        date_from_str = date_from.strftime("%Y-%m-%d")
        date_to_str = date_to.strftime("%Y-%m-%d")


        form = SupplierReportForm(initial={'datefrom': date_from, 'dateto': date_to, 'filter_supplier': filtered_supplier})
    return render(request, 'project/supplierreport.html', {'form': form, 'title': 'Отчёт по поставщикам',
                                                 'datefrom_': date_from_str,
                                                 'dateto_': date_to_str,
                                                 'details': details,
                                                 'filter_supplier': filtered_supplier,
                                                 'error': error
                                                           })


def get_supplier_details(date_from, date_to, filtered_supplier, is_special):
    supplier_name = Supplier.objects.filter(id=filtered_supplier)
    subdetails3 = []
    name = ''
    if supplier_name:
        name = supplier_name[0].name
        subdetails1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=date_from,
                                                   date__lte=date_to, new_supplier__id=filtered_supplier) \
            .values('id', 'date', 'title', 'comment',
                    number=F('archive_id__number'),
                    objectname=F('house_id__object_id__name'),
                    housename=F('house_id__name')) \
            .annotate(tag=Value('a', output_field=CharField()), summary=(F('summary')))
        subdetails2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=date_from,
                                             date__lte=date_to, supplier__id=filtered_supplier) \
            .values('bid_id', 'date', 'title', 'comment',
                    number=F('bid_id__number'),
                    objectname=F('house_id__object_id__name'),
                    housename=F('house_id__name')) \
            .annotate(tag=Value('x', output_field=CharField()), summary=(F('quantity') * F('price')))
        if not is_special:
            subdetails2 = subdetails2.exclude(bid__hidden=True)

        concrete_delivery = Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to,
                                                    supplier__id=filtered_supplier) \
            .values('id', 'date', 'comment') \
            .annotate(
            title=Value('', output_field=CharField()),
            number=Value('отгрузка', output_field=CharField()),
            objectname=F('house_id__object_id__name'),
            housename=F('house_id__name'),
            tag=Value('-', output_field=CharField()),
            summary=(F('price') * F('volume') + F('pumpsummary') + F('deliveryprice') * F('deliveryvolume') + F('pumptransfer') + F('downtimecost') * F('downtime')))

        concrete_payments = Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to,
                                                      supplier__id=filtered_supplier) \
            .values('id', 'date', 'comment') \
            .annotate(
            title=Value('', output_field=CharField()),
            number=Value('аванс', output_field=CharField()),
            objectname=Value('-', output_field=CharField()),
            housename=Value('-', output_field=CharField()),
            tag=Value('-', output_field=CharField()),
            summary=-1 * (F('summary')))

        subdetails3 = subdetails1.union(subdetails2, concrete_delivery, concrete_payments, all=True).order_by('-date')
    return subdetails3, name

@login_required
def supplier_detail_report(request, supplier_id):
    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    supplier_name = Supplier.objects.filter(id=supplier_id)
    if not supplier_name:
        raise Http404

    date_from_str = request.GET.get('from')
    date_to_str = request.GET.get('to')
    subdetails3 = []
    filtered_supplier = supplier_id
    filtered = request.GET.get('s')
    supplier_name = None

    if date_from_str == 'None' or not CorrectDate(date_from_str):
        date_from = datetime.date(2020, 1, 1)
    else:
        date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    if date_to_str == 'None' or not CorrectDate(date_to_str):
        date_to = datetime.date(2024, 12, 31)
    else:
        date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

    if filtered_supplier > 0:
        subdetails3, supplier_name = get_supplier_details(date_from, date_to, filtered_supplier, is_special)

    #print(subdetails3)

    prev_ = request.META.get('HTTP_REFERER')

    #print(supplier_name)

    #return render(request, 'project/supplierdetails.html',
    #              {'title': 'Детализация расходов по дому', 'date_from': date_from, 'date_to': date_to, 'details': subdetails3, 'prev': prev_, 'supplier': supplier_name, 'id':filtered_supplier})

    form = SupplierReportForm(initial={'datefrom': None, 'dateto': None, 'filter_supplier': None})
    return render(request, 'project/supplierdetails.html', {'form': form, 'title': 'Детализация расходов по дому', 'date_from': date_from, 'date_to': date_to, 'details': subdetails3, 'prev': prev_, 'supplier': supplier_name, 'id':filtered_supplier, 'filtered': filtered})


@login_required
def supplier_detail_xls_report(request, supplier_id):
    def row_height(l1, l2):
        l = max(l1, l2)  #// + 12
        h = l // 28 + 1 #28
        return 13 * h

    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    supplier_ = Supplier.objects.get(id=supplier_id)
    if not supplier_:
        raise Http404

    date_from = None
    date_to = None
    date_from_str = ''
    date_to_str = ''


    if 'from' in request.GET:
        date_from_str = request.GET.get('from', None)
        if date_from_str == 'None' or not CorrectDate(date_from_str):
            date_from = datetime.date(2020, 1, 1)
        else:
            date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    else:
        date_from = datetime.date(2020, 1, 1)

    if 'to' in request.GET:
        date_to_str = request.GET.get('to', None)
        if date_to_str == 'None' or not CorrectDate(date_to_str):
            date_to = datetime.date(2024, 12, 31)
        else:
            date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
    else:
        date_to = datetime.date(2024, 12, 31)

    subdetails3, supplier_name = get_supplier_details(date_from, date_to, supplier_id, is_special)

    buffer = io.BytesIO()
    workbook = xlsxwriter.Workbook(buffer)
    worksheet = workbook.add_worksheet()
    worksheet.set_portrait()
    worksheet.set_margins(0.5, 0.5, 0.55, 0.55)
    merge_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'left',
        'valign': 'vbottom',
        'color': 'white',
        'fg_color': 'gray'})
    cell_format = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10})
    cell_format_left = workbook.add_format({
        'bold': 1,
        'border': 1,
        'align': 'left',
        'valign': 'vbottom',
        'fg_color': 'white',
        'color': 'black',
        'font_size': 10})
    align_ = workbook.add_format(
        {'align': 'left', 'valign': 'vbottom', 'border': 1, 'text_wrap': True, 'font_size': 10})

    col_widths = [10, 25, 16, 7, 34]
    worksheet.merge_range('A1:E1', 'Поставщик: '+str(supplier_.name) + ' с ' + date_from.strftime("%d.%m.%Y") + ' по ' + date_to.strftime("%d.%m.%Y"), workbook.add_format({'bold': 1, 'border': 1, 'align': 'left', 'valign': 'vbottom', 'fg_color': 'gray', 'color': 'white', 'font_size': 14}))
    header1 = ['Дата', 'Объект/№ дома', 'Поступление/аванс', 'Номер', 'Описание']

    row = 2
    for col_num, data in enumerate(header1):
        worksheet.set_column(col_num, col_num, col_widths[col_num])
        worksheet.write(1, col_num, data, cell_format)

    #print(subdetails3)

    for item in subdetails3:
            worksheet.write(row, 0, item['date'].strftime(("%d.%m.%Y")), cell_format)
            worksheet.write(row, 1, item['objectname']+'/'+item['housename'], cell_format_left)
            worksheet.write(row, 2, item['summary'], workbook.add_format({'num_format': '#,##0.00', 'bold': 0, 'border': 1, 'align': 'right', 'valign': 'vbottom', 'fg_color': 'white', 'color': 'black', 'font_size': 10, 'text_wrap': True}))
            if item['tag'] == 'a':
                worksheet.write(row, 3, 'a'+item['number'], cell_format_left)
            else:
                worksheet.write(row, 3, item['number'], cell_format_left)

            length1 = len(item['comment'])

            commentstr = item['comment'] + '/' + item['title']
            worksheet.write(row, 4, commentstr, align_)
            length2 = len(commentstr)
            worksheet.set_row(row, row_height(length1, length2))

            row += 1



    workbook.close()
    buffer.seek(0)
    filename = 'report'+str(supplier_.id)+'.xlsx'
    response = HttpResponse(
            buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


@login_required
def house_report(request, house_id):
    return render(request, 'project/housereport.html', {'title': 'Отчёт по дому'})

@login_required
def house_estimate_report(request, house_id, estimate_id, phase_id, type, exclusion):

    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    date_from_str = request.GET.get('from')
    date_to_str = request.GET.get('to')

    barter_only = False
    barter_only_str = request.GET.get('b')
    if barter_only_str == 'True':
        barter_only = True
    else:
        barter_only = False

    if date_from_str == 'None' or not CorrectDate(date_from_str):
        date_from = datetime.date(2020, 1, 1)
    else:
        date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    if date_to_str == 'None' or not CorrectDate(date_to_str):
        date_to = datetime.date(2024, 12, 31)
    else:
        date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

    #print(date_from)
    #print(date_to)

    house = House.objects.get(id=house_id)
    object = Object.objects.get(id=house.object_id)
    estimate = Estimate.objects.get(id=estimate_id)

    if not barter_only:
        summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=date_from, date__lte=date_to, estimate_id=estimate_id, house_id=house_id).values('house__object__id', 'house__object__name', 'summary', 'archive_id__number', 'title', 'date', 'comment', 'supplier', 'house_id__name', 'phase_id__name', 'type').order_by('-archive_id__number') #.annotate(summary=Sum('summary'))
        if phase_id > 0:
            summary1 = summary1.filter(phase_id=phase_id)
        if type != '0':
            summary1 = summary1.filter(type=type)
    else:
        summary1 = []
    #print(summary1)
    if barter_only:
        summary2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, date__gte=date_from,
                                            date__lte=date_to, estimate_id=estimate_id, house_id=house_id, cash='b').values(
        'house__object__id', 'house__object__name', 'quantity', 'price', 'bid_id__number', 'title', 'date', 'comment', 'supplier_id__name', 'house_id__name', 'phase_id__name', 'type').order_by('-bid_id__number')  # .annotate(summary=Sum('summary'))
    else:
        summary2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, date__gte=date_from,
                                            date__lte=date_to, estimate_id=estimate_id, house_id=house_id).values(
        'house__object__id', 'house__object__name', 'quantity', 'price', 'bid_id__number', 'title', 'date', 'comment', 'supplier_id__name', 'house_id__name', 'phase_id__name', 'type').order_by('-bid_id__number')  # .annotate(summary=Sum('summary'))
    if not is_special:
        summary2 = summary2.exclude(bid__hidden=True)
    if phase_id >0:
        summary2 = summary2.filter(phase_id=phase_id)
    if type != '0':
        summary2 = summary2.filter(type=type)

    if exclusion == '1':
        summary2 = summary2.exclude(type='f', phase__id=6, estimate__id=84)

    disp = dict(Content.SUPPLY)
    for item in summary1:
        item['type'] = disp[item['type']]
    for item in summary2:
        item['type'] = disp[item['type']]

    #summary2 = Content.objects.filter(deleted=False, bid__deleted=False, date__gte=datefrom, date__lte=dateto).values('house__object__id', 'house__object__name').annotate(summary=Sum(F('quantity') * F('price')))
    #summary3 = summary1.union(summary2, all=True).order_by('house__object__id')


    return render(request, 'project/housereport.html',
                  {'title': 'Детализация расходов по дому', 'object': object, 'house': house, 'estimate': estimate,
                   'date_from': date_from, 'date_to': date_to, 'archive': summary1, 'bids': summary2})


@login_required
def house_phase_report(request, house_id, phase_id, estimate_id, type, exclusion):
    is_manager = request.user.groups.filter(name='managers').exists()
    is_special = request.user.groups.filter(name='special').exists()

    if not is_manager:
        raise Http404

    rollback = request.GET.urlencode()
    selected_house = 0

    date_from_str = request.GET.get('from')
    date_to_str = request.GET.get('to')

    barter_only = False
    barter_only_str = request.GET.get('b')
    if barter_only_str == 'True':
        barter_only = True
    else:
        barter_only = False

    if date_from_str == 'None' or not CorrectDate(date_from_str):
        date_from = datetime.date(2020, 1, 1)
    else:
        date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    if date_to_str == 'None' or not CorrectDate(date_to_str):
        date_to = datetime.date(2024, 12, 31)
    else:
        date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

    house = House.objects.get(id=house_id)
    object = Object.objects.get(id=house.object_id)
    phase = Phase.objects.get(id=phase_id)

    if not barter_only:
        summary1 = ArchiveDetail.objects.filter(deleted=False, archive__deleted=False, date__gte=date_from, date__lte=date_to, phase_id=phase_id, house_id=house_id).values('house__object__id', 'house__object__name', 'summary', 'archive_id__number', 'title', 'date', 'comment', 'supplier', 'house_id__name', 'estimate_id__name', 'type').order_by('-archive_id__number') #.annotate(summary=Sum('summary'))
        if estimate_id > 0:
            summary1 = summary1.filter(estimate_id=estimate_id)
        if type != '0':
            summary1 = summary1.filter(type=type)
    else:
        summary1 = []
    if barter_only:
        summary2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, date__gte=date_from,
                                            date__lte=date_to, phase_id=phase_id, house_id=house_id, cash='b').values(
        'house__object__id', 'house__object__name', 'quantity', 'price', 'bid_id', 'bid_id__number', 'title', 'date', 'comment', 'supplier_id__name', 'house_id__name', 'estimate_id__name', 'type').extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
        # .extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')  --- .order_by('-bid_id__number')
    else:
        summary2 = Content.objects.filter(deleted=False, bid__deleted=False, bid__refunded=False, date__gte=date_from,
                                            date__lte=date_to, phase_id=phase_id, house_id=house_id).values(
        'house__object__id', 'house__object__name', 'quantity', 'price', 'bid_id', 'bid_id__number', 'title', 'date', 'comment', 'supplier_id__name', 'house_id__name', 'estimate_id__name', 'type').extra({'n': "10000+CAST(number as TEXT)"}).order_by('-n')
    if not is_special:
        summary2 = summary2.exclude(bid__hidden=True)
    if estimate_id > 0:
        summary2 = summary2.filter(estimate_id=estimate_id)
    if type != '0':
        summary2 = summary2.filter(type=type)

    if exclusion == '1':
        summary2 = summary2.exclude(type='f', phase__id=6, estimate__id=84)

    disp = dict(Content.SUPPLY)
    for item in summary1:
        item['type'] = disp[item['type']]
    for item in summary2:
        item['type'] = disp[item['type']]

    #rollback = '?from=' + date_from_str + '&to=' + date_to_str + '&e=' + str(estimate_id) + '&p=' + str(phase_id) + '&t=' + type + '&c=False&b=' + str(barter_only) + '&x=' + str(exclusion)
    if 'h' in request.GET:
        selected_house_str = request.GET.get('h', None)
        try:
           rollback += '#panelsStayOpen-heading-' + selected_house_str
        except:
           pass
    #print('<---', rollback)

    return render(request, 'project/housephasereport.html',
                  {'title': 'Детализация расходов по дому', 'object': object, 'house': house, 'phase': phase,
                   'date_from': date_from, 'date_to': date_to, 'archive': summary1, 'bids': summary2, 'rollback': rollback})


@login_required
def house_concrete_report(request, house_id):
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    date_from_str = request.GET.get('from')
    date_to_str = request.GET.get('to')

    if date_from_str == 'None' or not CorrectDate(date_from_str):
        date_from = datetime.date(2020, 1, 1)
    else:
        date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    if date_to_str == 'None' or not CorrectDate(date_to_str):
        date_to = datetime.date(2024, 12, 31)
    else:
        date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")

    house = House.objects.get(id=house_id)
    object_ = Object.objects.get(id=house.object_id)

    delivery_house = (Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, house__id=house_id).values('house__id', 'object_id', 'house__name', 'comment', 'date', 'supplier__name', 'volume').annotate(
        total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F('deliveryvolume')).order_by('-date'))
    summary_volume = 0
    for item in delivery_house:
        summary_volume += item['volume']

    return render(request, 'project/houseconcrete.html',
                  {'title': 'Детализация заливок по дому', 'object': object_, 'house': house,
                   'date_from': date_from, 'date_to': date_to, 'delivery': delivery_house, 'summary_volume': summary_volume})

@login_required
def filtered_suppliers(request):
    error = ''
    filter_str = ''
    is_bosses = request.user.groups.filter(name='bosses').exists()
    is_accountants = request.user.groups.filter(name='accountants').exists()
    is_suppliers = request.user.groups.filter(name='suppliers').exists()

    if not is_bosses and not is_accountants and not is_suppliers:
        raise Http404

    selected = request.GET.get('s')
    try:
        selected_ = int(selected)
    except:
        selected_ = 0

    if request.method == 'POST':
        form = SuppliersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('project:suppliers')+'?f=' + cd['filter_str'])
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/suppliers.html', context)
    else:
        filter_str = ''
        if 'f' in request.GET:
            filter_str = request.GET.get('f').strip()
        if filter_str:
            suppliers = Supplier.objects.filter(name__icontains=filter_str)
        else:
            suppliers = Supplier.objects.all()

        form = SuppliersForm(initial={'filter_str': filter_str})
        context = {
            'form': form,
            'error': error,
            'filter_str': filter_str,
            'suppliers': suppliers
        }
    return render(request, 'project/suppliers.html', context)


@login_required
def filtered_estimates(request):
    error = ''
    filter_str = ''
    is_bosses = request.user.groups.filter(name='bosses').exists()

    if not is_bosses:
        raise Http404

    selected = request.GET.get('s')
    try:
        selected_ = int(selected)
    except:
        selected_ = 0
    deletemessage = request.GET.get('e')
    if deletemessage == '1':
        error = 'Ошибка удаления! Выбранная смета используется в действующих заявках!'

    if request.method == 'POST':
        form = EstimatesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('project:estimates')+'?f=' + cd['filter_str'])
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/estimates.html', context)
    else:
        filter_str = ''
        if 'f' in request.GET:
            filter_str = request.GET.get('f').strip()
        if filter_str:
            estimates = Estimate.objects.filter(name__icontains=filter_str, deleted=False).order_by('name')
        else:
            estimates = Estimate.objects.filter(deleted=False).order_by('name')

        form = EstimatesForm(initial={'filter_str': filter_str})
        context = {
            'form': form,
            'error': error,
            'filter_str': filter_str,
            'estimates': estimates
        }
    return render(request, 'project/estimates.html', context)


@login_required
def filtered_phases(request):
    error = ''
    filter_str = ''
    is_bosses = request.user.groups.filter(name='bosses').exists()

    if not is_bosses:
        raise Http404

    selected = request.GET.get('s')
    try:
        selected_ = int(selected)
    except:
        selected_ = 0
    deletemessage = request.GET.get('e')
    if deletemessage == '1':
        error = 'Ошибка удаления! Выбранный этап используется в действующих заявках!'

    if request.method == 'POST':
        form = PhasesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('project:phases')+'?f=' + cd['filter_str'])
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/phases.html', context)
    else:
        filter_str = ''
        if 'f' in request.GET:
            filter_str = request.GET.get('f').strip()
        if filter_str:
            phases = Phase.objects.filter(name__icontains=filter_str, deleted=False).order_by('name')
        else:
            phases = Phase.objects.filter(deleted=False).order_by('name')

        form = PhasesForm(initial={'filter_str': filter_str})
        context = {
            'form': form,
            'error': error,
            'filter_str': filter_str,
            'phases': phases
        }
    return render(request, 'project/phases.html', context)


@login_required
def search(request):
    search_str = ''
    bidlist = []
    archlist = []

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            return HttpResponseRedirect(reverse('project:found')+'?q=' + cd['number'])
    else:
        if 'q' in request.GET:
            search_str = request.GET.get('q', None)
        search_str = ''.join(c for c in search_str if c in '0123456789/-')

        if len(search_str) > 2:
            is_manager = request.user.groups.filter(name='managers').exists()
            if is_manager:
                bidlist = Bid.objects.filter(deleted=False, number__contains=search_str).order_by('-number')
                archlist = Archive.objects.filter(deleted=False, number__contains=search_str).order_by('-number')
            else:
                bidlist = Bid.objects.filter(owner=request.user, deleted=False, number__contains=search_str).order_by('-number')
                archlist = Archive.objects.filter(owner=request.user, deleted=False, number__contains=search_str).order_by('-number')

        form = SearchForm(initial={'number': search_str})
    return render(request, 'project/found.html', {'form': form, 'title': 'Поиск заявок',
                                                  'bidlist': bidlist,
                                                  'archlist': archlist,
                                                  'number': search_str})

def get_grade_display(index):
    return [item for item in Delivery.GRADE if index in item][0][1] #Delivery.GRADE[index]


def get_date_from_list(lst, index, ln):
    if index < ln:
        return lst[index]['date']
    else:
        return mydatetime.min

@login_required
def filtered_subcashes(request):
    error = ''
    filter_str = ''
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if not is_boss and not is_accountant:
        raise Http404

    cashregister = request.GET.get('c')
    try:
        cashregister = int(cashregister)
    except:
        cashregister = 0
    if request.method == 'POST':
        form = SubCashesForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cashreg = cd['cashregister']
            return HttpResponseRedirect(reverse('project:filteredsubcashes')+'?c=' + str(cashreg.id))
        else:
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/subcash.html', context)
    else:
        subcash = SubCash.objects.filter(deleted=False, cashregister_id=cashregister)
        form = SubCashesForm(initial={'cashregister': cashregister})
        context = {
            'form': form,
            'error': error,
            'cashregister': cashregister,
            'subcash': subcash
        }
    return render(request, 'project/subcash.html', context)


@login_required
def filtered_accounts(request):
    error = ''
    filter_str = ''
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if not is_boss and not is_accountant:
        raise Http404

    cashregister = request.GET.get('c')
    try:
        cashregister = int(cashregister)
    except:
        cashregister = 0
    if request.method == 'POST':
        form = AccountsForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cashreg = cd['cashregister']
            return HttpResponseRedirect(reverse('project:filteredaccounts')+'?c=' + str(cashreg.id))
        else:
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/accounts.html', context)
    else:
        subcash = Account.objects.filter(deleted=False, cashregister_id=cashregister)
        form = AccountsForm(initial={'cashregister': cashregister})
        context = {
            'form': form,
            'error': error,
            'cashregister': cashregister,
            'subcash': subcash
        }
    return render(request, 'project/accounts.html', context)


@login_required
def new_subcash(request):
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if not is_boss and not is_accountant:
        raise Http404
    cashregister = request.GET.get('c')
    try:
        cashregister = int(cashregister)
    except:
        cashregister = 0
    error = ''
    if request.method == 'POST':
        form = SubCashForm(request.POST, cashregisterid=cashregister)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:filteredsubcashes')+'?c='+str(cashregister))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новая касса',
                'cashregister': cashregister
            }
            return render(request, 'project/addsubcash.html', context)

    form = SubCashForm(initial={'cashregister': cashregister}, cashregisterid=cashregister)
    context = {
        'form': form,
        'error': error,
        'title': 'Новая касса',
        'cashregister': cashregister
    }
    return render(request, 'project/addsubcash.html', context)


@login_required
def new_account(request):
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if not is_boss and not is_accountant:
        raise Http404
    cashregister = request.GET.get('c')
    try:
        cashregister = int(cashregister)
    except:
        cashregister = 0
    error = ''
    if request.method == 'POST':
        form = AccountForm(request.POST, cashregisterid=cashregister)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:filteredaccounts')+'?c='+str(cashregister))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новый счет',
                'cashregister': cashregister
            }
            return render(request, 'project/addaccount.html', context)

    form = AccountForm(initial={'cashregister': cashregister}, cashregisterid=cashregister)
    context = {
        'form': form,
        'error': error,
        'title': 'Новый счет',
        'cashregister': cashregister
    }
    return render(request, 'project/addaccount.html', context)


@login_required
def edit_subcash(request, subcash_id):
    cashregister = request.GET.get('c')
    error = ''

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    subcash_ = SubCash.objects.get(id=subcash_id)
    if subcash_.deleted:
        raise Http404

    if request.method == 'POST':
        form = SubCashFormEdit(request.POST, instance=subcash_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:filteredsubcashes')+'?c='+str(cashregister))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка кассы',
                'cashregister': cashregister
            }
            return render(request, 'project/editsubcash.html', context)

    data = {'name': subcash_.name, 'balance': subcash_.balance, 'date': subcash_.date, 'closedate': subcash_.closedate,
            'cashregister': subcash_.cashregister}
    form = SubCashFormEdit(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Новая касса',
        'cashregister': cashregister,
        'cashregister_': subcash_.cashregister.name
    }
    return render(request, 'project/editsubcash.html', context)


@login_required
def edit_account(request, account_id):
    cashregister = request.GET.get('c')
    error = ''

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    account_ = Account.objects.get(id=account_id)
    if account_.deleted:
        raise Http404

    if request.method == 'POST':
        form = AccountFormEdit(request.POST, instance=account_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:filteredaccounts')+'?c='+str(cashregister))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка счета',
                'cashregister': cashregister
            }
            return render(request, 'project/editaccount.html', context)

    data = {'name': account_.name, 'balance': account_.balance, 'date': account_.date, 'closedate': account_.closedate,
            'cashregister': account_.cashregister}
    form = AccountFormEdit(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка счета',
        'cashregister': cashregister,
        'cashregister_': account_.cashregister.name
    }
    return render(request, 'project/editaccount.html', context)


@login_required
def edit_expense_transaction(request, content_id):
    rollback = request.GET.urlencode()
    if 'c' in request.GET:
        cashregister_str = request.GET.get('c', '0')
        try:
            cashregister = int(cashregister_str)
        except:
            cashregister = 0
    else:
        cashregister = 0
    cashreg = CashRegister.objects.get(id=cashregister)
    error = ''
    page_number = request.GET.get('page')

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    content_ = Content.objects.get(id=content_id)
    if content_.deleted or content_.bid.deleted:
        raise Http404

    if request.method == 'POST':
        form = ExpenseContentFormEdit(request.POST, instance=content_, cashregisterid=cashregister, contentdate=content_.date)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:filteredbalances')+'?'+str(rollback))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка кассы',
                'cashregister': cashregister,
                'content': content_,
                'cashreg': cashreg,
                'rollback': rollback
            }
            return render(request, 'project/editexpense.html', context)

    #data = {''}
    #print('====>',content_.subcash)
    form = ExpenseContentFormEdit(initial={'subcash': content_.subcash, 'expense_account': content_.expense_account, 'credit_account': content_.credit_account}, cashregisterid=cashregister, contentdate=content_.date)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка расхода',
        'cashregister': cashregister,
        'content': content_,
        'cashreg': cashreg,
        'rollback': rollback
    }
    return render(request, 'project/editexpense.html', context)


@login_required
def erase_expense_transaction(request, content_id):
    rollback = request.GET.urlencode()
    content_ = Content.objects.get(id=content_id)

    if content_.deleted or content_.bid.deleted:
        raise Http404

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    content_.subcash = None
    content_.expense_account = None
    content_.credit_account = None
    content_.save()
    return HttpResponseRedirect(reverse('project:filteredbalances')+'?'+str(rollback))


@login_required
def create_earning_transaction(request):
    errors = []
    rollback = request.GET.urlencode()
    if 'c' in request.GET:
        cashregister_str = request.GET.get('c', '0')
        try:
            cashregister = int(cashregister_str)
        except:
            cashregister = 0
    else:
        cashregister = 0
    if cashregister == 0:
        raise Http404

    cashreg = CashRegister.objects.get(id=cashregister)
    if 'from' in request.GET:
        date_from_str = request.GET.get('from', None)
        if date_from_str == 'None' or not CorrectDate(date_from_str):
            date_from = datetime.datetime(2024, 4, 22, 0, 0)
        else:
            date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    else:
        date_from = datetime.datetime(2024, 4, 22, 0, 0)
    error = ''
    page_number = request.GET.get('page')

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    if request.method == 'POST':
        form = EarningForm(request.POST, cashregisterid=cashregister, contentdate=date_from)
        if form.is_valid():
            new_earning_ = form.save(commit=False)
            new_earning_.owner = request.user

            subcash = SubCash.objects.get(id=new_earning_.subcash_id)
            credit_account = Account.objects.get(id=new_earning_.credit_account_id)
            expense_account = Account.objects.get(id=new_earning_.expense_account_id)
            if subcash.closedate and subcash.closedate < new_earning_.date:
                errors.append("На указанную дату касса '"+subcash.name+"' закрыта!")
            if expense_account.closedate and expense_account.closedate < new_earning_.date:
                errors.append("На указанную дату счет контрагента '"+expense_account.name+"' закрыт!")
            if credit_account.closedate and credit_account.closedate < new_earning_.date:
                errors.append("На указанную дату счет кассы '"+credit_account.name+"' закрыт!")
            if errors:
                context = {
                    'form': form,
                    'errors': errors,
                    'title': 'Добавление прихода',
                    'cashregister': cashreg,
                    'rollback': rollback
                }
                return render(request, 'project/addearning.html', context)
            else:
                form.save()
                return HttpResponseRedirect(reverse('project:filteredbalances')+'?'+str(rollback))
        else:
            errors = ['Неверные данные формы',]
            context = {
                'form': form,
                'errors': errors,
                'title': 'Добавление прихода',
                'cashregister': cashreg,
                'rollback': rollback
            }
            return render(request, 'project/addearning.html', context)

    form = EarningForm(cashregisterid=cashregister, contentdate=date_from)
    context = {
        'form': form,
        'errors': errors,
        'title': 'Добавление прихода',
        'cashregister': cashreg,
        'rollback': rollback
    }
    return render(request, 'project/addearning.html', context)


@login_required
def edit_earning_transaction(request, earning_id):
    errors = []
    rollback = request.GET.urlencode()
    if 'c' in request.GET:
        cashregister_str = request.GET.get('c', '0')
        try:
            cashregister = int(cashregister_str)
        except:
            cashregister = 0
    else:
        cashregister = 0
    cashreg = CashRegister.objects.get(id=cashregister)
    if 'from' in request.GET:
        date_from_str = request.GET.get('from', None)
        if date_from_str == 'None' or not CorrectDate(date_from_str):
            date_from = datetime.datetime(2024, 4, 22, 0, 0)
        else:
            date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
    else:
        date_from = datetime.datetime(2024, 4, 22, 0, 0)

    page_number = request.GET.get('page')

    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if not is_boss and not is_accountant:
        raise Http404

    earning_ = Earning.objects.get(id=earning_id)

    if request.method == 'POST':
        form = EarningForm(request.POST, instance=earning_, cashregisterid=cashregister, contentdate=date_from)
        if form.is_valid():
            new_earning_ = form.save(commit=False)
            new_earning_.owner = request.user

            subcash = SubCash.objects.get(id=new_earning_.subcash_id)
            credit_account = Account.objects.get(id=new_earning_.credit_account_id)
            expense_account = Account.objects.get(id=new_earning_.expense_account_id)
            if subcash.closedate and subcash.closedate < new_earning_.date:
                errors.append("На указанную дату касса '"+subcash.name+"' закрыта!")
            if expense_account.closedate and expense_account.closedate < new_earning_.date:
                errors.append("На указанную дату счет контрагента '"+expense_account.name+"' закрыт!")
            if credit_account.closedate and credit_account.closedate < new_earning_.date:
                errors.append("На указанную дату счет кассы '"+credit_account.name+"' закрыт!")
            if errors:
                context = {
                    'form': form,
                    'errors': errors,
                    'title': 'Корректировка прихода',
                    'cashregister': cashreg,
                    'rollback': rollback
                }
                return render(request, 'project/addearning.html', context)
            else:
                form.save()
                return HttpResponseRedirect(reverse('project:filteredbalances')+'?'+str(rollback))
        else:
            errors = ['Неверные данные формы',]
            context = {
                'form': form,
                'errors': errors,
                'title': 'Корректировка прихода',
                'cashregister': cashreg,
                'rollback': rollback
            }
            return render(request, 'project/addearning.html', context)

    form = EarningForm(initial={'comment': earning_.comment, 'date': earning_.date, 'summary': earning_.summary,
                                'supplier': earning_.supplier, 'object': earning_.object, 'subcash': earning_.subcash,
                                'expense_account': earning_.expense_account, 'credit_account': earning_.credit_account}, cashregisterid=cashregister, contentdate=date_from)
    context = {
        'form': form,
        'errors': errors,
        'title': 'Корректировка прихода',
        'cashregister': cashreg,
        'rollback': rollback
    }
    return render(request, 'project/addearning.html', context)


def GetDates(weekdelta, from_to):
    dt = datetime.datetime.now()
    #day = '25/05/2023'
    #dt = datetime.datetime.strptime(day, '%d/%m/%Y')
    start = dt - timedelta(days=dt.weekday()) + timedelta(weekdelta * 7)
    end = start + timedelta(days=6)
    #print(start.strftime('%d/%m/%Y'))
    #print(end.strftime('%d/%m/%Y'))
    if from_to: return start
    else: return end

@login_required
def filtered_balances(request):
    expense = []
    date_from = None
    date_to = None
    date_from_str = ''
    date_to_str = ''
    filtered_choice = 0
    cashregister = 0
    all_cash_in, all_cash_flow, all_cash_income, all_cash_out = 0, 0, 0, 0
    all_acc_in, all_acc_flow, all_acc_income, all_acc_out = 0, 0, 0, 0
    page_number = request.GET.get('page')
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    user = request.user

    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            out_str = '?page=1'
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)
            choice_filter = cd['choice_filter']
            if choice_filter is None:
                out_str += '&f=0'
            else:
                out_str += '&f=' + str(choice_filter)
            cashregister = cd['cashregister']
            if cashregister is None:
                out_str += '&c=0'
            else:
                out_str += '&c=' + str(cashregister.id)

            return HttpResponseRedirect(reverse('project:filteredbalances') + out_str)

    else:
        #GetDates(-1, True)
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = GetDates(0, True) # datetime.datetime(2023, 4, 22, 0, 0)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = GetDates(0, True) # datetime.datetime(2023, 4, 22, 0, 0)

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = GetDates(0, False) # datetime.datetime(2023, 12, 31, 0, 0)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
        else:
            date_to = GetDates(0, False) # datetime.datetime(2023, 12, 31, 0, 0)
        if 'f' in request.GET:
            filtered_choice_str = request.GET.get('f', '0')
            try:
                filtered_choice = int(filtered_choice_str)
            except:
                filtered_choice = 0
        else:
            filtered_choice = 0
        if 'c' in request.GET:
            cashregister_str = request.GET.get('c', '0')
            try:
                cashregister = int(cashregister_str)
            except:
                cashregister = 0
        else:
            cashregister = 0

        form = BalanceForm(initial={'datefrom': date_from, 'dateto': date_to, 'choice_filter': filtered_choice, 'cashregister': cashregister})

        start = time.time()

        # суммарные обороты по расходу и доходу за выбранный период в разрезе счетов
        flow_turnover_acc = Content.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, bid__locked=True,
                                      bid__deleted=False, subcash__isnull=False, credit_account__isnull=False,
                                      expense_account__isnull=False, subcash__cashregister=cashregister).values('expense_account').order_by('expense_account').annotate(summary=Sum(F('price') * F('quantity')))
        income_turnover_acc = Earning.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, subcash__cashregister=cashregister).values('credit_account').order_by('credit_account').annotate(summary=Sum('summary'))
        #print('-->',flow_turnover_acc)
        #print('<--', income_turnover_acc)
        accounts = Account.objects.filter((Q(closedate__gte=date_from) | Q(closedate__isnull=True)) & Q(deleted=False) & Q(cashregister=cashregister))
        accarray = []
        for item in accounts:
            fl_turn = 0
            for fl_ in flow_turnover_acc:
                if item.id == fl_['expense_account']:
                    fl_turn = fl_['summary']
                    break
            in_turn = 0
            for inc_ in income_turnover_acc:
                if item.id == inc_['credit_account']:
                    in_turn = inc_['summary']
                    break
            if item.date < date_from:
                flow = Content.objects.filter(deleted=False, date__gte=item.date, date__lt=date_from, bid__locked=True, bid__deleted=False, subcash__isnull=False, credit_account__isnull=False, expense_account__isnull=False, expense_account=item.id).aggregate(summary=Sum(F('price')*F('quantity')))['summary']
                if not flow: flow = 0
                income = Earning.objects.filter(deleted=False, date__gte=item.date, date__lt=date_from, credit_account=item.id).aggregate(summary=Sum('summary'))['summary']
                if not income: income = 0
                accarray.append({'id': item.id, 'name': item.name, 'incoming_balance': item.balance - flow + income, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': item.balance - flow + income - fl_turn + in_turn})
            elif item.date == date_from:
                accarray.append({'id': item.id, 'name': item.name, 'incoming_balance': item.balance, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': item.balance - fl_turn + in_turn})
            # если вообще нет остатка, то он устанавливается равным 0
            else:
                accarray.append({'id': item.id, 'name': item.name, 'incoming_balance': 0, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': 0 - fl_turn + in_turn})
            all_acc_in += accarray[len(accarray)-1]['incoming_balance']
            all_acc_flow += accarray[len(accarray)-1]['flow']
            all_acc_income += accarray[len(accarray)-1]['income']
            all_acc_out += accarray[len(accarray)-1]['outgoing']


        # суммарные обороты по расходу и доходу за выбранный период в разрезе касс
        flow_turnover = Content.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, bid__locked=True,
                                      bid__deleted=False, subcash__isnull=False, credit_account__isnull=False,
                                      expense_account__isnull=False, subcash__cashregister=cashregister).values('subcash', 'subcash__name').order_by('subcash').annotate(summary=Sum(F('price') * F('quantity')))
        income_turnover = Earning.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, subcash__cashregister=cashregister).values('subcash').order_by('subcash').annotate(summary=Sum('summary'))
        #print('-->',flow_turnover)
        #print('<--', income_turnover)

        # Список касс
        subcash = SubCash.objects.filter((Q(closedate__gte=date_from) | Q(closedate__isnull=True)) & Q(deleted=False) & Q(cashregister=cashregister))
        #print(subcash)
        casharray = []
        for item in subcash:
            fl_turn = 0
            for fl_ in flow_turnover:
                if item.id == fl_['subcash']:
                    fl_turn = fl_['summary']
                    break
            in_turn = 0
            for inc_ in income_turnover:
                if item.id == inc_['subcash']:
                    in_turn = inc_['summary']
                    break
            #print(item.name, item.date, item.balance)

            # если дата остатка по кассе меньше начальной даты отчёта, то вычисляем обороты за период от остатка до начала отчёта
            if item.date < date_from:
                flow = Content.objects.filter(deleted=False, date__gte=item.date, date__lt=date_from, bid__locked=True, bid__deleted=False, subcash__isnull=False, credit_account__isnull=False, expense_account__isnull=False, subcash=item.id).aggregate(summary=Sum(F('price')*F('quantity')))['summary']
                if not flow: flow = 0
                income = Earning.objects.filter(deleted=False, date__gte=item.date, date__lt=date_from, subcash=item.id).aggregate(summary=Sum('summary'))['summary']
                if not income: income = 0
                #print(flow)
                #print(income)
                casharray.append({'id': item.id, 'name': item.name, 'incoming_balance': item.balance - flow + income, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': item.balance - flow + income - fl_turn + in_turn})
            # если дата остатка совпадает с начальной датой отчёта
            elif item.date == date_from:
                casharray.append({'id': item.id, 'name': item.name, 'incoming_balance': item.balance, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': item.balance - fl_turn + in_turn})
            # если вообще нет остатка, то он устанавливается равным 0
            else:
                casharray.append({'id': item.id, 'name': item.name, 'incoming_balance': 0, 'flow': -1 * fl_turn, 'income': in_turn, 'outgoing': 0 - fl_turn + in_turn})
            #print(casharray[len(casharray)-1]['flow'])
            all_cash_in += casharray[len(casharray)-1]['incoming_balance']
            all_cash_flow += casharray[len(casharray)-1]['flow']
            all_cash_income += casharray[len(casharray)-1]['income']
            all_cash_out += casharray[len(casharray)-1]['outgoing']
            #print(all_cash_in, all_cash_flow, all_cash_income, all_cash_out )

        #print('==>', casharray)
        expense = []
        earnings = []
        if cashregister:
            # в зависимости от выбора определяем, какие обороты отображать в форме
            if filtered_choice in [0,2,3,4]:
                expense = (Content.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, bid__locked=True, bid__deleted=False).values('id', 'date', 'title', 'comment', 'quantity', 'price', 'subcash__name', 'bid__object__name', 'credit_account__name', 'expense_account__name', 'bid__number').order_by('-date', '-id'))
                #print(expense)
                if filtered_choice in [2,4]:
                    #expense = (expense.exclude(subcash__isnull=True).exclude(credit_account__isnull=True).exclude(expense_account__isnull=True))
                    expense = expense.exclude(Q(subcash__isnull=True) | Q(credit_account__isnull=True) | Q(expense_account__isnull=True)).filter(subcash__cashregister=cashregister)
                elif filtered_choice == 3:
                    expense = (expense.filter(Q(subcash__isnull=True) | Q(credit_account__isnull=True) | Q(expense_account__isnull=True)).order_by('-date', '-id'))
                else:
                    expense = (expense.filter(Q(subcash__isnull=True) | Q(credit_account__isnull=True) | Q(expense_account__isnull=True) | Q(subcash__cashregister=cashregister)).order_by('-date', '-id'))
            #print(expense)

            if filtered_choice in [0,1,4]:
                earnings = (Earning.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, subcash__cashregister=cashregister).values('id', 'date', 'comment', 'summary', 'subcash__name', 'object__name', 'credit_account__name', 'expense_account__name').order_by('-date', '-id'))

        #print(expense)
        expense_ = []
        for item in expense:
            if item['subcash__name'] == None:
                expense_.append({'type': 0,
                                'id': str(item['id'])+'a', 'id_': item['id'], 'number': item['bid__number'], 'date': item['date'], 'title': item['title'], 'comment': item['comment'],
                                'quantity': item['quantity'], 'price': item['price'], 'object_name': item['bid__object__name'], 'subcash_name': item['subcash__name'], 'credit_account__name': item['credit_account__name'], 'expense_account__name': item['expense_account__name']})
            else:
                expense_.append({'type': 1,
                                'id': str(item['id'])+'a', 'id_': item['id'], 'number': item['bid__number'], 'date': item['date'], 'title': item['title'], 'comment': item['comment'],
                                'quantity': item['quantity'], 'price': item['price'], 'object_name': item['bid__object__name'], 'subcash_name': item['subcash__name'], 'credit_account__name': item['credit_account__name'], 'expense_account__name': item['expense_account__name']})

        earnings_ = []
        for item in earnings:
            earnings_.append({'type': 2,
                                'id': str(item['id'])+'b', 'id_': item['id'], 'number': 'б/н', 'date': item['date'], 'title': item['comment'], 'comment': '',
                                'quantity': 1, 'price': item['summary'], 'object_name': item['object__name'], 'subcash_name': item['subcash__name'], 'credit_account__name': item['credit_account__name'], 'expense_account__name': item['expense_account__name']})

        res = []
        cp, cr = 0, 0
        lp, lr = len(expense_), len(earnings_)
        if expense_ and earnings_:
            while True:
                if get_date_from_list(expense_, cp, lp) > get_date_from_list(earnings_, cr, lr):
                    res.append(expense_[cp])
                    cp += 1
                else:
                    res.append(earnings_[cr])
                    cr += 1
                if cp >= lp and cr >= lr:
                    break
        else:
            if expense_: res = expense_
            else: res = earnings_

        #print(res)
        #for item in expense:
        #    print(item.house.name)
        paginator = Paginator(res, 10)

        try:
            page_ = paginator.page(page_number)
        except:
            page_ = paginator.page(1)
            page_number = 1

        print('1: ', time.time() - start)

    try:
        cashreg = CashRegister.objects.filter(id=cashregister)[0]
    except:
        cashreg = None

    date_from_minus = (date_from - timedelta(7)).strftime('%Y-%m-%d')
    date_to_minus = (date_to - timedelta(7)).strftime('%Y-%m-%d')
    date_from_plus = (date_from + timedelta(7)).strftime('%Y-%m-%d')
    date_to_plus = (date_to + timedelta(7)).strftime('%Y-%m-%d')
    return render(request, 'project/balances.html',
                  {'form': form, 'title': 'Балансы', 'datefrom': date_from_str, 'dateto': date_to_str, 'records': page_.object_list, 'date_from': date_from, 'date_to': date_to,
                   'page': page_number, 'pages': paginator, 'page_': page_, 'choice_filter': filtered_choice, 'cashregister': cashregister, 'cash': casharray, 'cashreg': cashreg,
                   'all_cash_in': all_cash_in, 'all_cash_flow': all_cash_flow, 'all_cash_income': all_cash_income, 'all_cash_out': all_cash_out, 'accounts': accarray,
                   'all_acc_in': all_acc_in, 'all_acc_flow': all_acc_flow, 'all_acc_income': all_acc_income, 'all_acc_out': all_acc_out,
                   'date_from_minus': date_from_minus, 'date_to_minus': date_to_minus, 'date_from_plus': date_from_plus, 'date_to_plus': date_to_plus})


@login_required
def filtered_concrete_delivery(request):
    date_from = None
    date_to = None
    supplier = None
    date_from_str = ''
    date_to_str = ''
    filtered_supplier = 0
    filtered_object = 0
    filtered_house = 0
    prepay_only = False
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_concrete and not is_manager:
        raise Http404

    user = request.user

    if request.method == 'POST':
        form = ConcreteForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            datefrom = cd['datefrom']
            dateto = cd['dateto']
            out_str = '?page=1'
            if datefrom is None or datefrom == '':
                pass
            else:
                out_str += '&from=' + str(datefrom)
            if dateto is None or dateto == '':
                pass
            else:
                out_str += '&to=' + str(dateto)

            supplier = cd['filter_supplier']
            if supplier is None:
                out_str += '&s=0'
            else:
                out_str += '&s=' + str(supplier.id)

            object_ = cd['object']
            if object_ is None:
                pass #out_str += '&o=0'
            else:
                out_str += '&o=' + str(object_.id)
            house_ = cd['house']
            if house_ is None:
                pass #out_str += '&o=0'
            else:
                out_str += '&h=' + str(house_.id)
            prepay_only_ = cd['prepay_only']
            if prepay_only_ is None:
                pass #out_str += '&o=0'
            else:
                out_str += '&a=' + str(prepay_only_)

            return HttpResponseRedirect(reverse('project:filteredconcretedelivery') + out_str)
    else:
        if 'from' in request.GET:
            date_from_str = request.GET.get('from', None)
            if date_from_str == 'None' or not CorrectDate(date_from_str):
                date_from = datetime.date(2020, 1, 1)
            else:
                date_from = datetime.datetime.strptime(date_from_str, "%Y-%m-%d")
        else:
            date_from = datetime.date(2020, 1, 1)

        if 'to' in request.GET:
            date_to_str = request.GET.get('to', None)
            if date_to_str == 'None' or not CorrectDate(date_to_str):
                date_to = datetime.date(2024, 12, 31)
            else:
                date_to = datetime.datetime.strptime(date_to_str, "%Y-%m-%d")
        else:
            date_to = datetime.date(2024, 12, 31)

        if 's' in request.GET:
            filtered_supplier_str = request.GET.get('s', 0)
            try:
                filtered_supplier = int(filtered_supplier_str)
            except:
                filtered_supplier = 0
        else:
            filtered_supplier = 0

        if 'o' in request.GET:
            filtered_object_str = request.GET.get('o', 0)
            try:
                filtered_object = int(filtered_object_str)
            except:
                filtered_object = 0
        else:
            filtered_object = 0

        if 'h' in request.GET:
            filtered_house_str = request.GET.get('h', 0)
            try:
                filtered_house = int(filtered_house_str)
            except:
                filtered_house = 0
        else:
            filtered_house = 0

        if 'a' in request.GET:
            prepay_only_str = request.GET.get('a', 'False')
            if prepay_only_str == 'True':
                prepay_only = True
            else:
                prepay_only = False
        else:
            prepay_only = False

        #start = time.time()

        if filtered_supplier:
            suppliers = (Prepayment.objects.filter(deleted=False, date__gte=date_from,date__lte=date_to, supplier__id=filtered_supplier).values('supplier__id', 'supplier__name').annotate(summary=Sum('summary')).order_by())
            delivery = (Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier).values('supplier__id', 'supplier__name', 'object_id', 'house_id').annotate(total_sum=F('price') * F('volume') + F('pumpsummary') + F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F('deliveryvolume')).order_by('supplier__id')) #.aggregate(summary=Sum('total_sum'))
        else:
            suppliers = (Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).values('supplier__id', 'supplier__name').annotate(summary=Sum('summary')).order_by())
            delivery = (Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).values('supplier__id', 'supplier__name', 'object_id', 'house_id').annotate(total_sum=F('price') * F('volume') + F('pumpsummary') + F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F('deliveryvolume')).order_by('supplier__id')) #.aggregate(summary=Sum('total_sum'))

        #print('1: ', time.time() - start)

        if filtered_object:
            suppliers = []
            delivery = delivery.filter(object_id=filtered_object)

        if filtered_house:
            suppliers = []
            delivery = delivery.filter(house_id=filtered_house)

        #print(suppliers)

        delivery_ = []
        supplierid = 0
        counter = -1
        for item in delivery:
            if item['supplier__id'] != supplierid:
                supplierid = item['supplier__id']
                delivery_.append({'supplier__id': supplierid, 'total_sum': item['total_sum'], 'supplier__name': item['supplier__name']})
                counter += 1
            else:
                delivery_[counter]['total_sum'] += item['total_sum']

        #print('2: ', time.time() - start)

        # тут надо дополнить оба массива поставщиками, которых не хватает (есть доставка, но нет платежей, и наоборот)
        del_, sup_ = [],[]
        for s_item in suppliers:
            found = False
            for d_item in delivery_:
                if s_item['supplier__id'] == d_item['supplier__id']:
                    found = True
            if not found:
                del_.append({'supplier__id': s_item['supplier__id'], 'total_sum': decimal.Decimal(0.0), 'supplier__name': s_item['supplier__name']})

        for d_item in delivery_:
            found = False
            for s_item in suppliers:
                if d_item['supplier__id'] == s_item['supplier__id']:
                    found = True
            if not found:
                sup_.append({'supplier__id': d_item['supplier__id'], 'summary': decimal.Decimal(0.0), 'supplier__name': d_item['supplier__name']})

        #print('3: ', time.time() - start)

        for item in del_:
            delivery_.append(item)
        suppliers_ = []
        for item in suppliers:
            suppliers_.append({'supplier__id': item['supplier__id'], 'summary': item['summary'], 'supplier__name': item['supplier__name']})
        for item in sup_:
            suppliers_.append(item)

        #print('4: ', time.time() - start)

        #print(sup_)
        #print(delivery_)

        #suppliers = (Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to,
        #                                       supplier__id=filtered_supplier).values('supplier__id',
        #                                                                              'supplier__name').annotate(
        #    summary=Sum('summary')).order_by())

        if filtered_supplier:
            #prepayments_ = Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier).order_by('-date')
            prepayments_2 = (Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier).values('supplier__name', 'date', 'comment', 'summary', 'id', 'owner__first_name', 'owner__last_name').order_by('-date'))
        else:
            #prepayments_ = Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).order_by('-date')
            prepayments_2 = (Prepayment.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).values('supplier__name', 'date', 'comment', 'summary', 'id', 'owner__first_name', 'owner__last_name').order_by('-date'))


        #print(prepayments_2)

        prepayments = []
        for item in prepayments_2:
            prepayments.append({'type': 1,
                                'supplier__name': item['supplier__name'],
                                'date': item['date'], 'comment': item['comment'],
                                'summary': item['summary'], 'id': item['id'], 'owner': (item['owner__first_name']+' '+item['owner__last_name']).strip()})
        #print(prepayments)
        if filtered_supplier:
            #records_ = Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier).order_by('-date')
            records_ = (Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to, supplier__id=filtered_supplier).values('supplier__name', 'house__name', 'object__name', 'owner__first_name', 'owner__last_name', 'volume', 'price', 'deliveryvolume', 'deliveryprice', 'pumpcomment', 'pumpsummary', 'pumptransfer', 'downtime', 'downtimecost', 'date', 'comment', 'pile', 'id', 'verified', 'concrete_grade').order_by('-date'))
        else:
            #records_ = Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).order_by('-date')
            records_ = (Delivery.objects.filter(deleted=False, date__gte=date_from, date__lte=date_to).values('supplier__name', 'house__name', 'object__name', 'owner__first_name', 'owner__last_name', 'volume', 'price', 'deliveryvolume', 'deliveryprice', 'pumpcomment', 'pumpsummary', 'pumptransfer', 'downtime', 'downtimecost', 'date', 'comment', 'pile', 'id', 'verified', 'concrete_grade').order_by('-date'))


        if filtered_object:
            records_ = records_.filter(object_id=filtered_object)
            prepayments = []
        #print(records_)


        if filtered_house:
            records_ = records_.filter(house_id=filtered_house)
            prepayments = []
        #print(records_)
        total_volume = 0
        total_sum = 0

        if prepay_only:
            #print(prepayments)
            total_sum = 0
            for item in prepayments:
                s = item['summary']
                #print(s)
                total_sum += s
                #prepayments += item['summary']

            #print(total_sum)
            records_ = []
        else:
            total_volume = records_.filter(deleted=False).aggregate(summary=Sum('volume'))["summary"]
            #print(total_volume)
            total_sum = (records_.filter(deleted=False).annotate(
                total_sum=F('price') * F('volume') + F('pumpsummary')+ F('pumptransfer') + F('downtime') * F('downtimecost') + F('deliveryprice') * F(
                    'deliveryvolume')).order_by('supplier__id')).aggregate(summary=Sum('total_sum'))["summary"]
            #print(total_sum)
        #total_sum = records_.filter(deleted=False).annotate aggregate(summary=Sum('volume'))["summary"]

        #print('5: ', time.time() - start)
        #print(records_)
        #print(records_2)

        records = []
        #print(len(records_))
        for item in records_:
            records.append({'type': 0,
                            'supplier__name': item['supplier__name'], 'house__name': item['house__name'],
                            'object__name': item['object__name'], 'volume': item['volume'], 'price': item['price'],
                            'deliveryvolume': item['deliveryvolume'],'deliveryprice': item['deliveryprice'],
                            'pumpcomment': item['pumpcomment'],'pumpsummary': item['pumpsummary'],
                            'pumptransfer': item['pumptransfer'], 'downtime': item['downtime'], 'downtimecost': item['downtimecost'],
                            'date': item['date'], 'comment': item['comment'],
                            'concretegrade': get_grade_display(item['concrete_grade']),
                            'pile': item['pile'], 'id': item['id'], 'owner': (item['owner__first_name']+' '+item['owner__last_name']).strip(),
                            'verified': item['verified']})

        #print('6: ', time.time() - start)

        res = []
        cp, cr = 0, 0
        lp, lr = len(prepayments), len(records)
        if prepayments or records:
            while True:
                if get_date_from_list(prepayments, cp, lp) > get_date_from_list(records, cr, lr):
                    res.append(prepayments[cp])
                    cp += 1
                else:
                    res.append(records[cr])
                    cr += 1
                if cp >= lp and cr >= lr:
                    break

        #print('7: ', time.time() - start)

        paginator = Paginator(res, 10)

        try:
            page_ = paginator.page(page_number)
        except:
            page_ = paginator.page(1)
            page_number = 1

        #print(filtered_supplier)

        form = ConcreteForm(initial={'datefrom': date_from, 'dateto': date_to, 'filter_supplier': filtered_supplier, 'object': filtered_object, 'house': filtered_house, 'prepay_only': prepay_only})
        date_from_str = date_from.strftime("%Y-%m-%d")

        #print('Time render: ', time.time() - start)

    return render(request, 'project/concrete.html',
                  {'form': form, 'title': 'Бетон', 'records': page_.object_list, 'page': page_number, 'pages': paginator,
                   'page_': page_, 'filter_supplier': filtered_supplier, 'suppliers': suppliers_, 'delivery': delivery_, 'datefrom': date_from_str, 'dateto': date_to_str, 'filtered_object': filtered_object, 'filtered_house': filtered_house, 'prepay_only': prepay_only, 'total_volume': total_volume, 'total_sum': total_sum})


@login_required
def new_prepayment(request):
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    object_ = request.GET.get('o')
    house_ = request.GET.get('h')
    error = ''
    if request.method == 'POST':
        form = PrepaymentForm(request.POST)
        if form.is_valid():
                new_pay_ = form.save(commit=False)
                #now = datetime.datetime.now()
                #new_pay_.date = now
                new_pay_.owner = request.user
                new_pay_.save()
                return HttpResponseRedirect(reverse('project:filteredconcretedelivery')) #+'?page='+str(page_number)+'&from='+str(date_from)+'&to='+str(date_to)+'&s='+str(supplier_id))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новый авансовый платёж',
                'page': page_number,
                'datefrom': date_from,
                'dateto': date_to,
                'filter_supplier': supplier_id,
                'filtered_object': object_,
                'filtered_house': house_,
            }
            return render(request, 'project/addpayment.html', context)

    form = PrepaymentForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Новый авансовый платёж',
        'page': page_number,
        'datefrom': date_from,
        'dateto': date_to,
        'filter_supplier': supplier_id,
        'filtered_object': object_,
        'filtered_house': house_,
    }
    return render(request, 'project/addpayment.html', context)


@login_required
def new_concrete_delivery(request):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()

    if not is_concrete:
        raise Http404


    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    object_ = request.GET.get('o')
    house_ = request.GET.get('h')

    error = ''
    if request.method == 'POST':
        form = ConcreteDeliveryForm(request.POST)
        if form.is_valid():
                new_delivery_ = form.save(commit=False)
                new_delivery_.owner = request.user

                correct_house = House.objects.get(id=new_delivery_.house_id)
                if correct_house.object_id == new_delivery_.object_id:
                    new_delivery_.verified = False
                    new_delivery_.save()
                    return HttpResponseRedirect(reverse('project:filteredconcretedelivery')) #+'?page='+str(page_number)+'&from='+str(date_from)+'&to='+str(date_to)+'&s='+str(supplier_id))
                else:
                    error = 'Дом не соответствует объекту!'
                    context = {
                        'form': form,
                        'error': error,
                        'title': 'Новая отгрузка',
                        'page': page_number,
                        'datefrom': date_from,
                        'dateto': date_to,
                        'filter_supplier': supplier_id,
                        'filtered_object': object_,
                        'filtered_house': house_,
                    }
                    return render(request, 'project/adddelivery.html', context)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новая отгрузка',
                'page': page_number,
                'datefrom': date_from,
                'dateto': date_to,
                'filter_supplier': supplier_id,
                'filtered_object': object_,
                'filtered_house': house_,
            }
            return render(request, 'project/adddelivery.html', context)

    form = ConcreteDeliveryForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Новая отгрузка',
        'page': page_number,
        'datefrom': date_from,
        'dateto': date_to,
        'filter_supplier': supplier_id,
        'filtered_object': object_,
        'filtered_house': house_,
    }
    return render(request, 'project/adddelivery.html', context)


@login_required
def concrete_delivery_edit(request, delivery_id):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()

    if not is_concrete:
        raise Http404


    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    object_ = request.GET.get('o')
    house_ = request.GET.get('h')
    prepay_only_ = request.GET.get('a')
    error = ''
    delivery_ = Delivery.objects.get(id=delivery_id)
    #arch_ = content_.archive
    is_manager = request.user.groups.filter(name='managers').exists()
    if delivery_.deleted:
        raise Http404
    #if delivery_.owner != request.user and not is_manager  and not is_concrete:
    #    raise Http404
    if request.method == 'POST':
        form = ConcreteDeliveryForm(request.POST, instance=delivery_)
        if form.is_valid():
            correct_house = House.objects.get(id=delivery_.house_id)
            if correct_house.object_id == delivery_.object_id:
                form.save()
                return HttpResponseRedirect(
                    reverse('project:filteredconcretedelivery') + '?page=' + str(page_number) + '&from=' + str(date_from)+'&to='+str(date_to)+'&s='+str(supplier_id)+'&o='+str(object_)+'&h='+str(house_)+'&a='+str(prepay_only_))
            else:
                #error = 'Дом '+ correct_house.name +' не соответствует объекту '+delivery_.house_id.name+'!'
                error = 'Дом не соответствует объекту!'
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Новая отгрузка',
                    'page': page_number,
                    'datefrom': date_from,
                    'dateto': date_to,
                    'filter_supplier': supplier_id,
                    'filtered_object': object_,
                    'filtered_house': house_,
                    'prepay_only': prepay_only_,
                    'delivery': delivery_
                }
                return render(request, 'project/editdelivery.html', context)
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                #'content': content_,
                #'title': 'Архивная заявка №' + str(arch_.number),
                'page': page_number,
                'datefrom': date_from,
                'dateto': date_to,
                'filter_supplier': supplier_id,
                'filtered_object': object_,
                'filtered_house': house_,
                'prepay_only': prepay_only_,
                'delivery': delivery_
            }
            return render(request, 'project/editdelivery.html', context)
    data = {'house': delivery_.house, 'date': delivery_.date, 'supplier': delivery_.supplier,
            'object': delivery_.object,
            'volume': delivery_.volume,
            'price': delivery_.price, 'pumpsummary': delivery_.pumpsummary, 'pumpcomment': delivery_.pumpcomment,
            'pumptransfer': delivery_.pumptransfer, 'downtime': delivery_.downtime, 'downtimecost': delivery_.downtimecost,
            'deliveryvolume': delivery_.deliveryvolume, 'deliveryprice': delivery_.deliveryprice,
            'pile': delivery_.pile, 'concrete_grade': delivery_.concrete_grade,
            'comment': delivery_.comment,
            'verified': delivery_.verified}
    form = ConcreteDeliveryForm(data)
    context = {
        'form': form,
        'error': error,
        #'arch': arch_,
        #'content': content_,
        #'title': 'Архивная заявка №' + str(arch_.number),
        'page': page_number,
        'datefrom': date_from,
        'dateto': date_to,
        'filter_supplier': supplier_id,
        'filtered_object': object_,
        'filtered_house': house_,
        'prepay_only': prepay_only_,
        'delivery': delivery_
    }
    return render(request, 'project/editdelivery.html', context)


@login_required
def concrete_delivery_delete(request, delivery_id):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()

    if not is_concrete:
        raise Http404


    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    object_ = request.GET.get('o')
    house_ = request.GET.get('h')
    prepay_only_ = request.GET.get('a')
    error = ''
    delivery_ = Delivery.objects.get(id=delivery_id)

    if delivery_.deleted:
        raise Http404

    delivery_.deleted = True
    delivery_.save()
    return HttpResponseRedirect(reverse('project:filteredconcretedelivery') + '?page=' + str(page_number) + '&from=' + str(date_from)+'&to='+str(date_to)+'&s='+str(supplier_id)+'&o='+str(object_)+'&h='+str(house_)+'&a='+str(prepay_only_))


def get_max_contracts():
    max_contract_number = Contract.objects.filter(deleted=False, type='a').extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')
    if max_contract_number:
        try:
            max_contract_a = str(int(max_contract_number[0].n) - 10000000 + 1)
        except:
            max_contract_a = '1'
    else:
        max_contract_a = '1'
    max_contract_number = Contract.objects.filter(deleted=False, type='b').extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')
    if max_contract_number:
        try:
            max_contract_b = str(int(max_contract_number[0].n) - 10000000 + 1)
        except:
            max_contract_b = '1'
    else:
        max_contract_b = '1'
    max_contract_number = Contract.objects.filter(deleted=False, type='c').extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')
    if max_contract_number:
        try:
            max_contract_c = str(int(max_contract_number[0].n) - 10000000 + 1)
        except:
            max_contract_c = '1'
    else:
        max_contract_c = '1'
    return max_contract_a, max_contract_b, max_contract_c


@login_required
def new_contract(request):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    rollback = request.GET.urlencode()

    error = []
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            num_ = form.cleaned_data['number']
            type_ = form.cleaned_data['type']
            found_contract = Contract.objects.filter(deleted=False, number=num_, type=type_)
            if found_contract:
                error.append('Уже есть контракт с номером ' + num_ + '!')
            new_contract_ = form.save(commit=False)
            new_contract_.owner = request.user

            correct_house = House.objects.get(id=new_contract_.house_id)
            if correct_house.object_id != new_contract_.object_id:
                error.append('Дом не соответствует объекту!')

            if not error:
                new_contract_.status = 'a'
                new_contract_.save()
                return HttpResponseRedirect(reverse('project:contracts'))
            else:
                max_contract_a, max_contract_b, max_contract_c = get_max_contracts()
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Новый контракт',
                    'rollback': rollback,
                    'max_contract_a': max_contract_a,
                    'max_contract_b': max_contract_b,
                    'max_contract_c': max_contract_c
                }
                return render(request, 'project/addcontract.html', context)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новый контракт',
                'rollback': rollback
            }
            return render(request, 'project/addcontract.html', context)

    max_contract_a, max_contract_b, max_contract_c = get_max_contracts()

    form = ContractForm(initial={'type': 'a', 'number': max_contract_a,})
    context = {
        'form': form,
        'error': error,
        'title': 'Новый контракт',
        'rollback': rollback,
        'max_contract_a': max_contract_a,
        'max_contract_b': max_contract_b,
        'max_contract_c': max_contract_c
    }
    return render(request, 'project/addcontract.html', context)


@login_required
def add_turnover(request, contract_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    rollback = request.GET.urlencode()

    contract_ = Contract.objects.get(id=contract_id)

    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.owner == request.user and contract_.status != 'a' and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    error = ''
    if request.method == 'POST':
        form = TurnoverForm(request.POST)
        if form.is_valid():
                new_turnover_ = form.save(commit=False)
                new_turnover_.contract = contract_
                new_turnover_.save()
                return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новая операция по контракту',
                'rollback': rollback,
                'contract': contract_
            }
            return render(request, 'project/addturnover.html', context)

    form = TurnoverForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Новая операция по контракту',
        'rollback': rollback,
        'contract': contract_
    }
    return render(request, 'project/addturnover.html', context)


@login_required
def add_checkimage(request, contract_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    rollback = request.GET.urlencode()

    contract_ = Contract.objects.get(id=contract_id)

    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404

    error = ''
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
                new_image_ = form.save(commit=False)
                new_image_.contract = contract_

                #print(new_image_.image.path.enc77ode('utf-8'))
                #instance = ContractImage(image=request.FILES['image'], date=new_image_.date, contract=contract_, comment=new_image_.comment)
                #instance.save()

                #filename = f'{request.user.username}_{datetime.datetime.now().strftime("%Y%m%d")}'
                #print(filename)
                #with open(filename, 'wb+') as destination:
                #    for chunk in new_image_.image.chunks():
                ##        destination.write(chunk)

                new_image_.save()
                return HttpResponseRedirect(reverse('project:contractreceipt', args=[contract_.id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Добавление изображения',
                'rollback': rollback,
                'contract': contract_
            }
            return render(request, 'project/addcheckimage.html', context)

    form = ImageUploadForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Добавление изображения',
        'rollback': rollback,
        'contract': contract_
    }
    return render(request, 'project/addcheckimage.html', context)


@login_required
def edit_contract(request, contract_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    contract_ = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    #is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.owner == request.user and contract_.status != 'a' and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    rollback = '&'.join(request.GET.urlencode().split('&')[1:])
    if rollback: rollback = '&' + rollback
    page_number = request.GET.get('page', 1)

    error = []
    if request.method == 'POST':
        form = ContractEditForm(request.POST, instance=contract_)

        if form.is_valid():
            new_contract_ = form.save(commit=False)
            #new_contract_.owner = request.user

            correct_house = House.objects.get(id=new_contract_.house_id)
            if correct_house.object_id != new_contract_.object_id:
                error.append('Дом не соответствует объекту!')

            if not error:
                new_contract_.save()
                return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + '?'+rollback)
            else:
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Корректировка контракта',
                    'page': page_number,
                    'rollback': rollback,
                    'contract': contract_
                }
                return render(request, 'project/editcontract.html', context)

        else:
            error.append('Неверные данные формы')
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка контракта',
                'page': page_number,
                'rollback': rollback,
                'contract': contract_
            }
            return render(request, 'project/editcontract.html', context)

    form = ContractEditForm(instance=contract_)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка контракта',
        'page': page_number,
        'rollback': rollback,
        'contract': contract_
    }
    return render(request, 'project/editcontract.html', context)


@login_required
def change_contract(request, contract_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    contract_ = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    #is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.owner == request.user and contract_.status != 'a' and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    rollback = '&'.join(request.GET.urlencode().split('&')[1:])
    if rollback: rollback = '&' + rollback
    page_number = request.GET.get('page', 1)

    error = []
    if request.method == 'POST':
        form = ContractChangeForm(request.POST, instance=contract_)

        if form.is_valid():
            num_ = form.cleaned_data['number']
            type_ = form.cleaned_data['type']
            found_contract = Contract.objects.filter(deleted=False, number=num_, type=type_)
            if found_contract:
                error.append('Уже есть контракт с номером ' + num_ + '!')
            new_contract_ = form.save(commit=False)

            if not error:
                new_contract_.save()
                return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + '?'+rollback)
            else:
                max_contract_a, max_contract_b, max_contract_c = get_max_contracts()
                context = {
                    'form': form,
                    'error': error,
                    'title': 'Смена типа договора',
                    'page': page_number,
                    'rollback': rollback,
                    'max_contract_a': max_contract_a,
                    'max_contract_b': max_contract_b,
                    'max_contract_c': max_contract_c,
                    'contract': contract_
                }
                return render(request, 'project/changecontract.html', context)

        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Смена типа договора',
                'page': page_number,
                'rollback': rollback,
                'contract': contract_
            }
            return render(request, 'project/changecontract.html', context)

    max_contract_a, max_contract_b, max_contract_c = get_max_contracts()

    form = ContractChangeForm(instance=contract_)
    context = {
        'form': form,
        'error': error,
        'title': 'Смена типа договора',
        'page': page_number,
        'rollback': rollback,
        'max_contract_a': max_contract_a,
        'max_contract_b': max_contract_b,
        'max_contract_c': max_contract_c,
        'contract': contract_
    }
    return render(request, 'project/changecontract.html', context)


@login_required
def revoke_contract(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()

    if contract_.deleted or contract_.revoked:
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404

    rollback = request.GET.urlencode()

    error = []
    if request.method == 'POST':
        form = ContractCommentForm(request.POST, instance=contract_)

        if form.is_valid():
            new_contract_ = form.save(commit=False)
            new_contract_.revoked = True
            new_contract_.status = 'd'
            new_contract_.save()
            return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Детали договора',
                'rollback': rollback,
                'contract': contract_
            }
            return render(request, 'project/revokecontract.html', context)

    form = ContractCommentForm(instance=contract_)
    context = {
        'form': form,
        'error': error,
        'title': 'Детали договора',
        'rollback': rollback,
        'contract': contract_
    }
    return render(request, 'project/revokecontract.html', context)


@login_required
def receipt_contract(request, contract_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    contract_ = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()

    is_headofsales = is_same_headofsales(request, contract_)
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if contract_.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    checks = contract_.contractimage_set.filter(deleted=False)

    rollback = request.GET.urlencode()

    error = []
    if request.method == 'POST':
        form = ContractReceiptForm(request.POST, instance=contract_)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Детали договора',
                'rollback': rollback,
                'contract': contract_,
                'checks': checks
            }
            return render(request, 'project/receiptcontract.html', context)

    form = ContractReceiptForm(instance=contract_)
    context = {
        'form': form,
        'error': error,
        'title': 'Детали договора',
        'rollback': rollback,
        'contract': contract_,
        'checks': checks
    }
    return render(request, 'project/receiptcontract.html', context)


@login_required
def edit_turnover(request, turnover_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    turnover_ = Turnover.objects.get(id=turnover_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    #is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    is_headofsales = is_same_headofsales(request, turnover_.contract)
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if turnover_.contract.owner == request.user and (turnover_.performed or turnover_.contract.status != 'a'):
        raise Http404
    if turnover_.contract.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    rollback = request.GET.urlencode()

    error = ''
    if request.method == 'POST':
        form = TurnoverForm(request.POST, instance=turnover_)
        if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка оборота по контракту',
                'rollback': rollback,
                'contract': turnover_.contract,
                'turnover': turnover_
            }
            return render(request, 'project/editturnover.html', context)

    form = TurnoverForm(instance=turnover_)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка оборота по контракту',
        'rollback': rollback,
        'contract': turnover_.contract,
        'turnover': turnover_
    }
    return render(request, 'project/editturnover.html', context)


@login_required
def edit_turnover_comment(request, turnover_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    turnover_ = Turnover.objects.get(id=turnover_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_headofsales = is_same_headofsales(request, turnover_.contract)
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.owner != request.user and not is_accountant and not is_boss and not is_headofsales:
        raise Http404
    if turnover_.contract.owner == request.user and turnover_.performed:
        raise Http404
    if turnover_.contract.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    rollback = request.GET.urlencode()

    error = ''
    if request.method == 'POST':
        form = TurnoverCommentOnlyForm(request.POST, instance=turnover_)
        if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + '?'+rollback)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка оборота по контракту',
                'rollback': rollback,
                'contract': turnover_.contract,
                'turnover': turnover_
            }
            return render(request, 'project/editturnovercomment.html', context)

    form = TurnoverCommentOnlyForm(instance=turnover_)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка оборота по контракту',
        'rollback': rollback,
        'contract': turnover_.contract,
        'turnover': turnover_
    }
    return render(request, 'project/editturnovercomment.html', context)


@login_required
def edit_turnover_perform(request, turnover_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    turnover_ = Turnover.objects.get(id=turnover_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    #is_headofsales = request.user.groups.filter(name='headsofsales').exists()
    is_headofsales = is_same_headofsales(request, turnover_.contract)
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if not is_accountant and not is_boss:
        raise Http404
    if turnover_.contract.owner == request.user and turnover_.performed and not is_accountant and not is_boss:
        raise Http404
    if turnover_.contract.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404

    rollback = request.GET.urlencode()

    error = ''
    if request.method == 'POST':
        form = TurnoverPerformedForm(request.POST, instance=turnover_)
        if form.is_valid():
                new_turnover_ = form.save(commit=False)
                cd = form.cleaned_data
                status = cd['performed']
                actualdate = cd['actualdate']

                #if status and not actualdate:
                #    error =

                if status:
                    if actualdate:
                        new_turnover_.save()
                        if turnover_.type >= 100:
                            return HttpResponseRedirect(reverse('project:turnoverexpense', args=[turnover_.id]) + '?' + rollback)
                        else:
                            return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + '?' + rollback)
                    else:
                        error = 'Не указана дата совершения операции!'
                else:
                    new_turnover_.actualdate = None
                    new_turnover_.save()
                    return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + '?'+rollback)
                if error:
                    context = {
                        'form': form,
                        'error': error,
                        'title': 'Корректировка оборота по контракту',
                        'rollback': rollback,
                        'contract': turnover_.contract,
                        'turnover': turnover_
                    }
                return render(request, 'project/editperform.html', context)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка оборота по контракту',
                'rollback': rollback,
                'contract': turnover_.contract,
                'turnover': turnover_
            }
            return render(request, 'project/editperform.html', context)

    form = TurnoverPerformedForm(instance=turnover_)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка оборота по контракту',
        'rollback': rollback,
        'contract': turnover_.contract,
        'turnover': turnover_
    }
    return render(request, 'project/editperform.html', context)


@login_required
def turnover_expense(request, turnover_id):
    is_seller = request.user.groups.filter(name='sellers').exists()

    if not is_seller:
        raise Http404

    turnover_ = Turnover.objects.get(id=turnover_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if not is_accountant and not is_boss:
        raise Http404
    #if turnover_.performed:
    #    raise Http404

    rollback = request.GET.urlencode()

    context = {
        'title': 'Создание заявки по контракту',
        'rollback': rollback,
        'contract': turnover_.contract,
        'turnover': turnover_,
        'bid': turnover_.bid
    }
    return render(request, 'project/turnoverexpense.html', context)


@login_required
def arch_delete(request, arch_id):
    arch_ = Archive.objects.get(id=arch_id)

    is_manager = request.user.groups.filter(name='managers').exists()
    if arch_.deleted:
        raise Http404
    if not is_manager:
        raise Http404

    page_number = request.GET.get('page')
    number = request.GET.get('q')
    try:
        num_ = int(number)
    except:
        num_ = 0
    error = ''

    arch_.deleted = True
    arch_.save()
    if not num_:
        return HttpResponseRedirect(
            reverse('project:archive') + '?page=' + str(page_number) + '&q=' + str(number))
    else:
        return HttpResponseRedirect(reverse('project:found') + '?q=' + str(number))


@login_required
def contract_accept(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if not is_accountant and not is_boss:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.status = 'b'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_restore(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    if contract_.deleted:
        raise Http404
    if not contract_.revoked:
        raise Http404
    if not is_boss:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.status = 'c'
    contract_.revoked = False
    contract_.comment = ''
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_execute(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'b':
        raise Http404
    if not is_boss:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.status = 'c'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_performed(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'c':
        raise Http404
    if contract_.owner != request.user and not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.status = 'd'
    contract_.save()
    return HttpResponseRedirect(reverse('project:contracts') + rollback)


@login_required
def contract_return(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'b' and contract_.status != 'c':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    if contract_.status == 'c':
        contract_.status = 'b'
    else:
        contract_.status = 'a'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_open(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'd':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.status = 'c'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_delete(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_headofsales = is_same_headofsales(request, contract_)

    if contract_.deleted or contract_.revoked:
        raise Http404
    performed = contract_.turnover_set.filter(deleted=False, performed=True).count()
    if performed > 0:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if contract_.owner != request.user and not is_boss and not is_accountant and not is_headofsales:
        raise Http404
    if contract_.reservation_type == 'c' and not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    contract_.deleted = True
    contract_.save()
    return HttpResponseRedirect(reverse('project:contracts') + rollback)


@login_required
def contract_reservation(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_headofsales = is_same_headofsales(request, contract_)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if contract_.deleted or contract_.revoked:
        raise Http404
    performed = contract_.turnover_set.filter(deleted=False, performed=True).count()
    if performed > 0:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if contract_.owner != request.user and not is_headofsales and not is_boss and not is_accountant:
        raise Http404
    if contract_.reservation_type != 'a':
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    contract_.reservation_type = 'b'
    now = datetime.datetime.now()
    contract_.reservation_date = now
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_unreservation(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_headofsales = is_same_headofsales(request, contract_)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if contract_.deleted or contract_.revoked:
        raise Http404
    performed = contract_.turnover_set.filter(deleted=False, performed=True).count()
    if performed > 0:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if contract_.owner != request.user and not is_headofsales and not is_boss and not is_accountant:
        raise Http404
    if contract_.reservation_type != 'b':
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    contract_.reservation_type = 'a'
    now = datetime.datetime.now()
    contract_.reservation_date = None
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_reservation_accept(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()

    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if contract_.reservation_type != 'b':
        raise Http404
    if not is_boss:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    contract_.reservation_type = 'c'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


@login_required
def contract_reservation_takeout(request, contract_id):
    contract_ = Contract.objects.get(id=contract_id)
    is_boss = request.user.groups.filter(name='bosses').exists()

    if contract_.deleted or contract_.revoked:
        raise Http404
    if contract_.status != 'a':
        raise Http404
    if contract_.reservation_type != 'c':
        raise Http404
    if not is_boss:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    contract_.reservation_type = 'a'
    contract_.reservation_date = None
    contract_.status = 'a'
    contract_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[contract_.id]) + rollback)


def get_settings(name, settingtype):
    setting = Setting.objects.filter(name=name)
    if setting:
        if setting[0].type == 1:
            return int(setting[0].value)
        elif setting[0].type == 2:
            return setting[0].value
        elif setting[0].type == 3:
            return setting[0].value == 'True'
        else:
            return datetime.datetime.strptime(setting[0].value, "%Y-%m-%d")
    else:
        if settingtype == 1:
            return 0
        elif settingtype == 2:
            return ''
        elif settingtype == 3:
            return False
        else:
            return datetime.datetime.strptime('2024-12-31', "%Y-%m-%d")

@login_required
def turnover_accept(request, turnover_id):
    turnover_ = Turnover.objects.get(id=turnover_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.status != 'b':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    turnover_.performed = True
    turnover_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + rollback)


@login_required
def turnover_bid_create(request, turnover_id):
    turnover_ = Turnover.objects.get(id=turnover_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.status != 'c':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    # создаём заявку
    contract = turnover_.contract
    if turnover_.type == 101:
        comission = "Комиссия агента "
    else:
        comission = "Комиссия эксклюзив "
    housenumber = contract.house.name.replace('Дом', '').replace('№', '').replace(' ', '')
    title = comission + contract.get_type_display() + "-" + contract.number + " литер " + housenumber + " кв " + contract.apartment + " " + contract.client
    now = datetime.datetime.now()
    max_bid_number = Bid.objects.filter(deleted=False).extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')[0]
    try:
        max_bid = str(int(max_bid_number.n) - 10000000 + 1)
    except:
        max_bid = ''
    bid = Bid(title=title, date=now, object=contract.object, owner=request.user, locked=False, deleted=False, number=max_bid, highlighted=False, supervision=False, supervisor='')
    bid.save()

    # 176 6 84 / 249 6 84
    if turnover_.type == 101:
        supplier = Supplier.objects.get(id=get_settings('supplier_agency_comission', 1))
        phase = Phase.objects.get(id=get_settings('phase_agency_comission', 1))
        estimate = Estimate.objects.get(id=get_settings('estimate_agency_comission', 1))
    else:
        supplier = Supplier.objects.get(id=get_settings('supplier_exclusive_comission', 1))
        phase = Phase.objects.get(id=get_settings('phase_exclusive_comission', 1))
        estimate = Estimate.objects.get(id=get_settings('estimate_exclusive_comission', 1))

    content = Content(title=title, date=turnover_.actualdate, type='f', cash='y', quantity=1, measure='on',
                      price=turnover_.amount, comment=title, bid=bid, house=contract.house, deleted=False,
                      supplier=supplier, phase=phase, estimate=estimate, history='', subcash=None, credit_account=None,
                      expense_account=None, prepaid=False)
    content.save()

    turnover_.bid = bid
    turnover_.save()

    return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + rollback)


@login_required
def turnover_return_perform(request, turnover_id):
    turnover_ = Turnover.objects.get(id=turnover_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.status != 'c':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback

    turnover_.performed = False
    turnover_.save()

    return HttpResponseRedirect(reverse('project:turnovereditperform', args=[turnover_.id]) + rollback)
    #return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + rollback)


@login_required
def turnover_return(request, turnover_id):
    turnover_ = Turnover.objects.get(id=turnover_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.status != 'a':
        raise Http404
    if not is_boss and not is_accountant:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    turnover_.performed = False
    turnover_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + rollback)


@login_required
def turnover_delete(request, turnover_id):
    turnover_ = Turnover.objects.get(id=turnover_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()
    is_headofsales = is_same_headofsales(request, turnover_.contract)

    if turnover_.contract.deleted or turnover_.contract.revoked:
        raise Http404
    if turnover_.deleted:
        raise Http404
    if turnover_.contract.owner != request.user and not is_boss and not is_accountant and not is_headofsales:
        raise Http404
    rollback = request.GET.urlencode()
    if rollback: rollback = '?' + rollback
    turnover_.deleted = True
    turnover_.save()
    return HttpResponseRedirect(reverse('project:onecontract', args=[turnover_.contract_id]) + rollback)


@login_required
def details_delete(request, detail_id):
    content_ = ArchiveDetail.objects.get(id=detail_id)
    arch_ = content_.archive
    is_manager = request.user.groups.filter(name='managers').exists()
    if arch_.deleted:
        raise Http404
    if not is_manager:
        raise Http404
    if content_.deleted:
        raise Http404

    page_number = request.GET.get('page')
    number = request.GET.get('q')
    error = ''

    content_.deleted = True
    content_.save()
    #return HttpResponseRedirect(reverse('project:filteredconcretedelivery') + '?page=' + str(page_number) + '&from=' + str(date_from))
    return HttpResponseRedirect(
        reverse('project:onearchiveitem', args=[arch_.id]) + '?page=' + str(page_number) + '&q=' + str(number))



@login_required
def prepayment_edit(request, prepayment_id):
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    object_ = request.GET.get('o')
    house_ = request.GET.get('h')
    prepay_only_ = request.GET.get('a')

    error = ''
    prepayment_ = Prepayment.objects.get(id=prepayment_id)
    #arch_ = content_.archive
    is_manager = request.user.groups.filter(name='managers').exists()
    if prepayment_.deleted:
        raise Http404
    #if prepayment_.owner != request.user and not is_manager:
    #    raise Http404
    if request.method == 'POST':
        form = PrepaymentForm(request.POST, instance=prepayment_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('project:filteredconcretedelivery') + '?page=' + str(page_number) + '&from=' + str(date_from)+'&to='+str(date_to)+'&s='+str(supplier_id)+'&o='+str(object_)+'&h='+str(house_)+'&a='+str(prepay_only_))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                #'content': content_,
                #'title': 'Архивная заявка №' + str(arch_.number),
                'page': page_number,
                'datefrom': date_from,
                'dateto': date_to,
                'filter_supplier': supplier_id,
                'filtered_object': object_,
                'filtered_house': house_,
                'prepay_only_': prepay_only_,
            }
            return render(request, 'project/editpayment.html', context)
    data = {'date': prepayment_.date, 'supplier': prepayment_.supplier,
            'summary': prepayment_.summary,
            'comment': prepayment_.comment}
    form = PrepaymentForm(data)
    context = {
        'form': form,
        'error': error,
        #'arch': arch_,
        #'content': content_,
        #'title': 'Архивная заявка №' + str(arch_.number),
        'page': page_number,
        'datefrom': date_from,
        'dateto': date_to,
        'filter_supplier': supplier_id,
        'filtered_object': object_,
        'filtered_house': house_,
        'prepay_only_': prepay_only_,
    }
    return render(request, 'project/editpayment.html', context)


class BookCreateView(BSModalCreateView):
    template_name = 'project/create_book.html'
    form_class = BookModelForm
    success_message = 'Success: Book was created.'
    success_url = reverse_lazy('project:bids')


class HouseDetailView(BSModalFormView):
    template_name = 'project/view_house.html'
    form_class = HouseDetailModelForm
    success_message = 'Success: House!'
    success_url = reverse_lazy('project:bids')


class BidsArchSearchView(BSModalFormView):
    template_name = 'project/view_search.html'
    form_class = BidsSearchForm
    #success_url = reverse_lazy('project:bids')

    def form_valid(self, form):
        self.filter = '?q=' + form.cleaned_data['number']
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        return reverse_lazy('project:bids') + self.filter


@login_required
def houses(request):
    error = ''
    if request.method == 'POST':
        form = TForm(request.POST)
        if form.is_valid():
            return redirect('project:requests')
        else:
            error = 'Неверные данные формы'
    form = TForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'project/houses.html', context)


@login_required
def suppliers(request):
    is_bosses = request.user.groups.filter(name='bosses').exists()

    if not is_bosses:
        raise Http404

    selected = request.GET.get('s')
    try:
        selected_ = int(selected)
    except:
        selected_ = 0
    suppliers = Supplier.objects.all()
    #houses = House.objects.all().order_by('object__id')

    return render(request, 'project/suppliers.html', {'title': 'Поставщики',
                                                    'selected': selected_,
                                                  'objects': suppliers})


@login_required
def supplier_edit(request, supplier_id):
    is_bosses = request.user.groups.filter(name='bosses').exists()

    if not is_bosses:
        raise Http404
    #bid_.locked = True
    #bid_.save()
    return HttpResponseRedirect(reverse('project:suppliers'))


@login_required
def objects(request):
    is_bosses = request.user.groups.filter(name='bosses').exists()

    if not is_bosses:
        raise Http404

    selected = request.GET.get('s')
    try:
        selected_ = int(selected)
    except:
        selected_ = 0
    objects = Object.objects.all()
    houses = House.objects.all().order_by('object__id')

    return render(request, 'project/objects.html', {'title': 'Объекты/дома',
                                                    'selected': selected_,
                                                  'objects': objects,
                                                  'houses': houses})




    #return render(request, 'project/suppliers.html', {'title': 'Поставщики',
    #                                                'selected': selected_,
    #                                              'objects': suppliers})


@login_required
def house_add(request, object_id):
    error = ''
    object_ = Object.objects.get(id=object_id)
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            new_house_ = form.save(commit=False)
            new_house_.object = object_
            new_house_.save()
            return HttpResponseRedirect(reverse('project:objects'))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error
            }
            return render(request, 'project/addhouse.html', context)
    form = HouseForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'project/addhouse.html', context)


@login_required
def house_add_modal(request, object_id):

    object_ = Object.objects.get(id=object_id)
    if request.method == 'POST':
        form = HouseForm(request.POST)
        if form.is_valid():
            new_house_ = form.save(commit=False)
            new_house_.object = object_
            new_house_.save()
            return HttpResponseRedirect(reverse('project:objects'))
        else:
            # error = 'Неверные данные формы'
            context = {
                'form': form,
                #'error': error
            }
            return render(request, 'project/addhousemodal.html', context)
    form = HouseForm()
    context = {
        'form': form,
        #'error': error
    }
    return render(request, 'project/addhousemodal.html',
                  {'title': 'Добавление нового дома к объекту', 'object': object_})


class HouseCreateView(BSModalCreateView):

    template_name = 'project/addhousemodal.html'
    form_class = HouseModelForm
    success_message = 'Успех: новый дом создан.'
    success_url = reverse_lazy('project:objects')

    object_ = None

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(HouseCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()


    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            obj = self.kwargs['object_id']
            house = form.save(commit=False)
            object_ = Object.objects.get(id=obj)
            house.object = object_
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                house.save()
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


class HouseUpdateView(BSModalUpdateView):
    model = House
    template_name = 'project/edithousemodal.html'
    form_class = HouseModelForm
    success_message = 'Успех: изменения по дому произведены.'
    success_url = reverse_lazy('project:objects')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(HouseUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()

    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            house = form.save(commit=False)
            obj = house.object.id
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                house.save()
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


class SupplierUpdateView(BSModalUpdateView):
    model = Supplier
    template_name = 'project/editsuppliermodal.html'
    form_class = SupplierModelForm
    success_message = 'Успех: изменения по поставщику произведены.'
    success_url = reverse_lazy('project:suppliers')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        is_accountant = request.user.groups.filter(name='accountants').exists()
        is_supplier = request.user.groups.filter(name='suppliers').exists()
        if is_boss or is_accountant or is_supplier:
            return super(SupplierUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()

    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            obj = Supplier.objects.get(pk=form.instance.pk)
            prev_name = copy.copy(obj).name

            supplier = form.save(commit=False)
            obj = supplier.id
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            is_accountant = self.request.user.groups.filter(name='accountants').exists()
            is_supplier = self.request.user.groups.filter(name='suppliers').exists()
            if is_boss or is_accountant or is_supplier:
                supplier.comment = prev_name + "|" + supplier.comment
                supplier.save()
        filter = self.request.GET.get('f')
        #print(self.success_url + '/#item' + str(obj) + '?f=' + filter)
        return HttpResponseRedirect(self.success_url + '?f=' + filter)


class SupplierRemoveView(BSModalUpdateView):
    model = Supplier
    template_name = 'project/removesuppliermodal.html'
    form_class = SupplierRemoveModelForm
    success_message = 'Успех: изменения поставщика в заявках произведены.'
    success_url = reverse_lazy('project:supplierreport')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_accountant = request.user.groups.filter(name='accountants').exists()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_accountant or is_boss:
            return super(SupplierRemoveView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()

    def form_valid(self, form):
        obj = 0
        filter = self.request.GET.get('f')
        if not self.request.is_ajax():
            obj = Supplier.objects.get(pk=form.instance.pk)
            prev_name = copy.copy(obj).name
            newsupplier = form.cleaned_data['newsupplier']

            supplier = form.save(commit=False)
            obj = supplier.id
            is_accountant = self.request.user.groups.filter(name='accountants').exists()
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_accountant or is_boss:


                #supplier.comment = prev_name + "|" + supplier.comment
                #supplier.save()
                #print(obj,'-->',newsupplier.id)
                if obj != newsupplier.id:
                    content = Content.objects.filter(deleted=False, supplier_id=obj)
                    with transaction.atomic():
                        for item in content:
                            history = item.history + '|' + str(obj)
                            Content.objects.filter(id=item.id).update(supplier_id=newsupplier.id, history=history)

                    archive = ArchiveDetail.objects.filter(deleted=False, new_supplier_id=obj)
                    with transaction.atomic():
                        for item in archive:
                            history = item.history + '|' + str(obj)
                            ArchiveDetail.objects.filter(id=item.id).update(new_supplier_id=newsupplier.id, history=history)

                    delivery = Delivery.objects.filter(deleted=False, supplier_id=obj)
                    with transaction.atomic():
                        for item in delivery:
                            history = item.history + '|' + str(obj)
                            Delivery.objects.filter(id=item.id).update(supplier_id=newsupplier.id, history=history)

                    prepay = Prepayment.objects.filter(deleted=False, supplier_id=obj)
                    with transaction.atomic():
                        for item in prepay:
                            history = item.history + '|' + str(obj)
                            Prepayment.objects.filter(id=item.id).update(supplier_id=newsupplier.id, history=history)
                else:
                    return HttpResponseRedirect(self.success_url + '?f=' + filter+ '&e=1')
                supplier.hidden = True
                supplier.save()
        return HttpResponseRedirect(self.success_url + '?f=' + filter)


class EstimateUpdateView(BSModalUpdateView):
    model = Estimate
    template_name = 'project/editestimatemodal.html'
    form_class = EstimateModelForm
    success_message = 'Успех: изменения по смете произведены.'
    success_url = reverse_lazy('project:estimates')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(EstimateUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()

    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            obj = Estimate.objects.get(pk=form.instance.pk)
            prev_name = copy.copy(obj).name
            #print(prev_name)
            estimate = form.save(commit=False)
            #old_name = estimate.name
            obj = estimate.id
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                estimate.comment = prev_name + "|" + estimate.comment
                estimate.save()
        filter = self.request.GET.get('f')
        #print(self.success_url + '/#item' + str(obj) + '?f=' + filter)
        return HttpResponseRedirect(self.success_url + '?f=' + filter)


class PhaseUpdateView(BSModalUpdateView):
    model = Phase
    template_name = 'project/editphasemodal.html'
    form_class = EstimateModelForm
    success_message = 'Успех: изменения по этапу строительства произведены.'
    success_url = reverse_lazy('project:phases')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(PhaseUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()

    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            obj = Phase.objects.get(pk=form.instance.pk)
            prev_name = copy.copy(obj).name
            phase = form.save(commit=False)
            obj = phase.id
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                phase.comment = prev_name + "|" + phase.comment
                phase.save()
        filter = self.request.GET.get('f')
        return HttpResponseRedirect(self.success_url + '?f=' + filter)


class ObjectCreateView(BSModalCreateView):
    model = Object
    template_name = 'project/addobjectmodal.html'
    form_class = ObjectModelForm
    success_message = 'Успех: объект добавлен.'
    success_url = reverse_lazy('project:objects')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(ObjectCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()


    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            object_ = form.save(commit=False)
            #user = self.request.user
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                object_.save()
                obj = object_.id
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


class SupplierCreateView(BSModalCreateView):
    model = Supplier
    template_name = 'project/addsuppliermodal.html'
    form_class = SupplierModelForm
    success_message = 'Успех: поставщик добавлен.'
    success_url = reverse_lazy('project:suppliers')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        is_accountant = request.user.groups.filter(name='accountants').exists()
        is_supplier = request.user.groups.filter(name='suppliers').exists()
        if is_boss or is_accountant or is_supplier:
            return super(SupplierCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()


    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            object_ = form.save(commit=False)
            #user = self.request.user
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            is_accountant = self.request.user.groups.filter(name='accountants').exists()
            is_supplier = self.request.user.groups.filter(name='suppliers').exists()
            if is_boss or is_accountant or is_supplier:
                object_.save()
                obj = object_.id
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


class EstimateCreateView(BSModalCreateView):
    model = Estimate
    template_name = 'project/addestimatemodal.html'
    form_class = EstimateModelForm
    success_message = 'Успех: смета добавлена.'
    success_url = reverse_lazy('project:estimates')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(EstimateCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()


    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            object_ = form.save(commit=False)
            #user = self.request.user
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                object_.save()
                obj = object_.id
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


class PhaseCreateView(BSModalCreateView):
    model = Phase
    template_name = 'project/addphasemodal.html'
    form_class = PhaseModelForm
    success_message = 'Успех: этап добавлен.'
    success_url = reverse_lazy('project:phases')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseRedirect()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(PhaseCreateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseRedirect()


    def form_valid(self, form):
        obj = 0
        if not self.request.is_ajax():
            object_ = form.save(commit=False)
            #user = self.request.user
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                object_.save()
                obj = object_.id
        return HttpResponseRedirect(self.success_url + '?s=' + str(obj))


@login_required
def samples(request):
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    sample_id_str = request.GET.get('i', 0)
    try:
        sample_id = int(sample_id_str)
    except:
        sample_id = 0

    data = Sample.objects.filter(deleted=False).order_by('id')
    #details = SampleDetail.objects.filter(deleted=False).order_by('sample_id')

    #print(details)

    return render(request, 'project/samples.html',
                  {'title': 'Шаблоны заказов', 'samples': data, 'sample_id': sample_id})


@login_required
def sample_add(request):
    error = ''
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    prev_ = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        form = SampleForm(request.POST)
        if form.is_valid():
            new_sample_ = form.save(commit=False)
            form.save()
            return HttpResponseRedirect(reverse('project:samples')+'?i='+str(new_sample_.id))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'prev': prev_
            }
            return render(request, 'project/addsample.html', context)

    form = SampleForm()
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'prev': prev_
    }

    return render(request, 'project/addsample.html', context)


@login_required
def sampledetail_add(request, sample_id):
    error = ''
    sample_ = Sample.objects.get(id=sample_id)
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    if sample_.deleted:
        raise Http404

    if request.method == 'POST':
        form = SampleDetailForm(request.POST)
        if form.is_valid():
            new_sampledetail_ = form.save(commit=False)
            new_sampledetail_.sample = sample_
            new_sampledetail_.save()
            return HttpResponseRedirect(reverse('project:samples')+'?i='+str(sample_.id))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'sample': sample_
            }
            return render(request, 'project/addsampledetail.html', context)

    form = SampleDetailForm()
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'sample': sample_
    }
    return render(request, 'project/addsampledetail.html', context)


@login_required
def sampledetail_edit(request, sampledetail_id):
    error = ''
    sampledetail_ = SampleDetail.objects.get(id=sampledetail_id)
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    if sampledetail_.deleted:
        raise Http404
    if request.method == 'POST':
        form = SampleDetailForm(request.POST, instance=sampledetail_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:samples')+'?i='+str(sampledetail_.sample.id))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'sample': sampledetail_.sample,
                'detail': sampledetail_
            }
            return render(request, 'project/editsampledetail.html', context)
    data = {'code': sampledetail_.code, 'description': sampledetail_.description, 'quantity': sampledetail_.quantity, 'measure': sampledetail_.measure,
            'price': sampledetail_.price}
    form = SampleDetailForm(data)
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'sample': sampledetail_.sample,
        'detail': sampledetail_
    }
    return render(request, 'project/editsampledetail.html', context)


@login_required
def sample_edit(request, sample_id):
    error = ''
    sample_ = Sample.objects.get(id=sample_id)
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    if sample_.deleted:
        raise Http404
    if request.method == 'POST':
        form = SampleForm(request.POST, instance=sample_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:samples')+'?i='+str(sample_.id))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'sample': sample_
            }
            return render(request, 'project/editsample.html', context)
    data = {'title': sample_.title, 'hidden': sample_.hidden}
    form = SampleForm(data)
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'sample': sample_
    }
    return render(request, 'project/editsample.html', context)


@login_required
def estimate_delete(request, estimate_id):
    estimate_ = Estimate.objects.get(id=estimate_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    filter = request.GET.get('f')


    if not is_boss:
        raise Http404

    details = Content.objects.filter(estimate_id=estimate_id, deleted=False).count()
    archive = ArchiveDetail.objects.filter(estimate_id=estimate_id, deleted=False).count()

    if (details + archive) == 0:
        estimate_.deleted = True
        estimate_.hidden = True
        estimate_.save()
        return HttpResponseRedirect(reverse('project:estimates')+'?f='+filter)
    else:
        return HttpResponseRedirect(reverse('project:estimates')+'?f='+filter+'&e=1')


@login_required
def phase_delete(request, phase_id):
    phase_ = Phase.objects.get(id=phase_id)
    is_boss = request.user.groups.filter(name='bosses').exists()
    filter = request.GET.get('f')


    if not is_boss:
        raise Http404

    details = Content.objects.filter(phase_id=phase_id, deleted=False).count()
    archive = ArchiveDetail.objects.filter(phase_id=phase_id, deleted=False).count()

    if (details + archive) == 0:
        phase_.deleted = True
        phase_.hidden = True
        phase_.save()
        return HttpResponseRedirect(reverse('project:phases')+'?f='+filter)
    else:
        return HttpResponseRedirect(reverse('project:phases')+'?f='+filter+'&e=1')


@login_required
def sample_del(request, sample_id):
    sample_ = Sample.objects.get(id=sample_id)
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    sample_.deleted = True
    sample_.save()
    return HttpResponseRedirect(reverse('project:samples'))


@login_required
def sampledetail_del(request, sampledetail_id):
    sampledetail_ = SampleDetail.objects.get(id=sampledetail_id)
    is_manager = request.user.groups.filter(name='managers').exists()

    if not is_manager:
        raise Http404

    sampledetail_.deleted = True
    sampledetail_.save()
    return HttpResponseRedirect(reverse('project:samples')+'?i='+str(sampledetail_.sample.id))


@login_required
def orders(request):
    is_concrete = request.user.groups.filter(name='concrete').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_supplier = request.user.groups.filter(name='suppliers').exists()
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if not is_concrete and not is_boss and not is_supplier and not is_accountant:
        raise Http404

    page_number = request.GET.get('page')

    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            status = cd['status']
            if status == '':
                return HttpResponseRedirect(reverse('project:orders'))
            else:
                return HttpResponseRedirect(reverse('project:orders') + '?f=' + str(status))
        else:
            context = {
                'form': form,
            }
            return render(request, 'project/orders.html', context)

    status_str = request.GET.get('f', 'None')

    STATUS_boss = (
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
        ('6'),
        ('7'),
    )
    STATUS_supplier = (
        ('2'),
        ('3'),
        ('4'),
        ('5'),
        ('6'),
        ('7'),
    )
    STATUS_accountant = (
        ('3'),
        ('4'),
        ('5'),
        ('6'),
        ('7'),
    )
    STATUS_not_completed = (
        ('0'),
        ('1'),
        ('2'),
        ('3'),
        ('4'),
        ('5'),
        ('6'),
    )

    if is_concrete:
        # порабам надо выбрать только их собственные заказы
        data = Order.objects.filter(deleted=False, owner=request.user).order_by('-id')
    if is_boss:
        # начальнику выбираем все, кроме созданных прорабами + свои собственные, если начальник создал заказ сам
        data = Order.objects.filter(deleted=False).order_by('-id')
        data = data.filter(Q(owner=request.user) | Q(status__in=STATUS_boss))
    if is_supplier:
        # снабженцу выбираем только переданные ему, переданные бухгалтеру, в доставке и завершенные
        data = Order.objects.filter(deleted=False).order_by('-id')
        data = data.filter(Q(status__in=STATUS_supplier))
    if is_accountant:
        # бухгалтеру выбираем только переданные ему, в доставке и завершенные
        data = Order.objects.filter(deleted=False).order_by('-id')
        data = data.filter(Q(status__in=STATUS_accountant))


    if status_str != 'None':
        if status_str != 'x':
            data = data.filter(Q(status=status_str))
        else:
            data = data.filter(Q(status__in=STATUS_not_completed))

    # если выбран фильтр, то применяем его
    paginator = Paginator(data, 10)

    try:
        page_ = paginator.page(page_number)
    except:
        page_ = paginator.page(1)
        page_number = 1

    form = OrdersForm(initial={'status': status_str,})
    choices = Order.STATUSES
    choices = ((None, '-----'),) + choices + (('x', 'Все незавершённые'),)
    form.fields['status'].choices = choices
    context = {
        'form': form,
        'orders': page_.object_list, 'page': page_number, 'pages': paginator, 'page_': page_, 'status': status_str
    }
    return render(request, 'project/orders.html', context)




@login_required
def new_order(request):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()

    if not is_concrete:
        raise Http404

    page_number = request.GET.get('page')
    supplier_id = request.GET.get('s')
    date_from = request.GET.get('from')
    date_to = request.GET.get('to')
    samples = Sample.objects.filter(deleted=False, hidden=False).order_by('id')
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
                cd = form.cleaned_data
                agreement = cd['agreement']
                new_order_ = form.save(commit=False)

                correct_house = House.objects.get(id=new_order_.house_id)
                if correct_house.object_id == new_order_.object_id:
                    new_order_.owner = request.user
                    now = datetime.datetime.now()
                    new_order_.date = now
                    new_order_.lastdate = now
                    new_order_.status ='0'

                    new_order_.save()

                    sample = cd['sample']
                    sampledetails = SampleDetail.objects.filter(sample=sample, deleted=False).order_by('sample_id')
                    for item in sampledetails:
                        d = OrderDetail(title=item.description, code=item.code, quantity=item.quantity, sample_quantity=item.quantity, measure=item.measure, price=item.price, order_id=new_order_.id)
                        d.save()

                    if agreement:
                        return HttpResponseRedirect(reverse('project:onapproval', args=[new_order_.id]))
                    else:
                        return HttpResponseRedirect(reverse('project:orders'))
                else:
                    error = 'Дом не соответствует объекту!'
                    context = {
                        'form': form,
                        'error': error,
                        'title': 'Новый заказ',
                        'samples': samples
                    }
                    return render(request, 'project/addorder.html', context)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Новый заказ',
                'samples': samples
            }
            return render(request, 'project/addorder.html', context)

    form = OrderForm()
    context = {
        'form': form,
        'error': error,
        'title': 'Новый заказ',
        'samples': samples
    }
    return render(request, 'project/addorder.html', context)


@login_required
def edit_order(request, order_id):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()
    is_boss = request.user.groups.filter(name='bosses').exists()

    if not is_concrete and not is_boss:
        raise Http404

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    if order_.owner.id != request.user.id:
        raise Http404

    status_str = request.GET.get('f', 'None')

    sample = order_.sample

    samples = Sample.objects.filter(deleted=False, hidden=False).order_by('id')
    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                agreement = cd['agreement']
                new_sample = cd['sample']
                new_order_ = form.save(commit=False)

                correct_house = House.objects.get(id=new_order_.house_id)
                if correct_house.object_id == new_order_.object_id:
                    now = datetime.datetime.now()
                    new_order_.lastdate = now
                    new_order_.save()

                    # если пользователь поменял наблон в заказе, то надо обновить детали
                    if new_sample != sample:
                        orderdetails = OrderDetail.objects.filter(order=new_order_).order_by('id')
                        orderdetails.delete()
                        sampledetails = SampleDetail.objects.filter(sample=new_sample, deleted=False).order_by('sample_id')
                        for item in sampledetails:
                            d = OrderDetail(title=item.description, code=item.code, quantity=item.quantity, sample_quantity=item.quantity, measure=item.measure, order_id=new_order_.id)
                            d.save()

                    # блок согласований/изменения статуса заказа
                    if is_concrete and new_order_.owner.id == request.user.id:
                        if agreement:
                            return HttpResponseRedirect(reverse('project:onapproval', args=[order_.id])+'?page='+str(page_number)+'&f='+str(status_str))
                        else:
                            return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
                    else:
                        return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
                else:
                    error = 'Дом не соответствует объекту!'
                    context = {
                        'form': form,
                        'error': error,
                        'title': 'Новый заказ',
                        'samples': samples,
                        'details': orderdetails,
                        'order': order_,
                        'page': page_number,
                        'status': status_str
                    }
                    return render(request, 'project/editorder.html', context)
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'samples': samples,
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'status': status_str
            }
            return render(request, 'project/editorder.html', context)

    agreement = order_.status in ('1','2')
    data = {'comment': order_.comment, 'sample': order_.sample, 'object': order_.object, 'house': order_.house, 'agreement': agreement}
    form = OrderForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'samples': samples,
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'status': status_str
    }
    return render(request, 'project/editorder.html', context)


@login_required
def on_approval(request, order_id):
    page_number = request.GET.get('page')
    is_concrete = request.user.groups.filter(name='concrete').exists()

    if not is_concrete:
        raise Http404

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    status_str = request.GET.get('f', 'None')

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    error = ''
    if request.method == 'POST':
        form = OnApprovalForm(request.POST, instance=order_)
        if form.is_valid():
                new_order_ = form.save(commit=False)

                correct_house = House.objects.get(id=new_order_.house_id)
                now = datetime.datetime.now()
                new_order_.lastdate = now
                new_order_.status = '1'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'status': status_str
            }
            return render(request, 'project/on_approval.html', context)

    #agreement = order_.status in ('1','2')
    data = {'comment': order_.comment, }
    form = OnApprovalForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'status': status_str
    }
    return render(request, 'project/on_approval.html', context)


@login_required
def order_resolve(request, order_id):
    page_number = request.GET.get('page')
    is_boss = request.user.groups.filter(name='bosses').exists()

    if not is_boss:
        raise Http404

    status_str = request.GET.get('f', 'None')

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    error = ''
    if request.method == 'POST':
        form = ResolveForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                resolve = cd['like']
                new_order_ = form.save(commit=False)

                now = datetime.datetime.now()
                new_order_.lastdate = now
                if resolve == 'option3':
                    new_order_.status = '2'
                else:
                    if resolve == 'option1':
                        new_order_.status = '0'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'status': status_str
            }
            return render(request, 'project/resolve.html', context)

    #agreement = order_.status in ('1','2')
    data = {'comment': order_.comment, 'like': 'option2'}
    form = ResolveForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'status': status_str
    }
    return render(request, 'project/resolve.html', context)


@login_required
def order_processing(request, order_id):
    page_number = request.GET.get('page')
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if not is_boss and not is_supplier:
        raise Http404

    status_str = request.GET.get('f', 'None')

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    summary = OrderDetail.objects.filter(order=order_, deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    #print(summary)
    error = ''
    if request.method == 'POST':
        form = ProcessingForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                resolve = cd['like']
                new_order_ = form.save(commit=False)

                now = datetime.datetime.now()
                new_order_.lastdate = now
                if resolve == 'option3':
                    if new_order_.supplier:
                        new_order_.status = '3'
                    else:
                        error = 'Выберите поставщика!'
                        context = {
                            'form': form,
                            'error': error,
                            'title': 'Корректировка заказа',
                            'details': orderdetails,
                            'order': order_,
                            'page': page_number,
                            'sum': summary,
                            'status': status_str
                        }
                        return render(request, 'project/processing.html', context)
                else:
                    if resolve == 'option1':
                        new_order_.status = '1'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'sum': summary,
                'status': status_str
            }
            return render(request, 'project/processing.html', context)

    data = {'comment': order_.comment, 'supplier': order_.supplier, 'like': 'option2'}
    form = ProcessingForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'sum': summary,
        'status': status_str
    }
    return render(request, 'project/processing.html', context)


@login_required
def order_closing(request, order_id):
    page_number = request.GET.get('page')
    is_boss = request.user.groups.filter(name='bosses').exists()
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if not is_boss and not is_supplier:
        raise Http404

    status_str = request.GET.get('f', 'None')

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    summary = OrderDetail.objects.filter(order=order_, deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    #print(summary)
    error = ''
    if request.method == 'POST':
        form = ClosingForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                resolve = cd['like']
                estimate = cd['estimate']
                phase = cd['phase']

                new_order_ = form.save(commit=False)

                now = datetime.datetime.now()
                new_order_.lastdate = now
                if resolve == 'option3':
                    if estimate and phase:
                        max_bid_number = Bid.objects.filter(deleted=False).extra({'n': "10000000+CAST(number as TEXT)"}).order_by('-n')[0]
                        try:
                            max_bid = str(int(max_bid_number.n) - 10000000 + 1)
                        except:
                            max_bid = ''

                        new_bid = Bid(title=new_order_.sample.title + ' (' + new_order_.house.name + ', заказ #' + str(new_order_.id) + ')', date=new_order_.lastdate, object=new_order_.object, owner=new_order_.owner, locked=True, deleted=False, highlighted=False, number=max_bid)
                        new_bid.save()

                        orderdetails_ = OrderDetail.objects.filter(deleted=False, order=new_order_).order_by('id')
                        for item in orderdetails_:
                            if item.quantity > 0:
                                new_orderdetail = Content(title=item.title, date=new_order_.lastdate, type='a', cash='n', quantity=item.quantity, price=item.price, measure=item.measure, comment=item.code, bid=new_bid, house=new_order_.house, deleted=False, supplier=new_order_.supplier, phase=phase, estimate=estimate)
                                new_orderdetail.save()


                        new_order_.status = '7'
                    else:
                        error = 'Не выбрана смета или этап строительства!'
                        context = {
                            'form': form,
                            'error': error,
                            'title': 'Корректировка заказа',
                            'details': orderdetails,
                            'order': order_,
                            'page': page_number,
                            'sum': summary,
                            'status': status_str
                        }
                        return render(request, 'project/closing.html', context)
                else:
                    if resolve == 'option1':
                        new_order_.status = '4'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'sum': summary,
                'status': status_str
            }
            return render(request, 'project/closing.html', context)

    data = {'comment': order_.comment, 'like': 'option2'}
    form = ClosingForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'sum': summary,
        'status': status_str
    }
    return render(request, 'project/closing.html', context)


@login_required
def order_receiving(request, order_id):
    page_number = request.GET.get('page')
    is_concreter = request.user.groups.filter(name='concrete').exists()

    if not is_concreter:
        raise Http404

    status_str = request.GET.get('f', 'None')

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    if order_.status != '4':
        raise Http404

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    summary = OrderDetail.objects.filter(order=order_, deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))

    error = ''
    if request.method == 'POST':
        form = ReceivingForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                resolve = cd['like']
                new_order_ = form.save(commit=False)

                now = datetime.datetime.now()
                new_order_.lastdate = now
                if resolve == 'option3':
                    new_order_.status = '6'
                else:
                    if resolve == 'option1':
                        new_order_.status = '5'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'sum': summary,
                'status': status_str
            }
            return render(request, 'project/receiving.html', context)

    data = {'comment': order_.comment, 'like': 'option2'}
    form = ReceivingForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'sum': summary,
        'status': status_str
    }
    return render(request, 'project/receiving.html', context)


@login_required
def order_completion(request, order_id):
    page_number = request.GET.get('page')
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if not is_supplier:
        raise Http404

    status_str = request.GET.get('f', 'None')

    order_ = Order.objects.get(id=order_id)
    if order_.deleted:
        raise Http404

    if order_.status not in ('5', '6'):
        raise Http404

    orderdetails = OrderDetail.objects.filter(order=order_).order_by('id')
    summary = OrderDetail.objects.filter(order=order_, deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))

    error = ''
    if request.method == 'POST':
        form = ReceivingForm(request.POST, instance=order_)
        if form.is_valid():
                cd = form.cleaned_data
                resolve = cd['like']
                new_order_ = form.save(commit=False)

                now = datetime.datetime.now()
                new_order_.lastdate = now
                if resolve == 'option3':
                    new_order_.status = '6'
                else:
                    if resolve == 'option1':
                        new_order_.status = '5'
                new_order_.save()
                return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            error = 'Неверные данные формы'
            context = {
                'form': form,
                'error': error,
                'title': 'Корректировка заказа',
                'details': orderdetails,
                'order': order_,
                'page': page_number,
                'sum': summary,
                'status': status_str
            }
            return render(request, 'project/receiving.html', context)

    data = {'comment': order_.comment, 'like': 'option2'}
    form = ReceivingForm(data)
    context = {
        'form': form,
        'error': error,
        'title': 'Корректировка заказа',
        'details': orderdetails,
        'order': order_,
        'page': page_number,
        'sum': summary,
        'status': status_str
    }
    return render(request, 'project/receiving.html', context)


class OrderDetailUpdateView(BSModalUpdateView):
    model = OrderDetail
    template_name = 'project/editorderdetailmodal.html'
    form_class = OrderDetailModelForm
    success_message = 'Успех: изменения по детали заказа произведены.'
    success_url = reverse_lazy('project:onapproval')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden()
        is_concreter = request.user.groups.filter(name='concrete').exists()
        if is_concreter:
            return super(OrderDetailUpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def form_valid(self, form):
        order = 0
        orderdetail = None
        page_number = self.request.GET.get('page', None)
        status_str = self.request.GET.get('f', 'None')
        if not self.request.is_ajax():
            orderdetail = form.save(commit=False)
            order = orderdetail.order.id
            is_concreter = self.request.user.groups.filter(name='concrete').exists()
            if is_concreter:
                orderdetail.save()
                order = orderdetail.order.id
        else:
            orderdetail = form.save(commit=False)
            order = orderdetail.order.id
        return HttpResponseRedirect(reverse('project:onapproval', args=[order])+'?page='+str(page_number)+'&f='+str(status_str))


class OrderDetail_resolve_UpdateView(BSModalUpdateView):
    model = OrderDetail
    template_name = 'project/editorderdetailmodal.html'
    form_class = OrderDetailModelForm
    success_message = 'Успех: изменения по детали заказа произведены.'
    success_url = reverse_lazy('project:orderresolve')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponseForbidden()
        is_boss = request.user.groups.filter(name='bosses').exists()
        if is_boss:
            return super(OrderDetail_resolve_UpdateView, self).dispatch(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def form_valid(self, form):
        order = 0
        orderdetail = None
        page_number = self.request.GET.get('page', None)
        status_str = self.request.GET.get('f', 'None')
        if not self.request.is_ajax():
            orderdetail = form.save(commit=False)
            order = orderdetail.order.id
            is_boss = self.request.user.groups.filter(name='bosses').exists()
            if is_boss:
                orderdetail.save()
                order = orderdetail.order.id
        else:
            orderdetail = form.save(commit=False)
            order = orderdetail.order.id
        return HttpResponseRedirect(reverse('project:orderresolve', args=[order])+'?page='+str(page_number)+'&f='+str(status_str))


@login_required
def order_del(request, order_id):
    order_ = Order.objects.get(id=order_id)
    is_boss = request.user.groups.filter(name='bosses').exists()

    if order_.deleted:
        raise Http404

    if order_.owner != request.user and not is_boss:
        raise Http404

    if order_.status != '0':
        raise Http404

    order_.deleted = True
    order_.save()
    return HttpResponseRedirect(reverse('project:orders'))


@login_required
def orderdetail_del(request, orderdetail_id):
    orderdetail_ = OrderDetail.objects.get(id=orderdetail_id)
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if orderdetail_.deleted:
        raise Http404

    if not is_supplier:
        raise Http404

    if orderdetail_.order.status != '2':
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    orderdetail_.deleted = True
    orderdetail_.save()
    return HttpResponseRedirect(reverse('project:orderprocessing', args=[orderdetail_.order.id])+'?page='+str(page_number)+'&f='+str(status_str))


@login_required
def orderdetailconcreter_del(request, orderdetail_id):
    orderdetail_ = OrderDetail.objects.get(id=orderdetail_id)
    is_concreter = request.user.groups.filter(name='concrete').exists()

    if orderdetail_.deleted:
        raise Http404

    if not is_concreter:
        raise Http404

    if orderdetail_.order.status != '4':
        raise Http404

    if orderdetail_.order.owner != request.user:
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    orderdetail_.deleted = True
    orderdetail_.save()
    return HttpResponseRedirect(reverse('project:orderreceiving', args=[orderdetail_.order.id])+'?page='+str(page_number)+'&f='+str(status_str))


@login_required
def orderdetail_add(request, order_id):
    error = ''
    order_ = Order.objects.get(id=order_id)
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if not is_supplier:
        raise Http404

    if order_.status != '2':
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    if request.method == 'POST':
        form = OrderDetailForm(request.POST)
        if form.is_valid():
            new_orderdetail_ = form.save(commit=False)

            new_orderdetail_.order = order_
            form.save()
            return HttpResponseRedirect(reverse('project:orderprocessing', args=[order_.id])+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'page': page_number,
                'status': status_str,
                'order': order_
            }
            return render(request, 'project/addorderdetail.html', context)

    #data = {'title': orderdetail_.title, 'code': orderdetail_.code, 'quantity': orderdetail_.quantity, 'measure': orderdetail_.measure, 'price': orderdetail_.price}
    form = OrderDetailForm()
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'page': page_number,
        'status': status_str,
        'order': order_
    }
    return render(request, 'project/addorderdetail.html', context)


@login_required
def orderdetailconcreter_add(request, order_id):
    error = ''
    order_ = Order.objects.get(id=order_id)
    is_concreter = request.user.groups.filter(name='concrete').exists()

    if not is_concreter:
        raise Http404

    if order_.status != '4':
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    if request.method == 'POST':
        form = OrderDetailForm(request.POST)
        if form.is_valid():
            new_orderdetail_ = form.save(commit=False)

            new_orderdetail_.order = order_
            form.save()
            return HttpResponseRedirect(reverse('project:orderreceiving', args=[order_.id])+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'page': page_number,
                'status': status_str,
                'order': order_
            }
            return render(request, 'project/addorderdetailconcreter.html', context)

    form = OrderDetailForm()
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'page': page_number,
        'status': status_str,
        'order': order_
    }
    return render(request, 'project/addorderdetailconcreter.html', context)


@login_required
def orderdetail_edit(request, orderdetail_id):
    error = ''
    orderdetail_ = OrderDetail.objects.get(id=orderdetail_id)
    is_supplier = request.user.groups.filter(name='suppliers').exists()

    if not is_supplier:
        raise Http404

    if orderdetail_.deleted or orderdetail_.order.deleted:
        raise Http404

    if orderdetail_.order.status != '2':
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    if request.method == 'POST':
        form = OrderDetailForm(request.POST, instance=orderdetail_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:orderprocessing', args=[orderdetail_.order.id])+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'page': page_number,
                'status': status_str,
                'orderdetail': orderdetail_
            }
            return render(request, 'project/editorderdetail.html', context)

    data = {'title': orderdetail_.title, 'code': orderdetail_.code, 'quantity': orderdetail_.quantity, 'measure': orderdetail_.measure, 'price': orderdetail_.price}
    form = OrderDetailForm(data)
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'page': page_number,
        'status': status_str,
        'orderdetail': orderdetail_
    }
    return render(request, 'project/editorderdetail.html', context)


@login_required
def orderdetail_concreter_edit(request, orderdetail_id):
    error = ''
    orderdetail_ = OrderDetail.objects.get(id=orderdetail_id)
    is_concreter = request.user.groups.filter(name='concrete').exists()

    if not is_concreter:
        raise Http404

    if orderdetail_.deleted or orderdetail_.order.deleted:
        raise Http404

    if orderdetail_.order.status != '4':
        raise Http404

    if orderdetail_.order.owner != request.user:
        raise Http404

    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')

    if request.method == 'POST':
        form = OrderDetailForm(request.POST, instance=orderdetail_)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('project:orderreceiving', args=[orderdetail_.order.id])+'?page='+str(page_number)+'&f='+str(status_str))
        else:
            context = {
                'form': form,
                'error': error,
                'title': '-----',
                'page': page_number,
                'status': status_str,
                'orderdetail': orderdetail_
            }
            return render(request, 'project/editorderdetailconcreter.html', context)

    data = {'title': orderdetail_.title, 'code': orderdetail_.code, 'quantity': orderdetail_.quantity, 'measure': orderdetail_.measure, 'price': orderdetail_.price}
    form = OrderDetailForm(data)
    context = {
        'form': form,
        'error': error,
        'title': '-----',
        'page': page_number,
        'status': status_str,
        'orderdetail': orderdetail_
    }
    return render(request, 'project/editorderdetailconcreter.html', context)


@login_required
def order_payment(request, order_id):
    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')
    order_ = Order.objects.get(id=order_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if order_.deleted:
        raise Http404

    if not is_accountant:
        raise Http404

    if order_.status != '3':
        raise Http404

    order_.status = '4'
    now = datetime.datetime.now()
    order_.lastdate = now
    order_.save()
    return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))


@login_required
def order_return(request, order_id):
    page_number = request.GET.get('page')
    status_str = request.GET.get('f', 'None')
    order_ = Order.objects.get(id=order_id)
    is_accountant = request.user.groups.filter(name='accountants').exists()

    if order_.deleted:
        raise Http404

    if not is_accountant:
        raise Http404

    if order_.status != '3':
        raise Http404

    order_.status = '2'
    now = datetime.datetime.now()
    order_.lastdate = now
    order_.save()
    return HttpResponseRedirect(reverse('project:orders')+'?page='+str(page_number)+'&f='+str(status_str))