from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4
import os


# Create your models here.

class Request(models.Model):
    title = models.TextField('Примечание', null=False, blank=False, default='Пусто')
    date = models.DateTimeField('Дата создания', editable=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    STATUSES = (
        ('c', 'Создано'),
        ('r', 'На исполнении'),
        ('x', 'Завершено'),
    )
    status = models.CharField(max_length=1, choices=STATUSES)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Goods(models.Model):
    name = models.TextField('Наименование', null=False, blank=False, default='Пусто')
    SUPPLY = (
        ('m', 'Материалы'),
        ('t', 'Инструменты'),
    )
    type = models.CharField(max_length=1, choices=SUPPLY)
    MEASURES = (
        ('kg', 'кг'),
        ('kk', 'т.'),
        ('m3', 'м3'),
        ('m2', 'кв.м'),
        ('pm', 'пг.м'),
        ('pc', 'шт.'),
        ('2p', 'пар.'),
    )
    measure = models.CharField(max_length=2, choices=MEASURES)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Материал/инструмент'
        verbose_name_plural = 'Материалы/инструменты'


class Details(models.Model):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return '[' + self.request.title + ']' + self.goods.name

    class Meta:
        verbose_name = 'Позиция заявки'
        verbose_name_plural = 'Позиции заявки'


class Object(models.Model):
    name = models.TextField('Описание', null=False, blank=False, default='Пусто')

    special = models.BooleanField('Использовать в заявках', null=False, blank=False, default=True)

    def __str__(self):
        return '[' + self.name + ']' # + self.goods.name

    class Meta:
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class Phase(models.Model):
    name = models.TextField('Описание', null=False, blank=False, default='Пусто')

    comment = models.TextField('Примечание', null=True, blank=True, default='')
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Этап строительства'
        verbose_name_plural = 'Этапы строительства'


class Bid(models.Model):
    number = models.TextField('Номер заявки', null=False, blank=False, default='0')
    title = models.TextField('Примечание', null=False, blank=False, default='Пусто')
    date = models.DateTimeField('Дата создания', editable=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    locked = models.BooleanField('Заблокировано', null=False, blank=False, default=False)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    highlighted = models.BooleanField('Подписано', null=False, blank=False, default=False)

    supervision = models.BooleanField('Техконтроль', null=False, blank=False, default=False)
    supervisor = models.TextField('Контролёр', null=False, blank=False, default='')

    hidden = models.BooleanField('Скрыта', null=False, blank=False, default=False)

    refunded = models.BooleanField('Возвращена', null=False, blank=False, default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class Archive(models.Model):
    #number = models.IntegerField('Номер заявки', null=False, blank=False, default=0)
    number = models.TextField('Номер заявки', null=False, blank=False, default='0')
    title = models.TextField('Примечание', null=False, blank=False, default='Пусто')
    date = models.DateTimeField('Дата создания', editable=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    #locked = models.BooleanField('Заблокировано', null=False, blank=False, default=False)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    highlighted = models.BooleanField('Помечено', null=False, blank=False, default=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Архивная заявка'
        verbose_name_plural = 'Архивные заявки'


class House(models.Model):
    name = models.TextField('Описание', null=False, blank=False, default='Пусто')
    object = models.ForeignKey(Object, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'


class Supplier(models.Model):
    name = models.TextField('Название поставщика', null=False, blank=False)
    type = models.CharField(max_length=1, default='0')

    comment = models.TextField('Примечание', null=True, blank=True, default='')
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'


class Estimate(models.Model):
    name = models.TextField('Название сметы', null=False, blank=False)

    comment = models.TextField('Примечание', null=True, blank=True, default='')
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Смета'
        verbose_name_plural = 'Сметы'

class CashRegister(models.Model):
    name = models.TextField('Название кассы', null=False, blank=False)

    STATUSES = (
        ('0', 'Касса'),
        ('1', 'Общий'),
        ('2', 'Внешний'),
    )
    status = models.CharField(max_length=1, choices=STATUSES, default='0')

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Касса'
        verbose_name_plural = 'Кассы'

class SubCash(models.Model):
    name = models.TextField('Название локальной кассы', null=False, blank=False)
    cashregister = models.ForeignKey(CashRegister, on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, default=0.0)
    date = models.DateTimeField('Остаток на дату', editable=True)
    closedate = models.DateTimeField('Дата закрытия', null=True, blank=True, editable=True)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Локальная касса'
        verbose_name_plural = 'Локальнаые кассы'

class Account(models.Model):
    name = models.TextField('Название счета', null=False, blank=False)
    cashregister = models.ForeignKey(CashRegister, on_delete=models.CASCADE)

    balance = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, default=0.0)
    date = models.DateTimeField('Остаток на дату', editable=True)
    closedate = models.DateTimeField('Дата закрытия', null=True, blank=True, editable=True)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'

class Earning(models.Model):
    comment = models.TextField('Пояснения', null=False, blank=False)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)

    date = models.DateTimeField('Дата', editable=True)
    summary = models.DecimalField('Сумма', max_digits=12, decimal_places=2, null=False, blank=False)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True)

    subcash = models.ForeignKey(SubCash, on_delete=models.CASCADE)
    expense_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expense_account')
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_account')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    locked = models.BooleanField('Заблокировано', null=False, blank=False, default=False)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    #highlighted = models.BooleanField('Подписано', null=False, blank=False, default=False)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Доход'
        verbose_name_plural = 'Доходы'


class Content(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    title = models.TextField('Описание', null=False, blank=False, default='Пусто')
    date = models.DateTimeField('Дата', editable=True)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE)
    SUPPLY = (
        ('a', 'Материалы'),
        ('b', 'Работа'),
        ('c', 'Техника'),
        ('d', 'Доставка'),
        ('e', 'Перемещение'),
        ('f', 'Прочие расходы'),
    )
    type = models.CharField(max_length=1, choices=SUPPLY)
    CASHLESS = (
        ('y', 'Нал'),
        ('n', 'Безнал'),
        ('b', 'Бартер'),
    )
    cash = models.CharField(max_length=1, choices=CASHLESS)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False, default=0)
    MEASURES = (
        ('kg', 'кг'),
        ('kk', 'т.'),
        ('m1', 'м.'),
        ('m3', 'м3'),
        ('m2', 'кв.м'),
        ('pm', 'пог.м'),
        ('pc', 'шт.'),
        ('2p', 'пар.'),
        ('bx', 'упак'),
        ('hh', 'час.'),
        ('lt', 'л.'),
        ('mt', 'мл.'),
        ('hu', 'чел.'),
        ('on', 'ед.'),
        ('ms', 'машина'),
        ('st', 'комплект'),
        ('--', 'доставка'),
    )
    measure = models.CharField(max_length=2, choices=MEASURES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    comment = models.TextField('Описание', null=False, blank=False)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)

    expense_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='expense_account2', null=True, default=None)
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_account2', null=True, default=None)

    history = models.TextField('История изменений', null=True, blank=True, default='')

    subcash = models.ForeignKey(SubCash, on_delete=models.CASCADE, null=True, default=None)

    prepaid = models.BooleanField('Оплата после доставки', null=False, blank=False, default=False)

    def __str__(self):
        return '[' + self.title + ']' # + self.goods.name

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказа'


