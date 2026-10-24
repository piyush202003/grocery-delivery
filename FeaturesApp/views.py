from decimal import Decimal

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from FeaturesApp.forms import AddressForm
from accounts.models import Address

from .dummyData import dummyProducts, dummyCategoriesData, generate_dummy_reviews, get_rating_breakdown, dummyDashboardOrdersData, statusColors, dummyAddressData
from .models import CartItem, Category, Order, OrderItem, OrderStatus, Product

# Create your views here.
def Home(request):

    categories = Category.objects.all().order_by('slug')

    popularProducts = Product.objects.all().order_by('-rating')[:10]

    context = {
        "categoriesData" : categories,
        "products" : popularProducts,
        "cart" : cart(request)
    }
    return render(request, "Home.html", context=context)

def cart(request):
    
    cart_items = []
    cart_total = Decimal('0')
    cart_count = 0

    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        for item in items:
            total_price = item.product.price * item.quantity
            cart_items.append({
                'product':item.product,
                'quantity':item.quantity,
                'total':total_price,
            })
            cart_total += total_price
            cart_count += 1
    else:
        cart = request.session.get("cart", {})
        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            if product:
                total_price = product.price * quantity
                cart_items.append({
                    "product":product,
                    "quantity":quantity,
                    "total":total_price,
                })
                cart_total += total_price
                cart_count += 1
    
    delivery_fee = Decimal('0')
    if cart_total <= Decimal('20'):
        delivery_fee = Decimal(1.99)

    tax = cart_total * Decimal(0.08)
    tax = round(tax, 2)

    context = {
        "cart_items":cart_items,
        "cart_total":cart_total,
        "cart_count":cart_count,
        "grand_total": cart_total + delivery_fee,
        "delivery_fee":delivery_fee,
        'tax':tax,
        'last_total': cart_total + delivery_fee + tax,
    }

    return context

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product.stock <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect(request.META.get("HTTP_REFERER", "Home"))
    
    if request.user.is_authenticated:
        item = CartItem.objects.filter(user=request.user, product=product).first()
        if item:
            item.quantity += 1
            item.save()
        else:
            CartItem.objects.create(
                user=request.user,
                product=product,
                quantity=1,
            )
    else:
        cart = request.session.get("cart",{})
        product_id = str(product_id)
        if product_id in cart:
            cart[product_id] += 1
        else:
            cart[product_id] = 1
        request.session['cart'] = cart

    messages.success(request, 'Product Added in Cart')
    return redirect(request.META.get("HTTP_REFERER", "Home"))

def remove_from_cart(request, product_id):

    if request.user.is_authenticated:
        item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
        item.delete()
    else:
        cart = request.session.get('cart',{})
        product_id = str(product_id)
        if product_id in cart:
            del cart[product_id]
        request.session['cart'] = cart
    messages.warning(request, 'Item has been removed from Cart')
    return redirect(request.META.get("HTTP_REFERER", "Home"))

def update_cart(request, product_id):

    if request.method == "POST":

        action = request.POST.get("action")
        if action not in ['increase', 'decrease']:
            messages.error(request, 'Invalid cart action.')
            return redirect(request.META.get('HTTP_REFERER','Home'))

        if request.user.is_authenticated:
            item = get_object_or_404(CartItem, user=request.user, product__id=product_id)
            if action == 'increase':
                if item.quantity >= item.product.stock:
                    messages.warning(request, 'You cannot add more than the availabel stock!')
                    return redirect(request.META.get('HTTP_REFERER', 'Home'))
                item.quantity+=1
                item.save()
            elif action == 'decrease':
                item.quantity -= 1
                if item.quantity == 0:
                    item.delete()
                else:
                    item.save()
        else:
            cart = request.session.get("cart", {})
            product_id = str(product_id)
            if product_id in cart:
                if action == "increase":
                    product = get_object_or_404(Product, id=product_id)
                    if cart[product_id] >= product.stock:
                        messages.warning(request, 'You cannot add more than the available stock.')
                        return redirect(request.META.get('HTTP_REFERER','Home'))
                    cart[product_id] += 1
                elif action == "decrease":
                    cart[product_id] -= 1
                    if cart[product_id] <= 0:
                        del cart[product_id]
            request.session["cart"] = cart

    messages.success(request, 'Item quantity has benn Updated')

    return redirect(request.META.get("HTTP_REFERER", "Home"))

def clear_cart(request):
    if request.user.is_authenticated:
        items = CartItem.objects.filter(user=request.user)
        items.delete()
    else:
        request.session.pop('cart', None)
    messages.warning(request, 'All Cart Items has been Cleared!')
    return redirect(request.META.get("HTTP_REFERER", "Home"))



