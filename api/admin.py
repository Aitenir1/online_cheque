from django.contrib import admin
from .models import Dish, Table, Category, Order, OrderItem, Additive

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('dish',)

#
# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInline]
#     list_display = ('id', 'table', 'time_created', 'get_dishes', 'total_price')
#
#     def get_dishes(self, obj):
#         dishes = Dish.objects.filter(orderitem__order=obj)
#         dish_names = ', '.join([dish.name_en for dish in dishes])
#         return dish_names
#
#     get_dishes.short_description = 'Dishes'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'table', 'status', 'time_created', 'total_price']
    list_filter = ['status', 'table']
    date_hierarchy = 'time_created'

admin.site.register(Dish)
admin.site.register(Table)
admin.site.register(Category)
# admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(Additive)
