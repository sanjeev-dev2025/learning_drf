from apiapp.models import Product
import django_filters
from rest_framework import filters
class InStockProductFilter(filters.BaseFilterBackend):
    def filter_queryset(self,request,queryset,view):
        return queryset.filter(stock__gt=0,price__gt=0)

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model=Product
        fields={
           "name": ["iexact","icontains"],
           "price": ["exact", "gt", "lt"]
       }