class Contract(models.Model):
    title = models.TextField('Описание', null=True, blank=True, default='')
    date = models.DateTimeField('Дата создания', editable=True)
    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    client = models.TextField('Клиент', null=False, blank=False, default='')
    clientphone = models.TextField('Телефон клиента', null=True, blank=True, default='')
    agency = models.TextField('Агентство/агент/менеджер', null=False, blank=False, default='')
    agencyphone = models.TextField('Телефон агентства', null=False, blank=False, default='')
    apartment = models.TextField('Апартамент', null=False, blank=False, default='')
    square = models.DecimalField('Площадь', max_digits=12, decimal_places=2, null=False, blank=False)
    price = models.DecimalField('Цена по шахматке', max_digits=12, decimal_places=2, null=False, blank=False)
    agency_discount = models.DecimalField('Скидка АН', max_digits=12, decimal_places=2, null=False, blank=False, default=0)
    developer_discount = models.DecimalField('Скидка застройщика', max_digits=12, decimal_places=2, null=False, blank=False, default=0)

    seller_commission_calc = models.TextField('Расчет комиссии ОП', null=False, blank=False, default='')
    seller_commission = models.DecimalField('Комиссия ОП', max_digits=12, decimal_places=2, null=False, blank=False, default=0)
    agency_commission_calc = models.TextField('Расчет комиссии АН', null=False, blank=False, default='')
    agency_commission = models.DecimalField('Комиссия АН', max_digits=12, decimal_places=2, null=False, blank=False, default=0)

    installment = models.TextField('Срок рассрочки', null=True, blank=True, default='')

    SLATUSES = (
        ('a', 'Создан'),
        ('b', 'Проверен бухгалтером'),
        ('c', 'На исполнении'),
        ('d', 'Исполнен'),
    )
    status = models.CharField(max_length=1, choices=SLATUSES)

    TYPES = (
        ('a', 'ДИ'),
        ('b', 'ДБ'),
        ('c', 'ДКП'),
    )
    type = models.CharField(max_length=1, choices=TYPES, default='a')
    number = models.TextField('Номер контракта', null=False, blank=False, default='0')

    receipt = models.BooleanField('Чек отбит', null=False, blank=False, default=False)
    onhand = models.BooleanField('Оригинал в наличии', null=False, blank=False, default=False)

    reservation_date = models.DateTimeField('Дата виртуального бронирования', editable=False, null=True, blank=True)
    RTYPES = (
        ('a', 'Нет брони'),
        ('b', 'Запрос виртуального бронирования'),
        ('c', 'Забронировано'),
    )
    reservation_type = models.CharField(max_length=1, choices=RTYPES, default='a')

    revoked = models.BooleanField('Контракт аннулирован', null=False, blank=False, default=False)
    comment = models.TextField('Комментарий', null=False, blank=False, default='')

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.get_type_display() + '-' + self.number

    class Meta:
        verbose_name = 'Контракт'
        verbose_name_plural = 'Контракты'

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return "images/user_{0}/{1}".format(instance.user.id, filename)

