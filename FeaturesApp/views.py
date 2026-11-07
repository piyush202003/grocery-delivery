from datetime import timedelta
from decimal import Decimal

from django.db import transaction
from django.db.models import F, Q
from django.db.models.aggregates import Avg, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBase, JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.utils import timezone

from razorpay.errors import SignatureVerificationError

from FeaturesApp.forms import AddressForm
from FeaturesApp.other_functions import create_review, edit_review, get_rating_breakdown, get_razorpay_client
from accounts.models import Address
from config import settings
from reviews.models import HelpfulVote, Review

from .dummyData import statusColors
from .models import CartItem, Category, Order, OrderItem, OrderStatus, Product

import logging

logger = logging.getLogger(__name__)

# Create your views here.
def Home(request):

    categories = Category.objects.all().order_by('slug')

    popularProducts = Product.objects.annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews__id')
    ).order_by('-average_rating')[:10]

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

    products_data = Product.objects.annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews__id')
    )
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
    product = get_object_or_404(
        Product.objects.annotate(
            average_rating=Avg('reviews__rating'),
            total_reviews=Count('reviews__id')
        ), id=pdid)

    if not product:
        messages.error(request, f"Product with Product Id = {pdid} is not present in data base")
        return redirect(request.META.get("HTTP_REFERER", "Products"))
    
    relatedProducts = Product.objects.filter(category=product.category).annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews__id')
    ).exclude(id=pdid)[:8]

    if request.user.is_authenticated:
        cartData = CartItem.objects.filter(user=request.user, product=product).first()
        if cartData:
            displayQuantity = cartData.quantity
            inCart=True
        else:
            inCart= False
            displayQuantity= 0
    else:
        cartData = request.session.get("cart", {})
        displayQuantity = cartData.get(str(pdid), 0)
        inCart = str(pdid) in cartData
        print(cartData)

    reviews = (
        Review.objects.filter(product=product)
        .select_related("user")
        .annotate(helpful_count=Count("helpful_votes"))
        .order_by("-created_at")
    )
    breakdown = get_rating_breakdown(reviews.values_list("rating", flat=True))
    now = timezone.now()

    for review in reviews:
        review.is_recent = review.created_at >= now - timedelta(days=7)

    user_review = None
    voted_review_ids=set()
    if(request.user.is_authenticated):
        user_review = Review.objects.filter(product=product, user=request.user).first()
        voted_review_ids = set(
            HelpfulVote.objects.filter(
                user=request.user,review__product=product
            ).values_list('review_id', flat=True)
        )

    # review_data = request.session.pop('review_data',None)
    review_data = None
    if request.GET.get('create_review',None):
        review_data = create_review(request, product_id=pdid)
    elif request.GET.get('edit_review', None):
        review_data = edit_review(request, user_review.id)
    if isinstance(review_data, HttpResponseBase):
        return review_data

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
        'user_review':user_review,
        'voted_review_ids':voted_review_ids,
        'data':review_data
    }
    return render(request, "ProductPage.html", context=context)

def SearchResults(request):
    cartData = cart(request)

    search = request.GET.get('search','')

    resultProducts = Product.objects.filter(
        Q(name__icontains=search) |
        Q(description__icontains=search)
    ).annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews__id')
    )

    context = {
        'search':search,
        'products': resultProducts,
        'cart': cartData,
    }
    return render(request, "SearchResults.html", context=context)

def FlashDeals(request):
    cartData = cart(request)
    
    products = Product.objects.filter( stock__gt= 0, discount__gt=0).annotate(
        average_rating=Avg('reviews__rating'),
        total_reviews=Count('reviews__id')
    ).order_by('-discount')[:10]

    context={
        'cart':cartData,
        'products':products,
    }
    return render(request, "FlashDeals.html", context=context)

