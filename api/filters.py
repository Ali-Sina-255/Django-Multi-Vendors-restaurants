from django_filters import FilterSet
from menu.models import Category , FootItem


class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'category_name':['exact']
        }