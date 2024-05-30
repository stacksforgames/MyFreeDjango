from .models import Request
from .models import Details
from django.forms import Form, ModelForm, TextInput, ModelChoiceField, CharField, Textarea, ChoiceField, Select, DateField, SelectDateWidget, DateInput, NumberInput, IntegerField, BooleanField, RadioSelect, CheckboxInput, ImageField, FileInput
from django.core.exceptions import ValidationError
from django.core import validators
from dal import autocomplete
from django import forms
from .models import Goods
from .models import Bid
from .models import Object
from .models import House
from .models import Content
from .models import Phase
from .models import Supplier
from .models import Estimate
from .models import Archive
from .models import ArchiveDetail
from .models import Prepayment
from .models import Delivery
from .models import SampleDetail
from .models import Sample
from .models import Order
from .models import OrderDetail
from .models import CashRegister
from .models import SubCash
from .models import Account
from .models import Earning
from .models import Contract
from .models import Turnover
from .models import ContractImage
from bootstrap_modal_forms.forms import BSModalModelForm
from bootstrap_modal_forms.forms import BSModalForm
from django.contrib.admin.widgets import AdminDateWidget
from dal import forward
from datetime import datetime
from django.contrib.auth.models import User


class RequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ["title"]
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите примечание к заявке'
            }),
        }


class DetailsForm(ModelForm):
    goods = ModelChoiceField(queryset=Goods.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_goods'), label="Выбрать")

    quantity = forms.DecimalField(label='Количество', max_digits=10, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'style': 'width: 100px'}))

    def clean_quantity(self):
        val = self.cleaned_data['quantity']
        if val <= 0:
            raise ValidationError('Укажите корректное количество!')
        return val

    class Meta:
        model = Details
        # fields = ('__all__')
        fields = ("goods", "quantity")


class BidForm(ModelForm):
    #number = IntegerField(label='Номер заявки', widget=NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}))
    number = CharField(label='Номер заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    title = CharField(label='Описание заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='')
    object = ModelChoiceField(queryset=Object.objects.filter(special=True), label='Объект',
                              widget=Select(attrs={'class': 'form-select'}))

    def clean_number(self):
        val = self.cleaned_data['number']
#        if val <= 0:
#            raise ValidationError('Некорректный номер заявки')
#        if val >= 1000000:
#            raise ValidationError('Некорректный номер заявки')
        if val == '' or val is None:
            raise ValidationError('Некорректный номер заявки')
        return val

    class Meta:
        model = Bid
        fields = ["number", "title", "object"]


class ArchEditForm(ModelForm):
    #number = IntegerField(label='Номер заявки', widget=NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}))
    number = CharField(label='Номер заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    title = CharField(label='Описание заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='')

    def clean_number(self):
        val = self.cleaned_data['number']
        if val == '' or val is None:
            raise ValidationError('Некорректный номер заявки')
        return val

    class Meta:
        model = Archive
        fields = ["number", "title"]


class BidEditForm(ModelForm):
    #number = IntegerField(label='Номер заявки', widget=NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}))
    number = CharField(label='Номер заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    title = CharField(label='Описание заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='')

    def clean_number(self):
        val = self.cleaned_data['number']
#        if val <= 0:
#            raise ValidationError('Некорректный номер заявки')
#        if val >= 1000000:
#            raise ValidationError('Некорректный номер заявки')
        if val == '' or val is None:
            raise ValidationError('Некорректный номер заявки')
        return val

    class Meta:
        model = Bid
        fields = ["number", "title", "id"]


