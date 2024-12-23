from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import (
    ProductionOrder,
    ProductionOrderSchedule,
    ProductionOrderScheduleBatching,
    Form,
    FurnacePattern
)

class ProductionOrderListView(LoginRequiredMixin, ListView):
    model = ProductionOrder
    template_name = 'production/production_order_list.html'
    context_object_name = 'production_orders'
    
    def get_queryset(self):
        queryset = ProductionOrder.objects.select_related(
            'product',
            'form',
            'furnacepattern',
            'user'
        ).filter(active=True)
        
        # Add filters based on query parameters
        if self.request.GET.get('product'):
            queryset = queryset.filter(product__productid=self.request.GET['product'])
        if self.request.GET.get('status'):
            if self.request.GET['status'] == 'completed':
                queryset = queryset.filter(quantityfilled__gte=models.F('quantityordered'))
            elif self.request.GET['status'] == 'in_progress':
                queryset = queryset.filter(quantityfilled__lt=models.F('quantityordered'))
        
        return queryset.order_by('-lastedit')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Production Orders'
        return context

class ProductionOrderDetailView(LoginRequiredMixin, DetailView):
    model = ProductionOrder
    template_name = 'production/production_order_detail.html'
    context_object_name = 'production_order'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Production Order {self.object.productionorderid}'
        context['schedules'] = self.object.productionorderschedule_set.filter(
            active=True
        ).order_by('pourdate')
        return context

class ProductionOrderCreateView(LoginRequiredMixin, CreateView):
    model = ProductionOrder
    template_name = 'production/production_order_form.html'
    fields = [
        'product',
        'quantityordered',
        'form',
        'taps',
        'lowerspec',
        'upperspec',
        'furnacepattern',
        'notes'
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Production Order'
        context['forms'] = Form.objects.all()
        context['furnace_patterns'] = FurnacePattern.objects.select_related('furnace').all()
        return context
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.lastedit = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('production:order_detail', kwargs={'pk': self.object.pk})

class ProductionOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = ProductionOrder
    template_name = 'production/production_order_form.html'
    fields = [
        'product',
        'quantityordered',
        'quantityfilled',
        'filldate',
        'form',
        'taps',
        'lowerspec',
        'upperspec',
        'furnacepattern',
        'notes',
        'active'
    ]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Production Order {self.object.productionorderid}'
        context['forms'] = Form.objects.all()
        context['furnace_patterns'] = FurnacePattern.objects.select_related('furnace').all()
        return context
    
    def form_valid(self, form):
        form.instance.lastedit = timezone.now()
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('production:order_detail', kwargs={'pk': self.object.pk})

class ProductionOrderScheduleCreateView(LoginRequiredMixin, CreateView):
    model = ProductionOrderSchedule
    template_name = 'production/schedule_form.html'
    fields = ['pourdate', 'stripdate', 'firedate', 'quantity']
    
    def dispatch(self, request, *args, **kwargs):
        self.production_order = get_object_or_404(ProductionOrder, pk=kwargs['order_pk'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Schedule Production Order {self.production_order.productionorderid}'
        context['production_order'] = self.production_order
        # Calculate remaining quantity
        filled = self.production_order.quantityfilled or 0
        context['remaining_quantity'] = self.production_order.quantityordered - filled
        return context
    
    def form_valid(self, form):
        form.instance.productionorder = self.production_order
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('production:order_detail', kwargs={'pk': self.production_order.pk})
