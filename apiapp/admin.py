from django.contrib import admin
from apiapp.models import Order,OrderItem
# Register your models he
class OrderItemInline(admin.TabularInline):
    model=OrderItem
class OrderAdmin(admin.ModelAdmin):
    inlines=[
        OrderItemInline,
    ]
admin.site.register(Order,OrderAdmin)