def Products(request):
    clear_all_filters = request.GET.get('clearAllFilters', 0)

    if (clear_all_filters):
        request.session.pop('productsCategory', None)
        request.session.pop('productsOrganic', None)
        request.session.pop('productsSort', None)
        request.session.pop('productsMin_price', None)
        request.session.pop('productsMax_price', None)

    category = request.GET.get("category", request.session.get('productsCategory',''))
    organic = request.GET.get("organic", request.session.get('productsOrganic', ''))
    sort = request.GET.get("sort", request.session.get('productsSort', ''))
    min_price = request.GET.get("minPrice", request.session.get('productsMin_price', ''))
    max_price = request.GET.get("maxPrice", request.session.get('productsMax_price', ''))

    products_data = Product.objects.all()
    categories = Category.objects.all()

    if category:
        products_data = products_data.filter(category__slug = category)
        request.session['productsCategory'] = category
    
    if organic == 'true':
        products_data = products_data.filter(is_organic=True)
        request.session['productsOrganic'] = organic

    if min_price:
        products_data = products_data.filter(price__gte=min_price)
        request.session['productsMin_price'] = min_price 

    if max_price:
        products_data = products_data.filter(price__lte=max_price)
        request.session['productsMax_price'] = max_price

    if sort:
        request.session['productsSort']  = sort
        if sort == "price_asc":
            products_data = products_data.order_by('price')
        elif sort == 'price_desc':
            products_data = products_data.order_by("-price")
        elif sort == 'rating':
            products_data = products_data.order_by("-rating")
        elif sort == "newest":
            products_data = products_data.order_by("-created_at")
        elif sort == 'name':
            products_data = products_data.order_by('name')

    paginator = Paginator(products_data, 12)

    page_number = request.GET.get("page")

    products_data = paginator.get_page(page_number)

    context = {
        "cart" : cart(request),
        'products': products_data,
        'category':category, 
        'categories':categories,
        'organic':organic,
        'sort':sort,
        'minPrice':min_price,
        'maxPrice':max_price,
    }
    return render(request, "Products.html", context=context)

def ProductPage(request,pdid):
    product = get_object_or_404(Product, id=pdid)

    if not product:
        messages.error(request, f"Product with Product Id = {pdid} is not present in data base")
        return redirect(request.META.get("HTTP_REFERER", "Products"))
    
    relatedProducts = Product.objects.filter(category=product.category).exclude(id=pdid)[:8]

    cartData = request.session.get("cart",{})
    # product_id = str(product.id)
    displayQuantity = cartData.get(str(pdid), 0)
    inCart = str(pdid) in cartData
    

    reviews = generate_dummy_reviews(product)
    breakdown = get_rating_breakdown(reviews)

    context={
        'pdid': pdid,
        'product':product,
        'relatedProducts':relatedProducts,
        'cart': cart(request),
        'displayQuantity': displayQuantity,
        'inCart': inCart,
        'reviews':reviews,
        'breakdown':breakdown,
        'maxRatingCount':max(breakdown),
    }
    return render(request, "ProductPage.html", context=context)

def SearchResults(request):
    cartData = cart(request)

    search = request.GET.get('search','')

    resultProducts = Product.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    )

    context = {
        'search':search,
        'products': resultProducts,
        'cart': cartData,
    }
    return render(request, "SearchResults.html", context=context)

def FlashDeals(request):
    cartData = cart(request)
    
    products = Product.objects.filter( stock__gt= 0, discount__gt=0).order_by('-discount')[:10]

    context={
        'cart':cartData,
        'products':products,
    }
    return render(request, "FlashDeals.html", context=context)

# from here all are needed authentication verification
@login_required(login_url='Login')
def Checkout(request):
    cartData = cart(request)

    addresses = Address.objects.filter(user=request.user)
    address = None
    newAdd = request.GET.get('addrId','')
    prevAdd = request.session.get('addrId','')
    if newAdd:
        address = addresses.filter(id=int(newAdd)).first()
        request.session['addrId'] = address.id
    elif prevAdd:
        address = addresses.filter(id=int(prevAdd)).first()
    else:
        address = addresses.filter(is_default=True).first()
        request.session['addrId'] = address.id

    paymentMethod = request.session.get("paymentMethod", "cash")
    if request.method == "POST":
        paymentMethod = request.POST.get("payment_method")
        request.session["paymentMethod"] = paymentMethod


    step = request.GET.get("step", "address")
    steps = [
        {'key':'address', 'label':'Address', 'icon':'map-pin'},
        {'key':'payment', 'label':'Payment', 'icon':'credit-card'},
        {'key':'review', 'label':'Review', 'icon':'check'},
    ]

    if request.GET.get('placeOrder'):
        order = Order.objects.create(
            user=request.user,
            shipping_address=address,
            payment_method=paymentMethod,
            subtotal=cartData['cart_total'],
            delivery_fee=cartData['delivery_fee'],
            tax=cartData['tax'],
            total=cartData['last_total'],
            status='Placed',
        )

        for item in cartData['cart_items']:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price=item['total'],
            )

        OrderStatus.objects.create(
            order=order,
            status='Placed',
            note='Order Placed Successfully',
        )

        clear_cart(request)
        messages.success(request, 'Your order has been placed')
        return redirect('Home')

    context = {
        "cart":cartData,
        'addresses':addresses,
        'address':address,
        'paymentMethod':paymentMethod,
        'step':step,
        'steps':steps,
    }
    return render(request, "Checkout.html", context=context)

