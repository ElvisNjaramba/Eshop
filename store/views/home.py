from django.shortcuts import render , redirect , HttpResponseRedirect

from store.models import Message
from store.models.product import Products
from store.models.category import Category
from django.views import View
from django.db.models import Q


# Create your views here.
class Index(View):

    def post(self , request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity<=1:
                        cart.pop(product)
                    else:
                        cart[product]  = quantity-1
                else:
                    cart[product]  = quantity+1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print('cart' , request.session['cart'])
        return redirect('homepage')



    def get(self , request):
        # print()
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products();

    data = {}
    data['products'] = products
    data['categories'] = categories
    context = {'products':products}
    print('you are : ', request.session.get('email'))
    return render(request, 'index.html', data)

def testimonial(request):
    return render(request, 'testimonial.html')

def about(request):
    return render(request, 'about.html')

def rate(request):
    return render(request, 'rate.html')

def contact(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        email = request.POST['email']
        phoneno = request.POST['phoneno']
        subject = request.POST['subject']
        message = request.POST['message']

        contactus_info = Message.objects.create()
        contactus_info.firstname = fname
        contactus_info.email = email
        contactus_info.phone = phoneno
        contactus_info.subject = subject
        contactus_info.message = message

        contactus_info.save()
        return redirect('contact')
    return render(request, 'contact.html')


