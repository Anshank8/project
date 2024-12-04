from django.contrib import admin
from .models import Coffee,Cart,Orderp
# Register your models here.

class Coffeadmin(admin.ModelAdmin):
    list_display=["name","price"]
admin.site.register(Coffee,Coffeadmin)

class Cartadmin(admin.ModelAdmin):
    list_display=['userid',"itemname",'itemprice']
admin.site.register(Cart,Cartadmin)

class Orderadmin(admin.ModelAdmin):
    list_display=['fname',"lname",'userid','ispaid']
admin.site.register(Orderp,Orderadmin)



