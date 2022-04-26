from django.shortcuts import render, get_object_or_404
from django.db.models import Prefetch
from .models import Product
from .forms import ProductFilterForm

def index(request):
    Product.objects.prefetch_related(Prefetch('productimage_set'))
    form = ProductFilterForm(request.GET)
    if request.GET != {}: #check for query parameters in the get request
      toSort = request.GET.get('sort')
      if toSort != None:
        products = Product.objects.all().order_by(toSort) #sort by this
        request.session['sort'] = toSort
      else:
        min = request.GET.get('min_price')
        max = request.GET.get('max_price')
        if min != "" and max != "":
          request.session['max'] = max
          request.session['min'] = min
          products = Product.objects.all().filter(price__lte=max).filter(price__gte=min)
        elif min == "" and max != "":
          products = Product.objects.all().filter(price__lte=max)
          request.session['max'] = max
        elif min != "" and max == "":
          request.session['min'] = min
          products = Product.objects.all().filter(price__gte=min)
        else:
          products = Product.objects.all().order_by('name') #if no filters present use name
    else:
      products = Product.objects.all().order_by('name') #otherwise sort by name
    name_search = request.GET.get('name_search')
    if name_search:
      products = products.filter(name__icontains=name_search)
      request.session['name'] = name_search 
    context = {'products': products, 'form': form}
    return render(request, 'products/index.html', context)
      

def show(request, product_id):
    p = get_object_or_404(Product, pk=product_id)
    context = { 'product':p }
    return render(request, 'products/show.html', context)
    
