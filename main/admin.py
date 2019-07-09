from django.contrib import admin
from main.models import *
# Register your models here.  
admin.site.register(option)
    
admin.site.register(specification)

admin.site.register(catagory)

admin.site.register(img)

class SKU_display(admin.ModelAdmin):
    list_display=('SKU_id','price','amount','belong')

admin.site.register(SKU,SKU_display)


class SPU_display(admin.ModelAdmin):
    list_display=('SPU_id','name')

admin.site.register(SPU,SPU_display)

class store_display(admin.ModelAdmin):
    list_display=('store_id','name')

admin.site.register(store,store_display)


class order_display(admin.ModelAdmin):
    list_display=('order_id','create_time','payment_time','confirm_time')

admin.site.register(order,order_display)

class customer_display(admin.ModelAdmin):
    list_display=('uuid','nickname','address','phone_number')

admin.site.register(customer,customer_display)