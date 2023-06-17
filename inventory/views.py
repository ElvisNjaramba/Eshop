from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Supplier, Product
from django.contrib.auth.decorators import login_required
from .forms import SupplierForm, AddProductForm
from django_pandas.io import read_frame
import plotly
import plotly.express as px
import json


# Create your views here.
def inventory_list(request):
    inventories = Product.objects.all()
    df = read_frame(inventories)

    product_in_stock = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    product_in_stock = px.pie(product_in_stock, names=product_in_stock.index, values=product_in_stock.quantity_in_stock,
                              title="Product in Stock")
    product_in_stock = json.dumps(product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)
    context = {
        "inventories": inventories,
        "product_in_stock": product_in_stock
    }
    return render(request, 'base/inventory_list.html', context)


@login_required
def per_product(request, pk):
    inventory = get_object_or_404(Product, pk=pk)
    context = {
        'inventory': inventory
    }
    return render(request, 'base/inventory_product.html', context)


from django.views.generic import ListView
from django.contrib.auth.decorators import login_required


# Supplier views
@login_required(login_url='login')
def create_supplier(request):
    forms = SupplierForm()
    if request.method == 'POST':
        forms = SupplierForm(request.POST)
        if forms.is_valid():
            name = forms.cleaned_data['name']
            address = forms.cleaned_data['address']
            email = forms.cleaned_data['email']
            username = forms.cleaned_data['username']
            password = forms.cleaned_data['password']
            retype_password = forms.cleaned_data['retype_password']
            if password == retype_password:
                user = User.objects.create_user(username=username, password=password, email=email, is_supplier=True)
                Supplier.objects.create(user=user, name=name, address=address)
                return redirect('supplier-list')
    context = {
        'form': forms
    }
    return render(request, 'store/addSupplier.html', context)


def add_products(request):
    inventories = Product.objects.all()
    inventory_count = inventories.count()
    inventory_quantity = Product.objects.filter(name='')
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard-products')
    else:
        form = AddProductForm()
    context = {
        'inventories': inventories,
        'form': form,
        'inventory_count': inventory_count,
    }
    return render(request, 'base/inventory_add.html', context)


def dashboard(request):
    inventories = Product.objects.all()
    df = read_frame(inventories)

    sales_graph = df.groupby(by="last_sales_date", as_index=False, sort=False)['sales'].sum()
    sales_graph = px.line(sales_graph, x=sales_graph.last_sales_date, y=sales_graph.sales, title="Sales Trend")
    sales_graph = json.dumps(sales_graph, cls=plotly.utils.PlotlyJSONEncoder)

    best_perfoming_product = df.groupby(by="name").sum().sort_values(by="quantity_sold")
    best_perfoming_product = px.bar(best_perfoming_product, x=best_perfoming_product.index,
                                    y=best_perfoming_product.quantity_sold, title="Best Performing Product")
    best_perfoming_product = json.dumps(best_perfoming_product, cls=plotly.utils.PlotlyJSONEncoder)

    product_in_stock = df.groupby(by="name").sum().sort_values(by="quantity_in_stock")
    product_in_stock = px.pie(product_in_stock, names=product_in_stock.index, values=product_in_stock.quantity_in_stock,
                              title="Product in Stock")
    product_in_stock = json.dumps(product_in_stock, cls=plotly.utils.PlotlyJSONEncoder)

    context = {
        "inventories": inventories,
        "sales_graph": sales_graph,
        "best_perfoming_product": best_perfoming_product,
        "product_in_stock": product_in_stock
    }
    return render(request, "base/dashboard.html", context)


class ProductListView(ListView):
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'product'