class ContentsForm(ModelForm):
    title = CharField(label='Описание (материала/работ/вида техники)', widget=Textarea(attrs={'class': 'form-control','rows': 2}), initial='')
    house = ModelChoiceField(label='№ дома', queryset=House.objects.all(), widget=Select(attrs={'class': 'form-select'}))
                               #  widget=Select()   autocomplete.ModelSelect2(url='project:select_house'), label="Выбрать")
    #date = DateField(label="Дата работ/поставки:", widget=SelectDateWidget(attrs={'class': 'form-control datetimepicker-input'}))
    date = DateField(label="Дата работ/поставки:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)
    type = ChoiceField(label='Вид расходов', choices=Content.SUPPLY, widget=Select(attrs={'class': 'form-select'}))
    cash = ChoiceField(label='Нал/безнал', choices=Content.CASHLESS, widget=Select(attrs={'class': 'form-select'}))
    quantity = forms.DecimalField(label='Количество', max_digits=12, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0)
    measure = ChoiceField(label='Ед. измерения', choices=Content.MEASURES, widget=Select(attrs={'class': 'form-select'}))
    price = forms.DecimalField(label='Стоимость за ед.', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    #supplier = ModelChoiceField(queryset=Supplier.objects.all(), label='Поставщик')
    supplier = ModelChoiceField(queryset=Supplier.objects.filter(hidden=False), #Supplier.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_supplier',
                                                                 attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
                                                                 label="Поставщик")
    phase = ModelChoiceField(queryset=Phase.objects.filter(hidden=False).order_by('name'), label='Этап строительства', widget=Select(attrs={'class': 'form-select'}))
    estimate = ModelChoiceField(queryset=Estimate.objects.filter(hidden=False).order_by('name'), label='Смета', widget=Select(attrs={'class': 'form-select'}))
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='')

    prepaid = BooleanField(label='Оплата после доставки', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    def __init__(self, *args, **kwargs):
        objectid = kwargs.pop('objectid', None)
        super(ContentsForm, self).__init__(*args, **kwargs)
        if objectid:
            self.fields['house'].queryset = House.objects.filter(object=objectid)
        # self.fields['house'].label = 'Дом №'
        #for visible in self.visible_fields():
        #    visible.field.widget.attrs['class'] = 'form-control'
        # self.fields['date'].required = ''

    def clean_quantity(self):
        type_ = self.cleaned_data['type']
        val = self.cleaned_data['quantity']
        if val <= 0 and type_ != 'd':
            raise ValidationError('Укажите корректное количество! В случае доставки укажите 0')
#        if val > 0 and type_ == 'b' and measure_ == 'hu' and (int(val) - val != 0):
#            raise ValidationError('Укажите корректное количество! Количество человек может быть только целым числом')
        return val

    def clean_date(self):
        val = self.cleaned_data['date']
        if not val:
            raise ValidationError('Дата указана неверно')
        return val

    def clean_measure(self):
        type_ = self.cleaned_data['type']
        try:
            quantity = self.cleaned_data['quantity']
        except:
            quantity = 0
        measure = self.cleaned_data['measure']
        if type_ == 'b' and measure != 'hh' and measure != 'm2' and measure != 'hu' and measure != 'm3' and measure != 'on' and measure != 'm1' and measure != 'pm':
            raise ValidationError('Работа измеряется в часах, единицах, количестве рабочих или в метрах!')
        if type_ == 'c' and measure != 'hh' and measure != 'm1' and measure != 'on':
            raise ValidationError('Работа техники измеряется в часах, единицах или метрах!')
        if type_ == 'd' and measure != '--':
            raise ValidationError('Для описания доставки надо в ед. измерения выбрать пункт "доставка"')
        if quantity > 0 and type_ == 'b' and measure == 'hu' and (int(quantity) - quantity != 0):
            raise ValidationError('Укажите корректное количество! Количество человек может быть только целым числом')
        return measure

    def clean_price(self):
        val = self.cleaned_data['price']
        type_ = self.cleaned_data['type']
        if val != 0 and type_ == 'e':
            raise ValidationError('При перемещении стоимость надо установить равной 0')
        if val <= 0 and type_ != 'e':
            raise ValidationError('Укажите корректное стоимость материалов/услуг!')
        return val

    class Meta:
        model = Content
        # fields = ('__all__')
        fields = ("house", "title", "date", "type", "cash", "quantity", "measure", "price", "supplier", "phase", "estimate", "comment", "prepaid")


class ContractForm(ModelForm):
    type = ChoiceField(label='Тип договора', choices=Contract.TYPES, widget=Select(attrs={'class': 'form-select'}))
    number = CharField(label='Номер договора', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    title = CharField(label='Описание (не обязательно):', widget=Textarea(attrs={'class': 'form-control','rows': 3, 'placeholder': 'необязательное поле'}), initial='', required=False)
    date = DateField(label="Дата контракта:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True, localize=False)

    object = ModelChoiceField(queryset=Object.objects.filter(special=True), label='Объект',
                              widget=Select(attrs={'class': 'form-select'}), required=True)

    client = CharField(label='Клиент', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    clientphone = CharField(label='Номер телефона клиента', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    agency = CharField(label='Агентство', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    agencyphone = CharField(label='Номер телефона АН', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    apartment = CharField(label='Помещение', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    square = forms.DecimalField(label='Площадь', max_digits=20, decimal_places=2,
                               widget=forms.widgets.NumberInput(
                                   attrs={'class': 'form-control', 'style': 'width: 100%'}))
    price = forms.DecimalField(label='Цена по шахматке', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    agency_discount = forms.DecimalField(label='Скидка АН', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    developer_discount = forms.DecimalField(label='Скидка застройщика', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    seller_commission_calc = CharField(label='Расчет комиссии ОП (формула)', widget=Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'например: 2 000 000 - 140 000 (ком АН) = 1 860 000 *5%',}), initial='')
    seller_commission = forms.DecimalField(label='Комиссия ОП (сумма)', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    agency_commission_calc = CharField(label='Расчет комиссии АН (формула)', widget=Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'например: 20 000/м2 *  17 м.'}), initial='')
    agency_commission = forms.DecimalField(label='Комиссия АН (сумма)', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    installment = CharField(label='Срок рассрочки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = Contract
        fields = ["type", "number", "title", "date", "object", "house", "client", "clientphone", "agency", "agencyphone", "apartment", "square", "price",
                  "agency_discount", "developer_discount", "seller_commission_calc", "seller_commission",
                  "agency_commission_calc", "agency_commission", "installment"]
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }

    def __init__(self, *args, **kwargs):
        super(ContractForm, self).__init__(*args, **kwargs)
        self.fields['house'].required = False


class ContractChangeForm(ModelForm):
    type = ChoiceField(label='Новый тип договора', choices=Contract.TYPES, widget=Select(attrs={'class': 'form-select'}))
    number = CharField(label='Новый номер договора', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = Contract
        fields = ["type", "number"]


class ContractReceiptForm(ModelForm):
    receipt = BooleanField(label='Чек отбит', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    onhand = BooleanField(label='Оригинал в наличии', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Contract
        fields = ["receipt", "onhand"]


class ContractCommentForm(ModelForm):
    comment = CharField(label='Причина аннулирования контракта', widget=Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'поле обязательно для заполнения'}), initial='')

    class Meta:
        model = Contract
        fields = ["comment"]


class ContractEditForm(ModelForm):
    title = CharField(label='Описание (не обзязательно):', widget=Textarea(attrs={'class': 'form-control','rows': 3, 'placeholder': 'необязательное поле'}), initial='', required=False)
    date = DateField(label="Дата контракта:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True, localize=False)

    object = ModelChoiceField(queryset=Object.objects.filter(special=True), label='Объект',
                              widget=Select(attrs={'class': 'form-select'}), required=True)

    client = CharField(label='Клиент', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    agency = CharField(label='Агентство', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    apartment = CharField(label='Помещение', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    square = forms.DecimalField(label='Площадь', max_digits=20, decimal_places=2,
                               widget=forms.widgets.NumberInput(
                                   attrs={'class': 'form-control', 'style': 'width: 100%'}))
    price = forms.DecimalField(label='Цена по шахматке', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    agency_discount = forms.DecimalField(label='Скидка АН', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    developer_discount = forms.DecimalField(label='Скидка застройщика', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    seller_commission_calc = CharField(label='Расчет комиссии ОП (формула)', widget=Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'например: 2 000 000 - 140 000 (ком АН) = 1 860 000 *5%',}), initial='')
    seller_commission = forms.DecimalField(label='Комиссия ОП (сумма)', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))
    agency_commission_calc = CharField(label='Расчет комиссии АН (формула)', widget=Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'например: 20 000/м2 *  17 м.'}), initial='')
    agency_commission = forms.DecimalField(label='Комиссия АН (сумма)', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    installment = CharField(label='Срок рассрочки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = Contract
        fields = ["title", "date", "object", "house", "client", "agency", "apartment", "square", "price",
                  "agency_discount", "developer_discount", "seller_commission_calc", "seller_commission",
                  "agency_commission_calc", "agency_commission", "installment"]
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }

    def __init__(self, *args, **kwargs):
        super(ContractEditForm, self).__init__(*args, **kwargs)
        self.fields['house'].required = False


class TurnoverForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 4}), initial='', required=True)
    date = DateField(label="Дата", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    amount = forms.DecimalField(label='Сумма', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    type = ChoiceField(label='Нал/безнал', choices=Turnover.TYPES, widget=Select(attrs={'class': 'form-select'}))

    class Meta:
        model = Turnover
        fields = ["comment", "date", "amount", "type"]


class TurnoverPerformedForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 4}), initial='', required=True)
    date = DateField(label="Дата", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    actualdate = DateField(label="Реальная дата операции", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=False, localize=False)
    amount = forms.DecimalField(label='Сумма', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    type = ChoiceField(label='Нал/безнал', choices=Turnover.TYPES, widget=Select(attrs={'class': 'form-select'}))

    performed = BooleanField(label='Проведено', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Turnover
        fields = ["comment", "date", "actualdate", "amount", "type", "performed"]


class TurnoverCommentOnlyForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 4}), initial='', required=True)

    class Meta:
        model = Turnover
        fields = ["comment"]


class ArchiveDetailForm(ModelForm):
    title = CharField(label='Описание (материала/работ/вида техники)', widget=Textarea(attrs={'class': 'form-control','rows': 2}), initial='')
    house = ModelChoiceField(label='№ дома', queryset=House.objects.all(), widget=Select(attrs={'class': 'form-select'}))

    date = DateField(label="Дата работ/поставки:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)
    #type = ChoiceField(label='Вид расходов', choices=Content.SUPPLY, widget=Select(attrs={'class': 'form-select'}))
    cash = ChoiceField(label='Нал/безнал', choices=Content.CASHLESS, widget=Select(attrs={'class': 'form-select'}))
    summary = forms.DecimalField(label='Сумма', max_digits=20, decimal_places=2,
                               widget=forms.widgets.NumberInput(
                                   attrs={'class': 'form-control', 'style': 'width: 100%'}))
    #supplier = CharField(label='Поставщик',
    #                  widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    new_supplier = ModelChoiceField(queryset=Supplier.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_supplier_view',
                                                                 attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
                                                                 label="Поставщик", required=True)
    spending = CharField(label='Расходы по смете',
                         widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    materials = CharField(label='Использованные материалы',
                         widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)

    quantity = forms.DecimalField(label='Количество (не обязательно)', max_digits=12, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=False)
    cost = forms.DecimalField(label='Стоимость за ед. (не обязательно)', max_digits=20, decimal_places=2,
                               widget=forms.widgets.NumberInput(
                                   attrs={'class': 'form-control', 'style': 'width: 100%'}), required=False)
    measure = CharField(label='Единица измерения (не обязательно)',
                         widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    foreman = CharField(label='Прораб (не обязательно)',
                        widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    phase = ModelChoiceField(queryset=Phase.objects.all(), label='Этап строительства', widget=Select(attrs={'class': 'form-select'}))
    estimate = ModelChoiceField(queryset=Estimate.objects.all(), label='Смета', widget=Select(attrs={'class': 'form-select'}))

    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='')

    def __init__(self, *args, **kwargs):
        objectid = kwargs.pop('objectid', None)
        super(ArchiveDetailForm, self).__init__(*args, **kwargs)
        if objectid:
            self.fields['house'].queryset = House.objects.filter(object=objectid)

    def clean_date(self):
        val = self.cleaned_data['date']
        if not val:
            raise ValidationError('Дата указана неверно')
        return val

    def clean_summary(self):
        val = self.cleaned_data['summary']
        if val <= 0:
            raise ValidationError('Укажите корректное стоимость материалов/услуг!')
        return val

    class Meta:
        model = ArchiveDetail
        # fields = ('__all__')
        fields = ("house", "title", "date", "cash", "summary", "quantity", "measure", "cost", "materials", "spending", "supplier", "foreman", "phase", "estimate", "comment")


class ReportForm(Form):
    datefrom = DateField(label="Дата с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Дата по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    estimate = ModelChoiceField(queryset=Estimate.objects.filter(deleted=False).order_by('name'), label='По смете',  widget=Select(attrs={'class': 'form-select'}), required=False)

    phase = ModelChoiceField(queryset=Phase.objects.filter(deleted=False).order_by('name'), label='По этапу строительства',  widget=Select(attrs={'class': 'form-select'}), required=False)

    Supply = (('0', '---------'),) + Content.SUPPLY
    type_ = ChoiceField(label='Вид расходов', choices=Supply, widget=Select(attrs={'class': 'form-select'}), required=False)

    #YES_NO = ((True, 'Yes'), (False, 'No'))

    concrete_only = BooleanField(label='Только бетон', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    barter_only = BooleanField(label='Отдельно бартер', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    closed_only = BooleanField(label='Только закрытые', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    Exclusions = (('0', '---------'), ('1', 'Расходы на продажу'))
    exclusion = ChoiceField(label='Не включать в отчёт', choices=Exclusions, widget=Select(attrs={'class': 'form-select'}), required=True)

    #class Meta:
        # fields = ('__all__')
        #fields = ("goods", "quantity")
        #fields = ['datefrom', 'concrete_only']
        #widgets = {
        #    'concrete_only': forms.CheckboxInput(
        #        attrs={"class": "form-check-input", "id": "flexSwitchCheckChecked"}),
        #    'datefrom' : DateInput(attrs={'class': 'form-control', 'type': 'date'})
        #}


class SuppliersForm(Form):
    filter_str = CharField(label='Поставщик', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)

#    def clean_number(self):
#        val = self.cleaned_data['filter_str'].strip()
#        if len(val) <= 2:
#            raise ValidationError('введите не менее трёх цифровых символов!')
#        return val


class EstimatesForm(Form):
    filter_str = CharField(label='Смета', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)


class SupplierReportForm(Form):
    datefrom = DateField(label="Дата с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Дата по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    #filter_supplier = ModelChoiceField(queryset=Supplier.objects.all(), label='Поставщик', widget=Select(attrs={'class': 'form-select'}), required=False)

    filter_supplier = ModelChoiceField(queryset=Supplier.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_supplier_view',
                                                                 attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
                                                                 label="Поставщик", required=False)


class PhasesForm(Form):
    filter_str = CharField(label='Этап строительства', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)


class ConcreteForm(ModelForm):
    datefrom = DateField(label="Фильтр по дате с", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)
    dateto = DateField(label="Фильтр по дате по", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)
    filter_supplier = ModelChoiceField(queryset=Supplier.objects.filter(type='1'), label='Фильтр по поставщику', widget=Select(attrs={'class': 'form-select'}), required=False)

    object = ModelChoiceField(queryset=Object.objects.all(), label='Объект',
                               widget=Select(attrs={'class': 'form-select'}), required=False)

    prepay_only = BooleanField(label='Только авансы', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Delivery
        fields = {"object", "house"}
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }
    def __init__(self, *args, **kwargs):
        super(ConcreteForm, self).__init__(*args, **kwargs)
        self.fields['house'].required = False

class TestForm(Form):
    datefrom = DateField(label="Дата с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Дата по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

class ExportForm(ModelForm):
    datefrom = DateField(label="Выгрузить с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Выгрузить по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    CHOICES = [('option1', 'По дате создания заявки'),
               ('option2', 'По дате поставки/выполнения')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    object = ModelChoiceField(queryset=Object.objects.all(), label='Объект',
                               widget=Select(attrs={'class': 'form-select'}), required=False)

    concrete_included = BooleanField(label='Включая бетон', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Content
        fields = {"object", "house"}
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }
    def __init__(self, *args, **kwargs):
        super(ExportForm, self).__init__(*args, **kwargs)
        self.fields['house'].required = False


class ContractsExportForm(Form):
    datefrom = DateField(label="Выгрузить с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Выгрузить по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)


class ImageUploadForm(ModelForm):
    date = DateField(label="Дата чека:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=True, localize=False)
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)
    image = ImageField(label='Изображение', widget=FileInput(attrs={'class': 'form-control'}), required=True)
    class Meta:
        model = ContractImage
        fields = ['date', 'comment', 'image']

class BalanceForm(Form):
    datefrom = DateField(label="С даты:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="По дату:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    CHOICES = [('0', 'Всё'),
               ('1', 'Приход'),
               ('2', 'Расход'),
               ('3', 'Нераспределённое'),
               ('4', 'Приход+расход'),]

    choice_filter = ChoiceField(label='Выбрать', choices=CHOICES, widget=Select(attrs={'class': 'form-select'}))

    cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status=0), label='Касса', widget=Select(attrs={'class': 'form-select'}), required=True)


class SubCashesForm(Form):
    cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status__in=[0]), label='Касса', widget=Select(attrs={'class': 'form-select'}), required=True)


class AccountsForm(Form):
    cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status__in=[0,1]), label='Касса', widget=Select(attrs={'class': 'form-select'}), required=True)


class SubCashForm(ModelForm):
    name = CharField(label='Название кассы:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status=0), label='Касса',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    balance = forms.DecimalField(label='Входящий остаток:', max_digits=20, decimal_places=2,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    date = DateField(label="На дату:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    closedate = DateField(label="Дата закрытия (если закрыта):", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=False, localize=False)

    class Meta:
        model = SubCash
        fields = ["name", "cashregister", "balance", "date", "closedate"]

    def __init__(self, *args, **kwargs):
        cashregisterid = kwargs.pop('cashregisterid', None)
        super(SubCashForm, self).__init__(*args, **kwargs)
        if cashregisterid:
            self.fields['cashregister'].queryset = CashRegister.objects.filter(id=cashregisterid)


class AccountForm(ModelForm):
    name = CharField(label='Название счета:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status=0), label='Принадлежность',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    balance = forms.DecimalField(label='Входящий остаток:', max_digits=20, decimal_places=2,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    date = DateField(label="На дату:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    closedate = DateField(label="Дата закрытия (если закрыт):", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=False, localize=False)

    class Meta:
        model = Account
        fields = ["name", "cashregister", "balance", "date", "closedate"]

    def __init__(self, *args, **kwargs):
        cashregisterid = kwargs.pop('cashregisterid', None)
        super(AccountForm, self).__init__(*args, **kwargs)
        if cashregisterid:
            self.fields['cashregister'].queryset = CashRegister.objects.filter(id=cashregisterid)


class SubCashFormEdit(ModelForm):
    name = CharField(label='Название кассы:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    #cashregister = ModelChoiceField(queryset=CashRegister.objects.filter(deleted=False, status=0), label='Касса',
    #                                widget=Select(attrs={'class': 'form-select'}), required=True)
    balance = forms.DecimalField(label='Входящий остаток:', max_digits=20, decimal_places=2,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    date = DateField(label="На дату:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    closedate = DateField(label="Дата закрытия (если закрыта):", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=False, localize=False)

    class Meta:
        model = SubCash
        fields = ["name", "balance", "date", "closedate"]


class AccountFormEdit(ModelForm):
    name = CharField(label='Название счета:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    balance = forms.DecimalField(label='Входящий остаток:', max_digits=20, decimal_places=2,
                                 widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    date = DateField(label="На дату:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    closedate = DateField(label="Дата закрытия (если закрыт):", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=False, localize=False)

    class Meta:
        model = Account
        fields = ["name", "balance", "date", "closedate"]


class ExpenseContentFormEdit(ModelForm):
    subcash = ModelChoiceField(queryset=SubCash.objects.all(), label='Касса',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    expense_account = ModelChoiceField(queryset=Account.objects.all(), label='Выдано со счёта',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    credit_account = ModelChoiceField(queryset=Account.objects.all(), label='Счет получателя',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)

    class Meta:
        model = Content
        fields = ["subcash", "expense_account", "credit_account"]

    def __init__(self, *args, **kwargs):
        cashregisterid = kwargs.pop('cashregisterid', None)
        contentdate = kwargs.pop('contentdate', None)
        super(ExpenseContentFormEdit, self).__init__(*args, **kwargs)
        if cashregisterid and contentdate:
            print(cashregisterid,'<===>',contentdate)
            self.fields['subcash'].queryset = SubCash.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister=cashregisterid)
            self.fields['expense_account'].queryset = Account.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister=cashregisterid)
            self.fields['credit_account'].queryset = Account.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister__status=2)


class SubcashChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.closedate:
            return f'{obj.name} (закрыта с {datetime.strftime(obj.closedate, "%d-%m-%Y")})'
        else:
            return f'{obj.name}'


class AccountChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.closedate:
            return f'{obj.name} (закрыт с {datetime.strftime(obj.closedate, "%d-%m-%Y")})'
        else:
            return f'{obj.name}'


class EarningForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    date = DateField(label="Дата", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)
    summary = forms.DecimalField(label='Сумма', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)

    supplier = ModelChoiceField(queryset=Supplier.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_supplier_view',
                                                                 attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
                                                                 label="Контрагент (необязательно)", required=False)

    object = ModelChoiceField(queryset=Object.objects.all(), label='Объект',
                              widget=Select(attrs={'class': 'form-select'}), required=True)

    subcash = SubcashChoiceField(queryset=SubCash.objects.all(), label='Касса',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    expense_account = AccountChoiceField(queryset=Account.objects.all(), label='Получено со счёта',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)
    credit_account = AccountChoiceField(queryset=Account.objects.all(), label='Счет кассы',
                                    widget=Select(attrs={'class': 'form-select'}), required=True)

    class Meta:
        model = Earning
        fields = ["comment", "date", "summary", "supplier", "object", "subcash", "expense_account", "credit_account"]

    def __init__(self, *args, **kwargs):
        cashregisterid = kwargs.pop('cashregisterid', None)
        contentdate = kwargs.pop('contentdate', None)
        super(EarningForm, self).__init__(*args, **kwargs)
        if cashregisterid and contentdate:
            self.fields['subcash'].queryset = SubCash.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister=cashregisterid)
            self.fields['expense_account'].queryset = Account.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister__status=2)
            self.fields['credit_account'].queryset = Account.objects.exclude(closedate__lt=contentdate).filter(deleted=False, cashregister=cashregisterid)


class AuthorChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'

class BidsForm(Form):
    filter_object = ModelChoiceField(queryset=Object.objects.filter(special=True), label='Фильтр по объекту', widget=Select(attrs={'class': 'form-select'}), required=False)

    summary = forms.DecimalField(label='Фильтр по сумме заявки', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}), required=False)

    #unlocked_only = BooleanField(label='Только разблокированные', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    #undelivered_only = BooleanField(label='Только недоставленные', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    datefrom = DateField(label="Выбрать с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Выбрать по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    author = AuthorChoiceField(queryset=User.objects.all(), label='Фильтр по инициатору', widget=Select(attrs={'class': 'form-select'}), required=False)

    CHOICES = [('0', 'Все'),
               ('1', 'Оплаченные и доставленные'),
               ('2', 'Доставленные но неоплаченные'),
               ('3', 'Оплаченные и недоставленные'),
               ('4', 'Все недоставленные материалы'),
               ('5', 'Доставленные и оплаченные'),
               ('6', 'Все неоплаченные заявки'),
               ('7', 'Возвраты')]

    choice_filter = ChoiceField(label='Выбрать', choices=CHOICES, widget=Select(attrs={'class': 'form-select'}))


class ContractsForm(ModelForm):
    object = ModelChoiceField(queryset=Object.objects.filter(special=True), label='Фильтр по объекту', widget=Select(attrs={'class': 'form-select'}), required=False)

    datefrom = DateField(label="Выбрать с:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    dateto = DateField(label="Выбрать по:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}), required=False, localize=False)

    author = AuthorChoiceField(queryset=User.objects.all(), label='Фильтр по инициатору', widget=Select(attrs={'class': 'form-select'}), required=False)

    CHOICES = [('0', 'Все'),
               ('a', 'Создан'),
               ('b', 'Проверен бухгалтером'),
               ('c', 'На исполнении'),
               ('d', 'Исполнен'),
               ('e', 'Просрочка'),
               ('f', 'Виртуальная бронь'),
               ('g', 'Бронь более 14 дней'),
               ('h', 'Аннулированные')]

    OPTIONS = [('0', '---------'),
               ('a', 'Есть'),
               ('b', 'Нет')]

    choice_filter = ChoiceField(label='Фильтр по статусу', choices=CHOICES, widget=Select(attrs={'class': 'form-select'}))

    contract_types = (('0', '---------'),) + Contract.TYPES
    contract_type = ChoiceField(label='Тип договора', choices=contract_types, widget=Select(attrs={'class': 'form-select'}))

    receipt = ChoiceField(label='Чек отбит', choices=OPTIONS, widget=Select(attrs={'class': 'form-select'}))

    onhand = ChoiceField(label='Оригинал в наличии', choices=OPTIONS, widget=Select(attrs={'class': 'form-select'}))

    number = CharField(label='Номер договора', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)

    client = CharField(label='Клиент', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)

    class Meta:
        model = Contract
        fields = {"object", "house"}
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }
    def __init__(self, *args, **kwargs):
        super(ContractsForm, self).__init__(*args, **kwargs)
        self.fields['house'].required = False


class BookModelForm(BSModalModelForm):
    class Meta:
        model = House
        fields = ['name']


class HouseDetailModelForm(BSModalForm):
    class Meta:
        model = House
        fields = ['name']

class SearchForm(Form):
    number = CharField(label='Номер заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    def clean_number(self):
        #val = self.cleaned_data['number'].strip()
        val = ''.join(c for c in self.cleaned_data['number'] if c in '0123456789/-')
        if len(val) <= 2:
            raise ValidationError('введите не менее трёх цифровых символов!')
        return val

class BidsSearchForm(BSModalForm):
    number = CharField(label='Номер заявки', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    #def clean_number(self):
    #    val = ''.join(c for c in self.cleaned_data['number'] if c in '0123456789/-')
    #    if len(val) <= 2:
    #        raise ValidationError('введите не менее трёх символов!')
    #    return val
    class Meta:
        fields = ['number']


class PrepaymentForm(ModelForm):
    comment = CharField(label='Комментарий (не обязательно)', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    summary = forms.DecimalField(label='Сумма аванса', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    supplier = ModelChoiceField(queryset=Supplier.objects.filter(type='1'), label='Поставщик',
                             widget=Select(attrs={'class': 'form-select'}), required=True)
    #supplier = ModelChoiceField(queryset=Supplier.objects.all(),
    #                            widget=autocomplete.ModelSelect2(url='project:select_supplier',
    #                                                             attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
    #                                                             label="Поставщик")
    date = DateField(label="Дата:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)

    class Meta:
        model = Prepayment
        fields = ["comment", "summary", "supplier", "date"]


class ConcreteDeliveryForm(ModelForm):
    comment = CharField(label='Комментарий (не обязательно)', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    volume = forms.DecimalField(label='Объём:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    price = forms.DecimalField(label='Цена за м3:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    pumpsummary = forms.DecimalField(label='Сумма (бетононасос):', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    pumptransfer = forms.DecimalField(label='Переезд автобетононасоса (сумма):', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)
    downtime = forms.DecimalField(label='Количество часов простоя:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)
    downtimecost = forms.DecimalField(label='Стоимость часа простоя:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)
    pumpcomment = CharField(label='Комментарий по бетононасосу (не обязательно)', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)

    deliveryvolume = forms.DecimalField(label='Объём доставки:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)
    deliveryprice = forms.DecimalField(label='Цена доставки за м3:', max_digits=20, decimal_places=2,
                              widget=forms.widgets.NumberInput(
                                  attrs={'class': 'form-control', 'style': 'width: 100%'}), required=True)

    supplier = ModelChoiceField(queryset=Supplier.objects.filter(type='1'), label='Поставщик',
                              widget=Select(attrs={'class': 'form-select'}), required=True)
    #supplier = ModelChoiceField(queryset=Supplier.objects.all(),
    #                            widget=autocomplete.ModelSelect2(url='project:select_supplier',
    #                                                             attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
    #                                                             label="Поставщик")
    date = DateField(label="Дата:", widget=DateInput(attrs={'class': 'form-control', 'type': 'date'}),
                       required=True, localize=False)

    object = ModelChoiceField(queryset=Object.objects.all(), label='Объект',
                               widget=Select(attrs={'class': 'form-select'}), required=True)

    pile = CharField(label='Информация по сваям (не обязательно)',
                        widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=False)
    concrete_grade = ChoiceField(label='Марка бетона', choices=Delivery.GRADE, widget=Select(attrs={'class': 'form-select'}))

    verified = BooleanField(label='Сверено', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Delivery
        #fields = ('__all__')
        fields = ["comment", "volume", "price", "pumpsummary", "pumptransfer", "downtime", "downtimecost", "pumpcomment", "deliveryvolume", "deliveryprice", "supplier", "date", "house", "object", "pile", "concrete_grade", "verified"]
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }


class TForm(forms.ModelForm):
    object_ = ModelChoiceField(queryset=Object.objects.all(), label='Объект', widget=Select(attrs={'class': 'form-select'}), required=True)

    #house = ModelChoiceField(label='№ дома', queryset=House.objects.all(), widget=Select(attrs={'class': 'form-select'}), required=True)
    class Meta:
        model = House
        fields = ('__all__')
        widgets = {
            'object': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('object_',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
        }

    class Media:
        js = (
            'linked_data.js',
        )


class HouseForm(ModelForm):
    name = CharField(label='Номер дома:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = House
        fields = ["name"]


class HouseModelForm(BSModalModelForm):
    name = CharField(label='Название (номер) дома:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = House
        fields = ['name']


class SupplierModelForm(BSModalModelForm):
    name = CharField(label='Название поставщика:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    hidden = BooleanField(label='Поставщик скрыт', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Supplier
        fields = ['name', 'hidden']

class SupplierChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return f'[{obj.id}] {obj.name}'

class SupplierRemoveModelForm(BSModalModelForm):
    #name = CharField(label='Название поставщика:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}))
    #hidden = BooleanField(label='Поставщик скрыт', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    newsupplier = SupplierChoiceField(queryset=Supplier.objects.filter(hidden=False), label='Поставщик',
                               widget=Select(attrs={'class': 'form-select'}), required=True)
    #newsupplier = ModelChoiceField(queryset=Supplier.objects.filter(hidden=False),
    #                                widget=autocomplete.ModelSelect2(url='project:select_supplier',
    #                                                             attrs={'dropdownParent': '.modal-content'}),
    #                                                           label="Поставщик")
    class Meta:
        model = Supplier
        fields = ['newsupplier']



class EstimateModelForm(BSModalModelForm):
    name = CharField(label='Название сметы:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    hidden = BooleanField(label='Смета скрыта', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Estimate
        fields = ['name', 'hidden']


class PhaseModelForm(BSModalModelForm):
    name = CharField(label='Название этапа:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')
    hidden = BooleanField(label='Этап скрыт', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Phase
        fields = ['name', 'hidden']

class ObjectModelForm(BSModalModelForm):
    name = CharField(label='Название объекта:', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='')

    class Meta:
        model = Object
        fields = ['name']


class SampleDetailForm(ModelForm):
    code = CharField(label='Код/артикул (не обязательно)', widget=Textarea(attrs={'class': 'form-control','rows': 1}), initial='', required=False)
    description = CharField(label='Товары (работы, услуги)', widget=Textarea(attrs={'class': 'form-control','rows': 2}), initial='', required=True)

    quantity = forms.DecimalField(label='Количество', max_digits=12, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)
    measure = ChoiceField(label='Ед. измерения', choices=SampleDetail.MEASURES, widget=Select(attrs={'class': 'form-select'}))
    price = forms.DecimalField(label='Цена за ед.', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    def clean_quantity(self):
        val = self.cleaned_data['quantity']
        if val < 0:
            raise ValidationError('Укажите корректное количество материалов/услуг!')
        return val

    class Meta:
        model = SampleDetail
        fields = ("code", "description", "quantity", "measure", "price")


class SampleForm(ModelForm):
    title = CharField(label='Описание шаблона', widget=Textarea(attrs={'class': 'form-control', 'rows': 1}), initial='', required=True)
    hidden = BooleanField(label='Скрытый шаблон', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)

    class Meta:
        model = Sample
        fields = ("title", "hidden")


class OrderForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    sample = ModelChoiceField(queryset=Sample.objects.filter(hidden=False), label='Шаблон заказа',
                               widget=Select(attrs={'class': 'form-select'}), required=True)

    object = ModelChoiceField(queryset=Object.objects.all(), label='Объект',
                               widget=Select(attrs={'class': 'form-select'}), required=True)
    agreement = BooleanField(label='Отправить на согласование', widget=CheckboxInput(attrs={'class': 'form-check-input'}),
                          required=False)

    class Meta:
        model = Order
        fields = ["comment", "sample", "house", "object"]
        widgets = {
            'house': autocomplete.ModelSelect2(url='project:linked_data',
                                              forward=('src_object', 'object',), attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true; height:38px'}),
        }
        labels = {
            'house': "Дом:",
        }


class OnApprovalForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    class Meta:
        model = Order
        fields = ["comment"]


class ResolveForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    #resolve = BooleanField(label='Решение', widget=CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
    CHOICES = [('option1', '⇐ На доработку'),
               ('option2', 'Без изменений'),
               ('option3', '⇒ Снабженцу')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ["comment"]


class ProcessingForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    supplier = ModelChoiceField(queryset=Supplier.objects.all(),
                                widget=autocomplete.ModelSelect2(url='project:select_supplier',
                                                                 attrs={'style': 'min-width: auto; width: 100%; dropdownAutoWidth: true'}),
                                                                 label="Поставщик", required=False)

    CHOICES = [('option1', '⇐ На доработку'),
               ('option2', 'Без изменений'),
               ('option3', '⇒ Бухгалтеру')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ["comment", "supplier"]


class ClosingForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    CHOICES = [('option1', '⇐ На доработку'),
               ('option2', 'Без изменений'),
               ('option3', '⇒ Закрыть заказ')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    phase = ModelChoiceField(queryset=Phase.objects.all(), label='Этап строительства', widget=Select(attrs={'class': 'form-select'}), required=False)
    estimate = ModelChoiceField(queryset=Estimate.objects.all(), label='Смета', widget=Select(attrs={'class': 'form-select'}), required=False)

    class Meta:
        model = Order
        fields = ["comment"]


class ReceivingForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    CHOICES = [('option1', '⇐ Всё доставлено'),
               ('option2', 'Без изменений'),
               ('option3', '⇒ Есть замечания')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ["comment"]


class CompletionForm(ModelForm):
    comment = CharField(label='Комментарий', widget=Textarea(attrs={'class': 'form-control', 'rows': 2}), initial='', required=True)

    CHOICES = [('option1', '⇐ Всё доставлено'),
               ('option2', 'Без изменений'),
               ('option3', '⇒ Есть замечания')]

    like = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

    class Meta:
        model = Order
        fields = ["comment"]


class OrderDetailModelForm(BSModalModelForm):
    quantity = forms.DecimalField(label='Количество', max_digits=12, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)

    class Meta:
        model = OrderDetail
        fields = ['quantity']

class ChoiceFieldNoValidation(ChoiceField):
   def validate(self, value):
       pass


class OrdersForm(Form):
    status = ChoiceFieldNoValidation(label='Фильтр по статусу заказа', choices=Order.STATUSES, widget=Select(attrs={'class': 'form-select'}), required=False)



class OrderDetailForm(ModelForm):
    code = CharField(label='Код/артикул (не обязательно)', widget=Textarea(attrs={'class': 'form-control','rows': 1}), initial='', required=False)
    title = CharField(label='Товары (работы, услуги)', widget=Textarea(attrs={'class': 'form-control','rows': 2}), initial='', required=True)

    quantity = forms.DecimalField(label='Количество', max_digits=12, decimal_places=3,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control', 'style': 'width: 100%'}), initial=0, required=True)
    measure = ChoiceField(label='Ед. измерения', choices=SampleDetail.MEASURES, widget=Select(attrs={'class': 'form-select'}))
    price = forms.DecimalField(label='Цена за ед.', max_digits=20, decimal_places=2,
                                  widget=forms.widgets.NumberInput(attrs={'class': 'form-control','style': 'width: 100%'}))

    def clean_quantity(self):
        val = self.cleaned_data['quantity']
        if val < 0:
            raise ValidationError('Укажите корректное количество материалов/услуг!')
        return val

    class Meta:
        model = OrderDetail
        fields = ("code", "title", "quantity", "measure", "price")
