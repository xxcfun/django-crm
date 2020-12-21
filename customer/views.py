from django.shortcuts import render
from django.views.generic import ListView

from customer.models import Customer


class CustomerView(ListView):
    model = Customer
    template_name = 'customer.html'
    paginate_by = 10
    context_object_name = 'customers'

    def get_queryset(self):
        user = self.request.session.get('user_id')
        return Customer.objects.filter(is_valid=True, user=user)


def customer_seach(request):
    pass


def customer_add(request):
    pass


def customer_detail(request):
    pass


def customer_edit(request):
    pass


def customer_delete(request):
    pass
