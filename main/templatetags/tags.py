from django import template
import datetime

register = template.Library()


@register.simple_tag
def is_manager(request):
    is_manager_ = request.user.groups.filter(name='managers').exists()
    if is_manager_:
        return True
    return False

@register.simple_tag
def is_boss(request):
    is_boss_ = request.user.groups.filter(name='bosses').exists()
    if is_boss_:
        return True
    return False

@register.simple_tag
def is_concreter(request):
    is_concreter_ = request.user.groups.filter(name='concrete').exists()
    if is_concreter_:
        return True
    return False

@register.simple_tag
def is_supplier(request):
    is_supplier_ = request.user.groups.filter(name='suppliers').exists()
    if is_supplier_:
        return True
    return False

@register.simple_tag
def is_accountant(request):
    is_accountant_ = request.user.groups.filter(name='accountants').exists()
    if is_accountant_:
        return True
    return False

@register.simple_tag
def is_supervisor(request):
    is_supervisor_ = request.user.groups.filter(name='supervisors').exists()
    if is_supervisor_:
        return True
    return False

@register.simple_tag
def is_seller(request):
    is_seller_ = request.user.groups.filter(name='sellers').exists()
    if is_seller_:
        return True
    return False

@register.simple_tag
def is_only_seller(request):
    is_seller_ = request.user.groups.filter(name='sellers').exists()
    is_seller_boss = request.user.groups.filter(name='headsofsales').exists()
    sellergroup = request.user.groups.filter(name__contains='sellersgroup').exists()
    #only = request.user.groups.count()
    if (is_seller_ and sellergroup) or is_seller_boss:
        return True
    return False

@register.simple_tag
def is_special(request):
    is_special_ = request.user.groups.filter(name='special').exists()
    if is_special_:
        return True
    return False

@register.simple_tag
def get_display_color_type(type_):
    if type_ == 'a':
        return "list-group-item-primary"
    elif type_ == 'b':
        return "list-group-item-secondary"
    elif type_ == 'c':
        return "list-group-item-warning"
    elif type_ == 'f':
        return "list-group-item-light"
    else:
        return "list-group-item-info"

@register.simple_tag
def get_contract_color_type(perform, status):
    if status == 'a':
        return "list-group-item-danger"
    elif status == 'b' or status == 'c':
        if perform > 0:
            return "list-group-item-danger"
        else:
            return "list-group-item-success"
    else:
        return "list-group-item-light"

@register.simple_tag
def get_amount_color_type(equal):
    if equal:
        return "bg-success"
    else:
        return "bg-danger"

@register.simple_tag
def get_reservation_color(type, reservation_date):
    if type == 'b':
        return "bg-warning"
    else:
        datenow = datetime.datetime.now()
        dateminus14days = datenow - datetime.timedelta(days=14)
        if reservation_date and (reservation_date < dateminus14days):
            return "bg-danger"
        else:
            return "bg-success"

@register.simple_tag
def is_work_bid(bid):
    cnt = bid.content_set.filter(deleted=False, type='b').count()
    return cnt > 0

@register.simple_tag
def is_tech_bid(bid):
    cnt = bid.content_set.filter(deleted=False, type='c').count()
    return cnt > 0

@register.simple_tag
def is_materials_bid(bid):
    cnt = bid.content_set.filter(deleted=False, type='a').count()
    return cnt > 0

@register.simple_tag
def is_not_prepaid_bid(bid):
    cnt = bid.content_set.filter(deleted=False, type='a', prepaid=True).count()
    return cnt > 0

@register.simple_tag
def get_rollback_link(number, extended, rollback, page, object, sum_filter, unlocked_only, undelivered_only, selected_supplier):
    if number:
        return '?q=' + str(number)
    elif extended:
        return '?' + rollback
    elif selected_supplier:
        return '?' + rollback
    else:
        #return '?page=' + str(page) + '&f=' + str(object) + '&q=' + str(number) + '&s=' + str(sum_filter) + '&l=' + str(unlocked_only) + '&u=' + str(undelivered_only)
        return '?' + rollback

@register.simple_tag
def get_bid_color_type(item):
    if item.materials:
        if item.not_prepaid:
            if item.supervision:
                if item.locked:
                    result = "list-group-item list-group-item-action py-2 lh-tight"
                else:
                    result = "list-group-item list-group-item-action list-group-item-primary py-2 lh-tight"
            else:
                result = "list-group-item list-group-item-action list-group-item-success py-2 lh-tight"
        else:
            if item.locked:
                if item.supervision:
                    result = "list-group-item list-group-item-action py-2 lh-tight"
                else:
                    result = "list-group-item list-group-item-action list-group-item-success py-2 lh-tight"
            else:
                if item.supervision:
                    result = "list-group-item list-group-item-action py-2 lh-tight"
                else:
                    result = "list-group-item list-group-item-action list-group-item-danger py-2 lh-tight"
    else:
        if item.locked:
            result = "list-group-item list-group-item-action py-2 lh-tight"
        else:
            result = "list-group-item list-group-item-action list-group-item-danger py-2 lh-tight"
    return result

@register.simple_tag
def get_bid_special_color(item):
    if item.hidden:
        return "border-right: 2px solid red"
    else:
        return "border-bottom: 1px solid rgba(0,0,0,0.125)"





