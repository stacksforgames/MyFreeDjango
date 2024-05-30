from django.contrib import admin
from .models import Request
from .models import Goods
from .models import Details
from .models import Bid
from .models import Content
from .models import Object
from .models import House
from .models import Phase
from .models import Supplier
from .models import Estimate
from .models import Archive
from .models import ArchiveDetail
from .models import Prepayment
from .models import Delivery
from .models import Sample
from .models import SampleDetail
from .models import CashRegister
from .models import SubCash
from .models import Account
from .models import Earning
from .models import Contract
from .models import Turnover
from .models import Setting
from .models import ContractImage

admin.site.register(Request)
admin.site.register(Goods)
admin.site.register(Details)

admin.site.register(Bid)
admin.site.register(Content)
admin.site.register(Object)
admin.site.register(House)
admin.site.register(Phase)
admin.site.register(Supplier)
admin.site.register(Estimate)
admin.site.register(Archive)
admin.site.register(ArchiveDetail)
admin.site.register(Prepayment)
admin.site.register(Delivery)
admin.site.register(Sample)
admin.site.register(SampleDetail)
admin.site.register(CashRegister)
admin.site.register(SubCash)
admin.site.register(Account)
admin.site.register(Earning)
admin.site.register(Contract)
admin.site.register(Turnover)
admin.site.register(Setting)
admin.site.register(ContractImage)