@login_required(login_url='Login')
def MyOrders(request):

    activeTab = request.GET.get('activeTab','All Orders')
    if activeTab == 'All Orders':
        orders = Order.objects.filter(user=request.user)
    elif activeTab == 'Placed':
        orders = Order.objects.filter(user=request.user, status__in=[ 'Placed', 'Confirmed', 'Assigned', 'Packed'])
    else:
        orders = Order.objects.filter(user=request.user, status=activeTab)

    statusCol = statusColors()
    for order in orders:
        order.statusColour = statusCol.get(order.status, 'bg-gray-100 text-gray-700') # will raise error for unexpeted status
        order.itemsExtraCount = max(order.items.count()-4, 0)

    context={
        'cart':cart(request),
        'orders':orders.prefetch_related('items__product').order_by('-created_at'),
        'tabs':['All Orders', 'Placed', 'Out for Delivery', 'Delivered', 'Cancelled'],
        'activeTab':activeTab,
        'statusColours':statusCol,
    }
    return render(request, "MyOrders.html", context=context)

@login_required(login_url='Login')
def OrderTracking(request, odid):
    allStatus = ['Placed', 'Confirmed', 'Assigned', 'Packed', 'Out for Delivery', 'Delivered']
    statusCol = statusColors()

    order = get_object_or_404( Order, id=odid, user=request.user)
    order.statusColour = statusCol.get(order.status, 'bg-gray-100 text-gray-700')

    currentIdx = (allStatus.index(order.status) if order.status in allStatus else -1)

    showOtp = order.delivery_otp and order.status in allStatus[2:5]

    liveLocation = None
    if order.status in allStatus[2:5]:
        liveLocation = order.live_location

    # Status information for timeline
    statusHistory = {
            history.status: history.timestamp
            for history in order.history.all()
        }
    
    statusIcons = {
        'Placed': 'clock',
        'Confirmed': 'check',
        'Assigned': 'truck',
        'Packed': 'package',
        'Out for Delivery': 'truck',
        'Delivered': 'check',
    }

    allStatusInfo = [
        {
            'status': status,
            'icon': statusIcons.get(status, 'circle'),
            'timestamp': statusHistory.get(status),
        }
        for status in allStatus
    ]

    context={
        "order":order,
        'showOtp': showOtp,
        'liveLocation':liveLocation,
        'allStatus':allStatus,
        'currentIdx':currentIdx,
        'statusHistory':statusHistory,
        'allStatusInfo':allStatusInfo,
    }
    return render(request, "OrderTracking.html", context=context)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

@login_required(login_url='Login')
@csrf_exempt  # Remove @csrf_exempt if passing CSRF header/token from app
def update_driver_location(request, odid):
    """
    Endpoint called by driver's mobile app or GPS tracker to push location updates.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            lat = float(data.get("lat"))
            lng = float(data.get("lng"))

            # 1. Broadcast the new location to WebSocket subscribers
            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)(
                f"order_{odid}",
                {
                    "type": "location_update",
                    "lat": lat,
                    "lng": lng,
                }
            )

            # 2. Optionally update your DB / cache here if needed...

            return JsonResponse({"status": "success", "lat": lat, "lng": lng})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "invalid_method"}, status=405)

@login_required(login_url='Login')
def Addresses(request, id=None):

    addresses = Address.objects.filter(user=request.user).order_by('-is_default', '-updated_at')

    address = None
    if id:
        address = get_object_or_404(Address, id=id, user=request.user)

    if request.method == "POST":
        form = AddressForm(request.POST, instance=address)

        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()

            if id:
                messages.success(request, f'Address with label {address.label} has been Updated Successfully')
            else:
                messages.success(request, 'New Address has been Added Successfully')
            return redirect('Addresses')
    else:
        form = AddressForm(instance=address)

    context = {
        'addresses': addresses,
        'form' : form,
        'isEdit':address is not None,
        'address':address,
    }
    return render(request, "Addresses.html", context=context)

@login_required(login_url='Login')
def AddressDelete(request, addid):
    address = get_object_or_404(Address, user=request.user, id=addid)
    address.delete()
    messages.warning(request, 'Address has been Deleted')
    return redirect(request.META.get("HTTP_REFERER", "Addresses"))