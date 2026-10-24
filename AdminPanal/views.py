from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render,redirect, get_object_or_404

from AdminPanal.decorators import admin_required
from AdminPanal.dummyData import dummy_admin_dashboard_data
from DeliveryPartner.dummyData import dummy_delivery_partner_data
from FeaturesApp.dummyData import dummyCategoriesData, dummyDashboardOrdersData, dummyProducts
from FeaturesApp.models import Category, DeliveryPartner, Order, OrderStatus, Product
from accounts import admin
from accounts.models import User

from .forms import AdminProductForms


# Create your views here.
AdminLinkData = [
    { 'to': "AdminDashboard", 'label': "Dashboard", 'icon': 'bar-chart-3' },
    { 'to': "AdminProductForm", 'label': "Add Product", 'icon': 'plus' },
    { 'to': "AdminProducts", 'label': "Products", 'icon': 'package-search' },
    { 'to': "AdminOrders", 'label': "Orders", 'icon': 'shopping-bag' },
    { 'to': "AdminDeliveryPartners", 'label': "Delivery Partners", 'icon': 'truck' },
    { 'to': "AdminLogout", 'label': "Exit", 'icon': 'log-out' },
]

@admin_required
def AdminLogout(request):
    logout(request.user)
    messages.warning(request, 'User has been Logged Out.')
    return redirect('Login')

def AdminDashboard(request):

    stats = {}
    stats['totalOrders'] = Order.objects.count()
    stats['totalUsers'] = User.objects.count()
    stats['totalProducts'] = Product.objects.count()
    stats['outOfStock'] = Product.objects.filter(stock__lte=0).count()
    stats['totalPartners'] = DeliveryPartner.objects.count()
    stats['recentOrders'] = Order.objects.all().order_by('-created_at')
    
    if stats:
        cards = [
            { 'label': "Total Orders", 'value': stats['totalOrders'], 'icon': 'shopping-bag' },
            { 'label': "Total Users", 'value': stats['totalUsers'], 'icon': 'users' },
            { 'label': "Total Products", 'value': stats['totalProducts'], 'icon': 'package' },
            { 'label': "Out of Stock", 'value': stats['outOfStock'], 'icon': 'alert-triangle' },
        ]

    context={
        'AdminLinkData':AdminLinkData,
        'stats':stats,
        'cards':cards,
    }
    return render(request, 'admin/AdminDashboard.html', context=context)

@admin_required
def AdminProducts(request):
    products = Product.objects.all()

    context={
        'AdminLinkData':AdminLinkData,
        'products':products,
    }
    return render(request, 'admin/AdminProducts.html', context=context)

@admin_required
def AdminProductOutOfStock(request, id):
    product = get_object_or_404(Product, id=id)
    product.stock = 0
    product.save()
    messages.error(request, f'Product #{product.name} has been set Out of Stock!')
    return redirect('AdminProducts')

@admin_required
def AdminProductForm(request, id=None):
    product=None

    if id:
        product = get_object_or_404(Product, id=id)

    if request.method == "POST":
        form = AdminProductForms(request.POST, request.FILES, instance=product,)

        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully')
            return redirect('AdminProducts')
    else:
        form = AdminProductForms(instance=product)

    context={
        'AdminLinkData':AdminLinkData,
        'isEdit':product is not None,
        'categoriesData':Category.objects.all(),
        'form':form,
        'product':product,
    }
    return render(request, 'admin/AdminProductForm.html', context=context)

@admin_required
def AdminOrders(request):
    orders = Order.objects.all().order_by('-created_at')
    partners = DeliveryPartner.objects.filter(is_active=True).order_by('user__email')
    statusOptions = ["Placed", "Confirmed", "Assigned", "Packed", "Out for Delivery", "Delivered", "Cancelled"]

    selectedPartner = ''
    if request.method == 'POST':
        if 'assignPartner' in request.POST:
            selectedPartner = request.POST.get('partner')
            order_id = request.POST.get('order_id')
            if selectedPartner:
                order = get_object_or_404(Order, id=order_id)
                partner = get_object_or_404(DeliveryPartner, id=selectedPartner)
                order.delivery_partner = partner
                order.status = 'Assigned'
                OrderStatus.objects.create(
                    order=order,
                    status='Assigned',
                )
                order.save()
                messages.success(request, f'For order #{order.id} delivery partner {partner.user} is assigned.')
        elif 'status_change' in request.POST:
            status = request.POST.get('status_change')
            order_id = request.POST.get('order_id')
            if status:
                order = get_object_or_404(Order, id=order_id)
                if order.status != status:
                    order.status = status
                    order.save()
                    OrderStatus.objects.create(
                        order=order,
                        status=status,
                    )
                messages.success(request, f'Updated status of order #{order_id} is {status}')

    assignModal = request.GET.get('assignModal')
    if assignModal :
        if assignModal == 'None':
            request.session['assignModal'] = None
            assignModal = None
        else:
            request.session['assignModal'] = assignModal
            selectedPartner = ''
    else:
        assignModal = request.session.get('assignModal')
    
    
    context={
        'AdminLinkData':AdminLinkData,
        'orders':orders,
        'partners':partners,
        'statusOptions':statusOptions,
        'assignModal':assignModal,
        'selectedPartner':selectedPartner,

    }
    return render(request, 'admin/AdminOrders.html', context=context)

@admin_required
def AdminDeliveryPartners(request):

    partners = DeliveryPartner.objects.all()

    active_status=request.GET.get('active_status')
    if active_status:
        partner_id = request.GET.get('partner_id',0)
        partner = partners.filter(id=int(partner_id)).first()
        if partner:
            partner.is_active = not partner.is_active
            partner.save()
            messages.success(request, f'Status of Delivery Parnter with ID #{partner_id} is Updated.')
        else:
            messages.warning(request, f'Delivery Partner with ID #{partner_id} is not availablein database!')
        return redirect('AdminDeliveryPartners')

    if request.method == 'POST':
        firstName=request.POST.get('first_name')
        middleName=request.POST.get('middle_name')
        lastName=request.POST.get('last_name')
        email=request.POST.get('email')
        password=request.POST.get('password')
        phone=request.POST.get('phone')
        vehicleType=request.POST.get('vehicle_type')

        if User.objects.filter(email=email):
            messages.warning(request, 'Account with this Email Id already exists!')
        elif User.objects.filter(username=f'{firstName}{middleName}{lastName}'):
            messages.warning(request, 'Account with this Name already exists!')
        else:
            user = User.objects.create_user(
                username=f'{firstName}{middleName}{lastName}',
                first_name=firstName,
                last_name=lastName,
                email=email,
                password=password,
                phone=phone,
                is_delivery_partner=True,
            )

            DeliveryPartner.objects.create(
                user=user,
                vehicle_type=vehicleType,
            )

            messages.success(request, "New delivery Partner has been created.")

    context={
        'AdminLinkData':AdminLinkData,
        'partners':partners,
    }
    return render(request, 'admin/AdminDeliveryPartners.html', context=context)