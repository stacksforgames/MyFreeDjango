from django.urls import path, include
from django.conf.urls import url
from . import views
from .views import HousesAutocomplete
from .views import SuppliersAutocomplete
from dal import autocomplete
from .models import Goods
from .models import Object
from .models import House
from .models import Supplier

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


app_name = 'project'


class LinkedDataView(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return House.objects.none()

        qs = House.objects.all()
        object_ = self.forwarded.get('object', None)

        if object_:
            qs = qs.filter(object_id=object_)

        return qs


urlpatterns = [
    url(
        r'^goods-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=Goods),
        # GoodsAutocomplete.as_view(),
        name='select_goods',
    ),
    url(
        r'^objects-autocomplete/$',
        autocomplete.Select2QuerySetView.as_view(model=Object),
        # GoodsAutocomplete.as_view(),
        name='select_object',
    ),
    url(
        r'^houses-autocomplete/$',
        # autocomplete.Select2QuerySetView.as_view(model=House),
        HousesAutocomplete.as_view(),
        name='select_house',
    ),
    url(
        r'^suppliers-autocomplete/$',
        #autocomplete.Select2QuerySetView.as_view(model=Supplier),
        #SuppliersAutocomplete.as_view(create_field='name'),
        SuppliersAutocomplete.as_view(),
        name='select_supplier',
    ),
    url(
        r'^suppliers-autocomplete-view/$',
        SuppliersAutocomplete.as_view(),
        name='select_supplier_view',
    ),
    url(
        '^linked_data/$',
        LinkedDataView.as_view(model=House),
        name='linked_data'
    ),

    path('requests/<int:request_id>/add/', views.details_add, name='detailsadd'),
    path('requests/<int:request_id>/', views.one_request, name='onerequest'),
    path('requests/add', views.new_request, name='newrequest'),
    path('requests/', views.requests, name='requests'),

    path('content/<int:content_id>/delete/', views.contents_delete, name='contentsdelete'),
    path('content/<int:content_id>/edit/', views.contents_edit, name='contentsedit'),
    path('content/<int:content_id>/copy/', views.contents_copy, name='contentscopy'),
    path('content/<int:content_id>/expense/', views.edit_expense_transaction, name='editexpensetransaction'),
    path('content/<int:content_id>/erase/', views.erase_expense_transaction, name='eraseexpensetransaction'),

    path('bids/<int:bid_id>/edit/', views.bid_edit, name='bidedit'),
    path('bids/<int:bid_id>/delete/', views.bid_del, name='biddel'),
    path('bids/<int:bid_id>/report/', views.bid_report, name='bidreport'),
    path('bids/<int:bid_id>/unlock/', views.bid_unlock, name='bidunlock'),
    path('bids/<int:bid_id>/mark/', views.bid_mark, name='bidmark'),
    path('bids/<int:bid_id>/unmark/', views.bid_unmark, name='bidunmark'),

    path('bids/<int:bid_id>/hide/', views.bid_hide, name='bidhide'),
    path('bids/<int:bid_id>/unhide/', views.bid_unhide, name='bidunhide'),

    path('bids/<int:bid_id>/refund/', views.bid_refund, name='bidrefund'),
    path('bids/<int:bid_id>/cancel/', views.bid_cancel_refund, name='bidcancelrefund'),

    path('bids/<int:bid_id>/sign/', views.bid_sign, name='bidsign'),
    path('bids/<int:bid_id>/lock/', views.bid_lock, name='bidlock'),
    path('bids/<int:bid_id>/add/', views.contents_add, name='contentsadd'),
    path('bids/<int:bid_id>/delivery/', views.bid_delivery, name='biddelivery'),
    path('bids/<int:bid_id>/', views.one_bid, name='onebid'),
    path('bids/add/', views.new_bid, name='newbid'),
    path('bids/', views.filtered_bids, name='bids'),

    path('contract/<int:contract_id>/image/<int:image_id>/', views.view_image, name='viewimage'),
    path('contract/<int:contract_id>/image/<int:image_id>/del/', views.delete_image, name='deleteimage'),

    path('turnover/<int:turnover_id>/goback/', views.turnover_return_perform, name='turnoverreturnperform'),
    path('turnover/<int:turnover_id>/bid/', views.turnover_bid_create, name='turnoverbidcreate'),
    path('turnover/<int:turnover_id>/expense/', views.turnover_expense, name='turnoverexpense'),
    path('turnover/<int:turnover_id>/delete/', views.turnover_delete, name='turnoverdelete'),
    path('turnover/<int:turnover_id>/accept/', views.turnover_accept, name='turnoveraccept'),
    path('turnover/<int:turnover_id>/return/', views.turnover_return, name='turnoverreturn'),
    path('turnover/<int:turnover_id>/perform/', views.edit_turnover_perform, name='turnovereditperform'),
    path('turnover/<int:turnover_id>/edit/', views.edit_turnover, name='turnoveredit'),
    path('turnover/<int:turnover_id>/comment/', views.edit_turnover_comment, name='turnovercommentedit'),
    path('contract/<int:contract_id>/report/', views.contract_report, name='contractreport'),
    path('contract/<int:contract_id>/return/', views.contract_return, name='contractreturn'),
    path('contract/<int:contract_id>/delete/', views.contract_delete, name='contractdelete'),
    path('contract/<int:contract_id>/open/', views.contract_open, name='contractopen'),
    path('contract/<int:contract_id>/performed/', views.contract_performed, name='contractperformed'),
    path('contract/<int:contract_id>/execute/', views.contract_execute, name='contractexecute'),
    path('contract/<int:contract_id>/onreserve/', views.contract_reservation, name='contractreservation'),
    path('contract/<int:contract_id>/unreserve/', views.contract_unreservation, name='contractunreservation'),
    path('contract/<int:contract_id>/reserve/', views.contract_reservation_accept, name='contractreserveaccept'),
    path('contract/<int:contract_id>/takeout/', views.contract_reservation_takeout, name='contractreservetakeout'),
    path('contract/<int:contract_id>/accept/', views.contract_accept, name='contractaccept'),
    path('contract/<int:contract_id>/turnover/', views.add_turnover, name='turnoveradd'),
    path('contract/<int:contract_id>/addimage/', views.add_checkimage, name='addcheckimage'),
    path('contract/<int:contract_id>/edit/', views.edit_contract, name='contractedit'),
    path('contract/<int:contract_id>/change/', views.change_contract, name='contractchange'),
    path('contract/<int:contract_id>/receipt/', views.receipt_contract, name='contractreceipt'),
    path('contract/<int:contract_id>/revoke/', views.revoke_contract, name='contractrevoke'),
    path('contract/<int:contract_id>/restore/', views.contract_restore, name='contractrestore'),
    path('contract/<int:contract_id>/', views.one_contract, name='onecontract'),
    path('contracts/add/', views.new_contract, name='contractadd'),
    path('contracts/', views.filtered_contracts, name='contracts'),

    path('contractsexport/', views.contracts_export, name='contractsexport'),
    path('bidsexport/', views.bids_export, name='bidsexport'),
    #path('transferobject/', views.transfer_object, name='transferobject'),
    #path('fill_delivered_bids/', views.fill_delivered_bids_, name='fill_delivered_bids'),
    #path('fill_performed_turnovers/', views.fill_performed_turnovers_, name='fill_performed_turnovers'),
    #path('fill_completed_contracts/', views.fill_completed_contracts_, name='fill_completed_contracts'),

    path('detail/<int:detail_id>/edit/', views.details_edit, name='detailsedit'),
    path('detail/<int:detail_id>/delete/', views.details_delete, name='detailsdelete'),
    path('archive/<int:arch_id>/delete/', views.arch_delete, name='archdelete'),
    path('archive/<int:arch_id>/edit/', views.arch_edit, name='archedit'),
    path('archive/<int:arch_id>/', views.one_archive_item, name='onearchiveitem'),
    path('archive/', views.archive, name='archive'),

    path('prepayment/<int:prepayment_id>/edit/', views.prepayment_edit, name='prepaymentedit'),
    path('prepayment/add/', views.new_prepayment, name='newprepayment'),
    path('concrete/<int:delivery_id>/edit/', views.concrete_delivery_edit, name='concretedeliveryedit'),
    path('concrete/<int:delivery_id>/delete/', views.concrete_delivery_delete, name='concretedeliverydelete'),
    path('concrete/add/', views.new_concrete_delivery, name='newdconcretedelivery'),
    path('concrete/', views.filtered_concrete_delivery, name='filteredconcretedelivery'),

    path('balances/', views.filtered_balances, name='filteredbalances'),
    path('subcash/<int:subcash_id>/edit/', views.edit_subcash, name='subcashedit'),
    path('subcash/add/', views.new_subcash, name='newsubcash'),
    path('subcash/', views.filtered_subcashes, name='filteredsubcashes'),

    path('earning/<int:earning_id>/edit/', views.edit_earning_transaction, name='editearningtransaction'),
    path('earning/add/', views.create_earning_transaction, name='newearning'),
    path('account/<int:account_id>/edit/', views.edit_account, name='accountedit'),
    path('account/add/', views.new_account, name='newaccount'),
    path('account/', views.filtered_accounts, name='filteredaccounts'),

    path('report/house/<int:house_id>/<int:estimate_id>/<int:phase_id>/<str:type>/<str:exclusion>/', views.house_estimate_report, name='houseestimatereport'),
    path('phasereport/house/<int:house_id>/<int:phase_id>/<int:estimate_id>/<str:type>/<str:exclusion>/', views.house_phase_report, name='housephasereport'),
    path('report/house/<int:house_id>/concrete/', views.house_concrete_report, name='houseconcretereport'),
    path('report/house/<int:house_id>/', views.house_report, name='housereport'),
    path('supplier/<int:supplier_id>/report', views.supplier_detail_xls_report, name='supplierdetailxlsreport'),

    path('supplier/<int:pk>/edit/', views.SupplierUpdateView.as_view(), name='suppliereditmodal'),
    path('supplier/<int:pk>/remove/', views.SupplierRemoveView.as_view(), name='supplierremovemodal'),
    path('estimate/<int:pk>/edit/', views.EstimateUpdateView.as_view(), name='estimateeditmodal'),
    path('phase/<int:pk>/edit/', views.PhaseUpdateView.as_view(), name='phaseeditmodal'),
    path('estimate/<int:estimate_id>/delete/', views.estimate_delete, name='estimatedelete'),
    path('phase/<int:phase_id>/delete/', views.phase_delete, name='phasedelete'),

    path('supplier/<int:supplier_id>/', views.supplier_detail_report, name='supplierdetailreport'),
    path('supplier/add/', views.SupplierCreateView.as_view(), name='supplieraddmodal'),
    path('estimate/add/', views.EstimateCreateView.as_view(), name='estimateaddmodal'),
    path('phase/add/', views.PhaseCreateView.as_view(), name='phaseaddmodal'),
    path('supplier/', views.supplier_report, name='supplierreport'),
    path('report/', views.report, name='report'),
    path('phasereport/', views.phase_report, name='phasereport'),
    #path('report2/', views.report2, name='report2'),
    #path('search/', views.BidsArchSearchView.as_view(), name='search'),
    #path('objects/<int:object_id>/add/', views.house_add_modal, name='houseaddmodal'),
    path('objects/<int:object_id>/add/', views.HouseCreateView.as_view(), name='houseaddmodal'),
    path('house/<int:pk>/edit/', views.HouseUpdateView.as_view(), name='houseditmodal'),
    path('objects/add/', views.ObjectCreateView.as_view(), name='objectaddmodal'),
    path('objects/', views.objects, name='objects'),
    path('sampledetail/<int:sampledetail_id>/edit/', views.sampledetail_edit, name='sampledetailedit'),
    path('sampledetail/<int:sampledetail_id>/del/', views.sampledetail_del, name='sampledetaildel'),
    path('samples/<int:sample_id>/edit/', views.sample_edit, name='sampleedit'),
    path('samples/<int:sample_id>/delete/', views.sample_del, name='sampledel'),
    path('samples/<int:sample_id>/add/', views.sampledetail_add, name='sampledetailadd'),
    path('samples/add/', views.sample_add, name='sampleadd'),
    path('samples/', views.samples, name='samples'),
    path('orderdetail/<int:orderdetail_id>/delete/', views.orderdetailconcreter_del, name='orderdetailconcreterdel'),
    path('orderdetail/<int:orderdetail_id>/del/', views.orderdetail_del, name='orderdetaildel'),
    path('orderdetail/<int:orderdetail_id>/c/', views.orderdetail_concreter_edit, name='editorderconcreterdetail'),
    path('orderdetail/<int:orderdetail_id>/', views.orderdetail_edit, name='editorderdetail'),
    path('orderdetail/<int:pk>/edit/', views.OrderDetailUpdateView.as_view(), name='orderdetaileditmodal'),
    path('orderdetail/<int:pk>/resolve/', views.OrderDetail_resolve_UpdateView.as_view(), name='orderdetailresolveeditmodal'),
    path('orderdetail/<int:order_id>/add/', views.orderdetail_add, name='orderdetailadd'),
    path('orderdetail/<int:order_id>/addplus/', views.orderdetailconcreter_add, name='orderdetailaddconcreter'),
    path('orders/<int:order_id>/approval/', views.on_approval, name='onapproval'),
    path('orders/<int:order_id>/processing/', views.order_processing, name='orderprocessing'),
    path('orders/<int:order_id>/receiving/', views.order_receiving, name='orderreceiving'),
    path('orders/<int:order_id>/closing/', views.order_closing, name='orderclosing'),
    path('orders/<int:order_id>/delete/', views.order_del, name='orderdel'),
    path('orders/<int:order_id>/edit/', views.edit_order, name='editorder'),
    path('orders/<int:order_id>/pay/', views.order_payment, name='orderpayment'),
    path('orders/<int:order_id>/return/', views.order_return, name='orderreturn'),
    path('orders/<int:order_id>/resolve/', views.order_resolve, name='orderresolve'),
    path('orders/add/', views.new_order, name='neworder'),
    path('orders/', views.orders, name='orders'),
    path('found/', views.search, name='found'),
    path('suppliers/', views.filtered_suppliers, name='suppliers'),
    path('estimates/', views.filtered_estimates, name='estimates'),
    path('phases/', views.filtered_phases, name='phases'),
    #path('houses/', views.houses, name='houses'),
    path('', views.filtered_bids, name='bids'),
    #path('create/', views.BookCreateView.as_view(), name='create_book'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()
#import djhacker
#from django import forms
#djhacker.formfield(
#        Details.goods,
#        forms.ModelChoiceField,
 #       widget=autocomplete.ModelSelect2(url='project:select_goods')
#    )