def path_and_rename_func(instance, filename, path):
    upload_to = path
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_image(instance, filename):
    return path_and_rename_func(instance, filename, 'image')

class ContractImage(models.Model):
    date = models.DateTimeField('Дата', editable=True)
    comment = models.TextField('Комментарий', null=False, blank=False, default='')
    image = models.ImageField(upload_to=path_and_rename_image)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return '[' + self.contract.number + ']' + self.comment

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

class Turnover(models.Model):
    date = models.DateTimeField('Планируемая дата совершения операции', editable=True)
    actualdate = models.DateTimeField('Реальная дата совершения операции', editable=True, null=True, blank=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    amount = models.DecimalField('Сумма', max_digits=12, decimal_places=2, null=False, blank=False)

    TYPES = (
        (1, 'Бронь'),
        (2, 'Поступление оплаты'),
        (100, 'Выплата комиссии ОП'),
        (101, 'Выплата комиссии АН'),
    )
    type = models.IntegerField('Тип операции', default=2, choices=TYPES, blank=False, null=False)
    comment = models.TextField('Комментарий', null=False, blank=False, default='')

    performed = models.BooleanField('Проведена', null=False, blank=False, default=False)

    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, null=True, default=None)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Операция по контракту'
        verbose_name_plural = 'Операции по контракту'