# from here all are needed authentication verification
@login_required(login_url='Login')
def Checkout(request):

    cartData = cart(request)
    if not cartData['cart_items']:
        messages.info(request, "Your cart is empty.")
        return redirect('Home')

    addresses = Address.objects.filter(user=request.user)
    address_id = request.GET.get('addrId') or request.session.get('addrId')
    address = addresses.filter(id=address_id).first() if address_id else None

    if address is None:
        address = addresses.filter(is_default=True).first()

    if address is None:
        messages.info(request, 'Please add at least one address!')
        return redirect('Addresses')

    request.session['addrId'] = address.id

    paymentMethod = request.session.get("paymentMethod", "cash")

    step = request.GET.get("step", "address")

    steps = [
        {'key': 'address', 'label': 'Address', 'icon': 'map-pin'},
        {'key': 'payment', 'label': 'Payment', 'icon': 'credit-card'},
        {'key': 'review', 'label': 'Review', 'icon': 'check'},
    ]

    # Save selected payment method
    if request.method == "POST" and request.GET.get("step") == "review" and not request.POST.get("place_order"):

        selected_method = request.POST.get("payment_method")

        if selected_method not in ["card", "cash"]:
            messages.error(request, "Please select a valid payment method.")
            return redirect(f"{reverse('Checkout')}?step=payment")

        request.session["paymentMethod"] = selected_method

        return redirect(f"{reverse('Checkout')}?step=review")

    # Place order
    if request.method == "POST" and request.POST.get("place_order"):

        paymentMethod = request.session.get("paymentMethod", "cash")

        with transaction.atomic():

            order = Order.objects.create(
                user=request.user,
                shipping_address=address,
                payment_method=paymentMethod,
                subtotal=cartData['cart_total'],
                delivery_fee=cartData['delivery_fee'],
                tax=cartData['tax'],
                total=cartData['last_total'],
                status='Placed' if paymentMethod == 'cash' else 'Pending Payment',
                is_paid=False,
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
                status=order.status,
                note='Order Placed' if paymentMethod == 'cash' else 'Waiting for online payment',
            )

        # Cash on Delivery
        if paymentMethod == "cash":
            with transaction.atomic():
                cart_items = CartItem.objects.filter(user=request.user)
                for item in cart_items:
                    updated = Product.objects.filter(
                        id=item.product.id,
                        stock__gte=item.quantity
                    ).update(
                        stock=F('stock') - item.quantity
                    )

                    if updated == 0:
                        raise ValueError(
                            f"{item.product.name} is out of stock."
                        )
                clear_cart(request)
            messages.success(request, "Your order has been placed successfully!")
            return redirect('Home')

        # Online Payment
        if paymentMethod == "card":
            try:
                client = get_razorpay_client()
                razorpay_order = client.order.create({
                    "amount": int(order.total * 100),
                    "currency": "INR",
                    "receipt": f"order_{order.id}",
                })

                order.razorpay_order_id = razorpay_order['id']
                order.save(update_fields=['razorpay_order_id'])

                context = {
                    "order": order,
                    "razorpay_order_id": razorpay_order['id'],
                    "razorpay_key": settings.RAZORPAY_KEY_ID,
                    "razorpay_amount": int(order.total * 100),
                }

                return render(request, "components/Checkout/RazorpayPayment.html", context)

            except Exception as e:
                logger.exception("Razorpay order creation failed")
                messages.error( request, f"Payment initialization failed: {str(e)}")
                return redirect(f"{reverse('Checkout')}?step=review")

    context = {
        "cart": cartData,
        "addresses": addresses,
        "address": address,
        "paymentMethod": paymentMethod,
        "step": step,
        "steps": steps,
    }

    return render(request, "Checkout.html", context)

@login_required(login_url='Login')
@require_POST
def VerifyPayment(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    payment_id = request.POST.get("razorpay_payment_id")
    razorpay_order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    if not all([payment_id, razorpay_order_id, signature]):
        messages.error(request, "Payment details are incomplete.")
        return redirect('Checkout')

    if order.razorpay_order_id != razorpay_order_id:
        messages.error(request, "Invalid payment order.")
        return redirect('Checkout')

    client = get_razorpay_client()

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": razorpay_order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        })

        payment = client.payment.fetch(payment_id)

        if (
            payment['order_id'] != order.razorpay_order_id
            or int(payment['amount']) != int(order.total * 100)
            or payment['currency'] != "INR"
            or payment['status'] != "captured"
        ):
            messages.error(request, "Payment has not been confirmed.")
            return redirect('Checkout')

        with transaction.atomic():

            locked_order = Order.objects.select_for_update().get(
                id=order.id,
                user=request.user
            )

            if not locked_order.is_paid:

                locked_order.is_paid = True
                locked_order.razorpay_payment_id = payment_id
                locked_order.status = "Placed"

                locked_order.save(update_fields=[
                    "is_paid",
                    "razorpay_payment_id",
                    "status",
                    "updated_at",
                ])

                OrderStatus.objects.create(
                    order=locked_order,
                    status="Placed",
                    note="Online payment successful."
                )

        with transaction.atomic():
            cart_items = CartItem.objects.filter(user=request.user)
            for item in cart_items:
                updated = Product.objects.filter(
                    id=item.product.id,
                    stock__gte=item.quantity
                ).update(
                    stock=F('stock') - item.quantity
                )

                if updated == 0:
                    raise ValueError(
                        f"{item.product.name} is out of stock."
                    )
            clear_cart(request)

        messages.success(request, "Payment successful! Your order is confirmed.")

        return redirect('Home')
    
    except SignatureVerificationError:
        messages.error(request, "Payment verification failed.")
        return redirect('Checkout')

    except Exception:
        messages.error(request, "Unable to verify payment. Please contact support.")
        return redirect('Checkout')
    
@login_required(login_url='Login')
def PaymentFailed(request, order_id):
    try:
        order = Order.objects.filter(id=order_id, user=request.user).first()
        order.delete()
    except Exception as e:
        messages.error(request, e.message)

    messages.warning( request, "Payment was not completed. You can retry payment.")

    return redirect('Checkout')

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
        'carto_api_key':settings.CARTO_API_KEY,
    }
    return render(request, "OrderTracking.html", context=context)

@login_required(login_url='Login')
def get_delivery_location(request, order_id):

    try:
        order = Order.objects.get(id=order_id, user=request.user)
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found'
        }, status=404)
    

    if order.status != 'Out for Delivery':
        return JsonResponse({
            'success': False,
            'message': 'Order is not out for delivery yet'
        }, status=400)

    if not order.delivery_partner:
        return JsonResponse({
            'success': False,
            'message': 'No delivery partner assigned'
        }, status=404)

    if not order.live_location:
        return JsonResponse({
            'success': False,
            'message': 'Driver location not available yet'
        }, status=404)

    return JsonResponse({
        'success': True,
        'location': order.live_location
    })

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
        'cart':cart(request),
        'addresses': addresses,
        'form' : form,
        'isEdit':address is not None,
        'address':address,
        'CARTO_API_KEY':settings.CARTO_API_KEY
    }
    return render(request, "Addresses.html", context=context)

@login_required(login_url='Login')
def AddressDelete(request, addid):
    address = get_object_or_404(Address, user=request.user, id=addid)
    address.delete()
    messages.warning(request, 'Address has been Deleted')
    return redirect(request.META.get("HTTP_REFERER", "Addresses"))