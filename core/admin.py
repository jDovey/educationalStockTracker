from django.contrib import admin

from .models import Transactions, Holdings
# Register your models here.
admin.site.register(Transactions)
admin.site.register(Holdings)