class Setting(models.Model):
    name = models.TextField('Описание', null=False, blank=False, default='')

    TYPES = (
        (1, 'int'),
        (2, 'string'),
        (3, 'boolean'),
        (4, 'date'),
    )
    type = models.IntegerField('Тип значения', default=1, choices=TYPES, blank=False, null=False)
    value = models.TextField('Значение', null=False, blank=False, default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'


class ArchiveDetail(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    title = models.TextField('Описание', null=False, blank=False, default='Пусто')
    date = models.DateTimeField('Дата', editable=True)
    archive = models.ForeignKey(Archive, on_delete=models.CASCADE)

    CASHLESS = (
        ('y', 'Нал'),
        ('n', 'Безнал'),
    )
    SUPPLY = (
        ('a', 'Материалы'),
        ('b', 'Работа'),
        ('c', 'Техника'),
        ('d', 'Доставка'),
        ('e', 'Перемещение'),
        ('f', 'Прочие расходы'),
    )
    type = models.CharField(max_length=1, choices=SUPPLY, default='f')

    cash = models.CharField(max_length=1, choices=CASHLESS)

    summary = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)

    comment = models.TextField('Описание', null=True, blank=True)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    supplier = models.TextField('Поставщик', null=True, blank=True)

    new_supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    # расходы (из столбца "расходы по смете")
    spending = models.TextField('Поставщик', null=True, blank=True)

    # материалы (из столбца "Использованные материалы/Вид техники")
    materials = models.TextField('Материалы', null=True, blank=True)

    phase = models.ForeignKey(Phase, on_delete=models.CASCADE)
    estimate = models.ForeignKey(Estimate, on_delete=models.CASCADE)

    # количество (если указано)
    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    # цена (если указана)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # единица измерения (если указана)
    measure = models.CharField(max_length=8, null=True, blank=True)

    # прораб (если указан)
    foreman = models.TextField('Прораб', null=True, blank=True)

    history = models.TextField('История изменений', null=True, blank=True, default='')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Позиция архивной заявки'
        verbose_name_plural = 'Позиции архивной заявки'


class Prepayment(models.Model):
    comment = models.TextField('Комментарий', null=False, blank=False, default='')
    date = models.DateTimeField('Дата создания', editable=True)
    summary = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    history = models.TextField('История изменений', null=True, blank=True, default='')

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Авансовый платёж'
        verbose_name_plural = 'Авансовые платежи'


class Delivery(models.Model):
    comment = models.TextField('Комментарий', null=False, blank=False, default='')
    date = models.DateTimeField('Дата создания', editable=True)
    volume = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    pumpcomment = models.TextField('Бетононасос', null=False, blank=True, default='')
    pumpsummary = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)

    pumptransfer = models.DecimalField('Переезд автобетононасоса', max_digits=12, decimal_places=2, null=False, blank=False, default=0)
    downtime = models.DecimalField('Количество часов простоя', max_digits=12, decimal_places=2, null=False, blank=False, default=0)
    downtimecost = models.DecimalField('Стоимость часа простоя', max_digits=12, decimal_places=2, null=False, blank=False, default=0)

    deliveryvolume = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)
    deliveryprice = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)

    GRADE = (
        ('a', '300'),
        ('b', '350'),
        ('c', '400'),
    )
    concrete_grade = models.CharField(max_length=1, choices=GRADE)

    pile = models.TextField('Информация', null=False, blank=True, default='')


    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    verified = models.BooleanField('Сверено', null=False, blank=False, default=True)

    history = models.TextField('История изменений', null=True, blank=True, default='')


    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Заливка бетона'
        verbose_name_plural = 'Заливки бетона'


class Sample(models.Model):
    title = models.TextField('Примечание', null=False, blank=False, default='')
    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)
    hidden = models.BooleanField('Скрыто', null=False, blank=False, default=False)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Шаблон заказа'
        verbose_name_plural = 'Шаблоны заказа'


class SampleDetail(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    code = models.TextField('Код', null=False, blank=True, default='')
    description = models.TextField('Описание', null=False, blank=False, default='')

    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False, default=0)
    MEASURES = (
        ('kg', 'кг'),
        ('kk', 'т.'),
        ('m1', 'м.'),
        ('m3', 'м3'),
        ('m2', 'кв.м'),
        ('pm', 'пог.м'),
        ('pc', 'шт.'),
        ('2p', 'пар.'),
        ('bx', 'упак'),
        ('lt', 'л.'),
        ('mt', 'мл.'),
        ('on', 'ед.'),
        ('ms', 'машина'),
        ('st', 'комплект'),
    )
    measure = models.CharField(max_length=2, choices=MEASURES)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'Позиция шаблона заказа'
        verbose_name_plural = 'Позиции шаблона заказа'


class Order(models.Model):
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    comment = models.TextField('Комментарий', null=False, blank=False, default='')

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField('Дата создания', editable=False)
    lastdate = models.DateTimeField('Дата последнего статуса', editable=False)

    object = models.ForeignKey(Object, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)

    STATUSES = (
        ('0', 'Создан'),
        ('1', 'У руководителя'),
        ('2', 'У снабженца'),
        ('3', 'У бухгалтера'),
        ('4', 'Поставка'),
        ('5', 'Доставлено полностью'),
        ('6', 'Не доставлено/есть замечания'),
        ('7', 'Завершён'),
    )
    status = models.CharField(max_length=1, choices=STATUSES)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return self.comment

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    code = models.TextField('Код', null=False, blank=True, default='')
    title = models.TextField('Комментарий', null=False, blank=False, default='')

    quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False, default=0)
    sample_quantity = models.DecimalField(max_digits=8, decimal_places=2, null=False, blank=False, default=0)

    price = models.DecimalField(max_digits=12, decimal_places=2, null=False, blank=False, default=0.0)

    measure = models.CharField(max_length=2, choices=SampleDetail.MEASURES)

    deleted = models.BooleanField('Удалено', null=False, blank=False, default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Деталь заказа'
        verbose_name_plural = 'Детали заказа'




