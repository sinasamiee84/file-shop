from django.db.models import Prefetch
from django.views.generic import DetailView, ListView
from apps.products.models import Category, Product
from django.db.models import Q, Prefetch

class ProductListView(ListView):
    model = Category
    context_object_name = "categories"
    template_name = "products/product_list.html"

    def get_queryset(self):
        query = self.request.GET.get("q", "").strip()

        product_filter = Q(is_active=True)

        if query:
            product_filter &= (
                Q(title__icontains=query)
                | Q(description__icontains=query)
            )

        active_products = Product.objects.filter(product_filter).order_by(
            "-created_at"
        )

        categories = Category.objects.prefetch_related(
            Prefetch(
                "products",
                queryset=active_products,
                to_attr="active_products",
            )
        ).filter(products__is_active=True)

        if query:
            categories = categories.filter(
                Q(products__title__icontains=query)
                | Q(products__description__icontains=query)
            )

        return categories.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "").strip()
        return context

class ProductDetailView(DetailView):
    model = Product
    context_object_name = "product"
    template_name = "products/product_detail.html"

    slug_field = "slug"
    slug_url_kwarg = "slug"
class CategoryDetailView(DetailView):
    model = Category
    context_object_name = "category"
    template_name = "products/category_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # گرفتن محصولات فعال این دسته‌بندی
        context["products"] = self.object.products.filter(is_active=True).order_by("-created_at")
        return context
