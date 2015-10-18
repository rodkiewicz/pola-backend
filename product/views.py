from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.decorators.cache import cache_page
from braces.views import LoginRequiredMixin, FormValidMessageMixin
from django.utils.translation import ugettext_lazy as _
from reportlab.graphics import renderPM
import reversion
from reversion.models import Version
from django_filters.views import FilterView
from .forms import ProductForm
from .filters import ProductFilter
from .images import Barcode
from . import models


class ProductDetailView(LoginRequiredMixin, DetailView):
    slug_field = 'code'
    model = models.Product
    queryset = models.Product.objects.with_query_count().all()


class ProductListView(LoginRequiredMixin, FilterView):
    model = models.Product
    filterset_class = ProductFilter
    paginate_by = 25
    queryset = models.Product.objects.with_query_count().all()


class ProductCreate(LoginRequiredMixin, FormValidMessageMixin, CreateView):
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    form_valid_message = _(u"Product created!")


class ProductUpdate(LoginRequiredMixin, FormValidMessageMixin, UpdateView):
    slug_field = 'code'
    model = models.Product
    form_class = ProductForm
    form_valid_message = _(u"Product updated!")


class ProductDelete(LoginRequiredMixin, FormValidMessageMixin,  DeleteView):
    slug_field = 'code'
    model = models.Product
    success_url = reverse_lazy('product:list')
    form_valid_message = _(u"Product deleted!")


class ProductHistoryView(LoginRequiredMixin, ListView):
    slug_field = 'code'
    model = Version
    revision_model = models.Product
    template_name = 'product/product_history.html'

    def get_object(self):
        slug_field = self.slug_field
        slug = self.kwargs['slug']
        return self.revision_model.objects.get(**{slug_field: slug})

    def get_queryset(self):
        self.queryset = reversion.get_for_object(self.get_object())
        return super(ProductHistoryView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(ProductHistoryView, self).get_context_data(**kwargs)
        context['object'] = self.get_object()
        return context


class ProductHistoryDetailAjaxView(LoginRequiredMixin, DetailView):
    # TODO: Fix display related objects
    # See:
    # https://github.com/etianen/django-reversion/blob/master/src/reversion/admin.py#L182-L199
    model = Version
    revision_model = models.Product
    template_name = 'product/product_history_detail.html'

    def get_queryset(self):
        return reversion.get_for_object(self.get_revision_object())

    def get_revision_object(self):
        product_code = self.kwargs['code']
        return self.revision_model.objects.get(code=product_code)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        revision_id = self.kwargs['pk']
        return queryset.get(pk=revision_id)

    def get_context_data(self, **kwargs):
        import ipdb; ipdb.set_trace()
        return super(
            ProductHistoryDetailAjaxView,
            self).get_context_data(**kwargs)


@cache_page(0)
def get_image(request, code):
    response = HttpResponse(content_type="image/png")
    # barcode = Barcode.get_barcode(value=code, width=600)
    # data = renderPM.drawToString(barcode, fmt='PNG')
    # response.write(data)
    return response
