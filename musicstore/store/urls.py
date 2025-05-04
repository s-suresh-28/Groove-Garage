from django.urls import path
from .views import (
    home, category_products, product_detail,
    view_cart, add_to_cart, remove_from_cart,
    update_cart_quantity, about_us, contact_us, checkout,
    save_wallet, payment_success, process_payment
)

urlpatterns = [
    # Home Page
    path('', home, name='home'),
    
    # Category and Product Views
    path('category/<slug:slug>/', category_products, name='category_products'),
    path('product/<int:product_id>/', product_detail, name='product_detail'),
    
    # Cart Functionality
    path('cart/', view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:product_id>/', update_cart_quantity, name='update_cart_quantity'),
    
    # Static Pages
    path('about-us/', about_us, name='about_us'),
    path('contact-us/', contact_us, name='contact_us'),
    
    # Checkout Page
    path('checkout/', checkout, name='checkout'),

    # Save Wallet Address (MetaMask)
    path('save-wallet/', save_wallet, name='save_wallet'),

    # Payment Success and Processing
    path('payment-success/', payment_success, name='payment_success'),
    path('process-payment/', process_payment, name='process_payment'),
]

