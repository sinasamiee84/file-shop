from django.views.generic import DetailView, ListView

from apps.products.models import Product


class ProductListView(ListView):
    model = Product
    queryset = Product.objects.filter(is_active=True)
    context_object_name = "products"
    template_name = "products/product_list.html"
    paginate_by = 12


class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"

    slug_field = "slug"
    slug_url_kwarg = "slug"
