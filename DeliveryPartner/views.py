from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import logout, login, hashers, authenticate

from FeaturesApp.dummyData import dummyDashboardOrdersData, statusColors
from FeaturesApp.models import DeliveryPartner, Order, OrderStatus
from accounts.models import User
from .dummyData import dummy_delivery_partner_data
from .decorators import delivey_partner_required

# Create your views here.
def DeliveryLogin(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')

        user = authenticate(request, email=email, password=password)
        if user:
            if user.is_delivery_partner == False:
                messages.error(request, 'User cannot login as a Delivery Partner')
                return redirect('Home')
            
            if user.delivery_partner.is_active == False:
                messages.error(request, 'Your account has been Deactivated. Reactive it through Admin.')
                return redirect('DeliveryDashboard')
            
            login(request, user)
            messages.success(request, f'Welcome {user.first_name} {user.last_name} to Delivery Partners Panal.')
            return redirect('DeliveryDashboard') 
        else :
            messages.error(request, 'Entered Email or Password is not Wrong..')
            return redirect('DeliveryPartnerLogin')
        
    return render(request, 'delivery/DeliveryLogin.html')

@delivey_partner_required
def DeliveryLogout(request):
    logout(request)
    messages.warning(request, 'Your has been Logged Out!')
    return render(request, 'delivery/DeliveryLogin.html')

@delivey_partner_required
def DeliveryDashboard(request):
    orders = Order.objects.filter(delivery_partner__user=request.user)

    # tab acitve or completed
    tab = request.GET.get('tab','')
    if tab:
        request.session['deliveryPartnerTab'] = tab
    else:
        tab = request.session.get('deliveryPartnerTab', 'active') 

    if tab == 'completed':
        orders = orders.filter(status__in=['Delivered', 'Cancelled'])
    elif tab == 'active':
        orders = orders.filter(status__in=['Assigned', 'Packed', 'Out for Delivery'])
    
    # Tracking share location
    tracking = request.GET.get("tracking")
    if tracking is not None:
        tracking = tracking == "1"
        request.session["deliveryPartnerTracking"] = tracking
    else:
        tracking = request.session.get("deliveryPartnerTracking", False)

    orderStatusColors = statusColors()

    # otp verification form otpModal=order_id
    otpModal = request.GET.get("otpModal",'')
    if otpModal:
        if otpModal == 'None':
            request.session['deliveryPartnerOtpModal'] = None
            otpModal = None
        else:
            request.session['deliveryPartnerOtpModal'] = otpModal
    else:
        otpModel = request.session.get('deliveryPartnerOtpModal')

    submitting = False

    # Canceling order cancelModel=order_id
    cancelModal = request.GET.get("cancelModal",'')
    if cancelModal:
        if cancelModal == 'None':
            request.session['deliveryPartnerCancelModal'] = None
            cancelModal = None
        else:
            request.session['deliveryPartnerCancelModal'] = cancelModal
    else:
        cancelModel = request.session.get('deliveryPartnerCancelModal')


    context={
        'tab' : tab,
        'tracking': tracking,
        'orders':orders,
        'statusColors':orderStatusColors,
        'otpModal':otpModal,
        'cancelModal':cancelModal,
    }
    return render(request, 'delivery/DeliveryDashboard.html', context=context)

@delivey_partner_required
def UpdateDeliveryStatus(request, order_id):
    if request.method != "POST":
        return redirect('DeliveryDashboard')

    order = get_object_or_404(Order, id=order_id, delivery_partner__user=request.user)

    new_status = request.POST.get('status')

    allowed_transitions = {
        'Assigned':['Packed'],
        'Packed':['Out for Delivery'],
        'Out for Delivery':['Delivered'],
    }

    allowed_next_statuses = allowed_transitions.get(order.status, [])

    if new_status not in allowed_next_statuses:
        messages.error(request, f'Cannot change order from {order.status} to {new_status}')
        return redirect('DeliveryDashboard')


    order.status = new_status
    order.save()

    OrderStatus.objects.create(order=order, status=new_status)

    messages.success(request, f'Order #{str(order.id)[-6:].upper()} updated to {new_status}.')

    return redirect('DeliveryDashboard')

@delivey_partner_required
def VerifyOtp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        order_id = request.POST.get('order_id',0)

        order = get_object_or_404(Order, id=int(order_id))

        if order.status=='Delivered' or order.status=='Cancelled':
            messages.warning(request, 'Invalid Request')
            return redirect('DeliveryDashboard')

        if order.delivery_otp==otp:
            order.status = 'Delivered'
            order.save()
        
            OrderStatus.objects.create(order=order, status='Delivered')
            messages.success(request, 'Order has been delivered.')
        else:
            messages.error(request, 'Please enter Valid OTP given by Customer')

    return redirect('DeliveryDashboard')

@delivey_partner_required
def CancelModel(request):
    if request.method == 'POST':
        reason = request.POST.get('cancel_reason')
        order_id = request.POST.get('order_id',0)

        order = get_object_or_404(Order, id=int(order_id))

        if(order.status=='Delivered'):
            messages.warning(request, 'Cannot Cancel the Delivered Order')
            return redirect('DeliveryDashboard')
        
        order.status = 'Cancelled'
        order.save()

        OrderStatus.objects.create(order=order, status='Cancelled')
        messages.success(request, f'Order with Order Id #{order_id} has been Cancelled.')

    return redirect('DeliveryDashboard')