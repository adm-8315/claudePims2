from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import (
    Item, Material, Product,
    Iteminventory, MaterialInventory, ProductInventory,
    MaterialTransaction, ProductTransaction
)

class ItemListView(LoginRequiredMixin, ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add inventory levels for each item
        for item in context['items']:
            item.inventory_levels = Iteminventory.objects.filter(item=item)
        return context

class MaterialListView(LoginRequiredMixin, ListView):
    model = Material
    template_name = 'inventory/material_list.html'
    context_object_name = 'materials'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add inventory levels for each material
        for material in context['materials']:
            material.inventory_levels = MaterialInventory.objects.filter(material=material)
        return context

class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'inventory/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add inventory levels for each product
        for product in context['products']:
            product.inventory_levels = ProductInventory.objects.filter(product=product)
        return context

class MaterialDetailView(LoginRequiredMixin, DetailView):
    model = Material
    template_name = 'inventory/material_detail.html'
    context_object_name = 'material'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_levels'] = MaterialInventory.objects.filter(material=self.object)
        context['transactions'] = MaterialTransaction.objects.filter(
            materialinventory__material=self.object
        ).order_by('-transactiondate')[:10]  # Last 10 transactions
        return context

class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'inventory/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inventory_levels'] = ProductInventory.objects.filter(product=self.object)
        context['transactions'] = ProductTransaction.objects.filter(
            productinventory__product=self.object
        ).order_by('-transactiondate')[:10]  # Last 10 transactions
        return context

class MaterialTransactionCreateView(LoginRequiredMixin, CreateView):
    model = MaterialTransaction
    template_name = 'inventory/material_transaction_form.html'
    fields = ['materialinventory', 'transactiontype', 'quantity']
    success_url = reverse_lazy('inventory:material-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.companylocationlink = form.instance.materialinventory.companylocationlink
        return super().form_valid(form)

class ProductTransactionCreateView(LoginRequiredMixin, CreateView):
    model = ProductTransaction
    template_name = 'inventory/product_transaction_form.html'
    fields = ['productinventory', 'transactiontype', 'quantity']
    success_url = reverse_lazy('inventory:product-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.companylocationlink = form.instance.productinventory.companylocationlink
        return super().form_valid(form)
