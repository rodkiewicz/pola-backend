import django_filters
from dal import autocomplete
from django import forms
from django.utils.translation import ugettext_lazy as _

from company.models import Company
from pola.filters import CrispyFilterMixin

from .models import Product


class NullProductFilter(django_filters.Filter):
    field_class = forms.BooleanField

    def filter(self, qs, value):
        if value:
            return qs.filter(company=None)
        return qs


class ProductFilter(CrispyFilterMixin, django_filters.FilterSet):
    company_empty = NullProductFilter(label="Tylko produkty bez producenta")

    companies = django_filters.ModelChoiceFilter(
        label="Producent",
        queryset=Company.objects.all(),
        widget=autocomplete.ModelSelect2(url='company:company-autocomplete'),
    )

    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'code': ['icontains'],
        }
        order_by = (
            ('name', _('Nazwa (A-Z)')),
            ('-name', _('Nazawa (Z-A)')),
            ('query_count', _('Liczba zeskanowań (rosnąco)')),
            ('-query_count', _('Liczba zeskanowań (malejąco)')),
        )
