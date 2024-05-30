import os
from django import template
from django.db.models import Sum
from django.db.models import F

register = template.Library()


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def dividing(value, arg):
    return round(value / arg, 2)
@register.filter
def addition(value, arg):
    return value + arg

@register.filter
def subtraction(value, arg):
    return value - arg

@register.filter
def comma_separator(value):
    val = str(value)

@register.filter
def in_sample(details):
    return details.filter(deleted=False)

@register.filter
def summary(details):
    #sum = details.filter(deleted=False).aggregate(Sum('price'))
    summary = details.filter(deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    #ummary = OrderDetail.objects.filter(order=order_, deleted=False).annotate(total_price=F('quantity') * F('price')).aggregate(summary=Sum('total_price'))
    return summary['summary']

@register.filter
def get_display_type(type_):
    return type_

@register.filter
def get_details(details, object_):
    ret = []
    for item in details:
        if item['house__object__id'] == object_:
            ret.append(item)
    return ret
    #return details.filter(deleted=False)


@register.filter
def get_subdetails(subdetails, house):
    ret = []
    for item in subdetails:
        if item['house__id'] == house:
            ret.append(item)
    return ret


@register.filter
def amount_space_separator(amount):
    amount = '{:,}'.format(amount).replace(',', ' ')
    if amount[-2:] == '.0': amount = amount + '0'
    if len(amount)-amount.index('.')-2 > 1:
        amount = amount[:-(len(amount)-amount.index('.')-3)]
    return amount

@register.filter
def filename(value):
    return os.path.basename(value.file.name)



