import os

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.template.loader import get_template
from django.http import HttpResponse, FileResponse
from django.views import View
from xhtml2pdf import pisa

import invoice
from Eshop import settings
from .models import LineItem, Invoice
from .forms import LineItemFormset, InvoiceForm
import pdfkit
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from .utils import render_to_pdf


class InvoiceListView(View):
    def get(self, *args, **kwargs):
        invoices = Invoice.objects.all()

        context = {
            "invoices":invoices,
        }
        return render(self.request, 'invoice/invoice-list.html', context)
    
    def post(self, request):        
        # import pdb;pdb.set_trace()
        invoice_ids = request.POST.getlist("invoice_id")
        invoice_ids = list(map(int, invoice_ids))

        update_status_for_invoices = int(request.POST['status'])
        invoices = Invoice.objects.filter(id__in=invoice_ids)
        # import pdb;pdb.set_trace()
        if update_status_for_invoices == 0:
            invoices.update(status=False)
        else:
            invoices.update(status=True)

        return redirect('invoice:invoice-list')


def createInvoice(request):
    """
    Invoice Generator page it will have Functionality to create new invoices, 
    this will be protected view, only admin has the authority to read and make
    changes here.
    """

    heading_message = 'Formset Demo'
    if request.method == 'GET':
        formset = LineItemFormset(request.GET or None)
        form = InvoiceForm(request.GET or None)
    elif request.method == 'POST':
        formset = LineItemFormset(request.POST)
        form = InvoiceForm(request.POST)

        if form.is_valid():
            invoice = Invoice.objects.create(customer=form.data["customer"],
                                             customer_email=form.data["customer_email"],
                                             billing_address=form.data["billing_address"],
                                             date=form.data["date"],
                                             due_date=form.data["due_date"],
                                             message=form.data["message"],
                                             )
            # invoice.save()

        if formset.is_valid():
            # import pdb;pdb.set_trace()
            # extract name and other data from each form and save
            total = 0
            for form in formset:
                service = form.cleaned_data.get('service')
                description = form.cleaned_data.get('description')
                quantity = form.cleaned_data.get('quantity')
                rate = form.cleaned_data.get('rate')
                if service and description and quantity and rate:
                    amount = float(rate) * float(quantity)
                    total += amount
                    LineItem(customer=invoice,
                             service=service,
                             description=description,
                             quantity=quantity,
                             rate=rate,
                             amount=amount).save()
            invoice.total_amount = total
            invoice.save()
            try:
                print("helo")#generate_PDF(request, id=invoice.id)
            except Exception as e:
                print(f"********{e}********")
            return redirect('dashboard')
    context = {
        "title": "Invoice Generator",
        "formset": formset,
        "form": form,
    }
    return render(request, 'invoice/invoice-create.html', context)


def view_PDF(request, id=None):
    invoice = get_object_or_404(Invoice, id=id)
    lineitem = invoice.lineitem_set.all()

    context = {
        "company": {
            "name": "Rochad Enterprises",
            "address" :"P.o Box 101, Nairobi, Ruai, Kenya",
            "phone": "0795002100",
            "email": "rochadenterprises@gmail.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "lineitem": lineitem,

    }
    return render(request, 'invoice/pdf_template.html', context)

from django.template.loader import get_template
from django.template import Context


from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
import io

from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

def generate_PDF(request, id=id):
    invoice = get_object_or_404(Invoice, id=id)
    line_items = invoice.lineitem_set.all()
    template = get_template('invoice/pdf_template.html')
    context = {
        "company": {
            "name": "Rochad Enterprises",
            "address": "P.o Box 101, Nairobi, Ruai, Kenya",
            "phone": "0795002100",
            "email": "rochadenterprises@gmail.com",
        },
        "invoice_id": invoice.id,
        "invoice_total": invoice.total_amount,
        "customer": invoice.customer,
        "customer_email": invoice.customer_email,
        "date": invoice.date,
        "due_date": invoice.due_date,
        "billing_address": invoice.billing_address,
        "message": invoice.message,
        "line_items": line_items,
    }
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'

    pisa.CreatePDF(html, dest=response)

    return response

def change_status(request):
    return redirect('invoice:invoice-list')

def view_404(request,  *args, **kwargs):

    return redirect('invoice:invoice-list')

#def upload_product_from_excel(request):
    # Upload excel file to static folder "excel"
    # add all product to database
    # save product to database
    # redirect to view_product
    #excelForm = excelUploadForm(request.POST or None, request.FILES or None)
    #print("Reached HERE!")
    #if request.method == "POST":
        #print("Reached HERE2222!")

        #handle_file_upload(request.FILES["excel_file"])
        #excel_file = "static/excel/masterfile.xlsx"
        #df = pd.read_excel(excel_file)
        #Product.objects.all().delete()
        #for index, row in df.iterrows():
            #product = Product(
                #product_name=row["product_name"],
                #product_price=row["product_price"],
                #product_unit=row["product_unit"],
            #)
            #print(product)
            #product.save()
        #return redirect("view_product")
    #return render(request, "invoice/upload_products.html", {"excelForm": excelForm})
