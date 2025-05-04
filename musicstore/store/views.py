from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.conf import settings
from .models import Product, Category
import json

# Home view - displays categories and featured products
def home(request):
    categories = Category.objects.filter(name__in=["Guitars", "Pianos", "Drums", "Flutes", "Saxophones", "Tools and Accessories"])
    featured_products = Product.objects.filter(is_featured=True)
    return render(request, 'store/home.html', {'categories': categories, 'featured_products': featured_products})

# Display products by category
def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'store/category_products.html', {'category': category, 'products': products})

# Product detail view
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})

# Add product to cart
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)
    
    # Debugging: print cart and product info
    print("Cart before adding:", cart)
    print(f"Adding product: {product.name}, Price: {product.price}")

    if str(product_id) not in cart:
        cart[str(product_id)] = {
            'name': product.name,
            'price': float(product.price),
            'quantity': 1,
            'image': product.image.url,
        }
    else:
        cart[str(product_id)]['quantity'] += 1

    request.session['cart'] = cart
    
    # Debugging: print cart after adding product
    print("Cart after adding:", cart)

    return redirect('view_cart')

# Remove product from cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('view_cart')

# Update cart quantity
def update_cart_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product = get_object_or_404(Product, id=product_id)

    if str(product_id) in cart:
        action = request.POST.get('action')

        if action == 'increase':
            cart[str(product_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(product_id)]['quantity'] > 1:
            cart[str(product_id)]['quantity'] -= 1

    request.session['cart'] = cart
    return redirect('view_cart')

# View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'store/cart.html', {'cart': cart, 'total': total})

# Checkout View
def checkout(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    return render(request, 'store/checkout.html', {
        'cart': cart,
        'total': total,
        'seller_address': settings.SELLER_ADDRESS,
        'escrow_contract_address': settings.ESCROW_CONTRACT_ADDRESS,
    })

# Save Wallet Address from MetaMask
def save_wallet(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        wallet_address = data.get('wallet_address')
        request.session['wallet_address'] = wallet_address
        return JsonResponse({'message': 'Wallet address saved'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

# About Us Page
def about_us(request):
    return render(request, 'store/about_us.html')

# Contact Us Page
def contact_us(request):
    return render(request, 'store/contact_us.html')

# Payment Success Page
def payment_success(request):
    ipfs_hash = request.GET.get('ipfs_hash', None)
    return render(request, 'store/payment_success.html', {'ipfs_hash': ipfs_hash})

from web3 import Web3

# Connect to Ganache (Ensure your port matches 7545)
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))

def send_payment(request):
    sender_address = "0xe7148f00FCbCc4A2664E44165D31f2b3d4fA596e"
    recipient_address = "0x9B85f8Eb9faF0c6D933BAea299f19f8815c608E7"
    private_key = "0xd38b2864de5e63921840c800411884c653119d7e83654577f240a44451b21a3c"

    # Build the transaction with higher gas limits
    transaction = {
        'from': sender_address,
        'to': recipient_address,
        'value': web3.to_wei(1, 'ether'),
        'gas': 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000,  # Increase gas limit here
        'gasPrice': web3.to_wei(50, 'gwei'),  # Increase gas price if needed
        'nonce': web3.eth.get_transaction_count(sender_address)
    }

    # Sign and send the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    return f"Transaction sent: {web3.to_hex(tx_hash)}"
    
    print("Block Gas Limit: ", web3.eth.get_block('latest')['gasLimit'])

# store/views.py

import os
from django.conf import settings
from django.shortcuts import render, redirect
from store.utils.encryption import encrypt_message
from store.utils.ipfs_upload import upload_to_ipfs

# Generate invoice, encrypt, upload to IPFS, and return hash
def generate_invoice_and_upload(cart, total):
    content = "\n".join([  # Creating the invoice content from the cart
        f"{item['name']} x{item['quantity']} = ${item['price'] * item['quantity']}"
        for item in cart.values()
    ])
    content += f"\nTotal: ${total}"

    # Encrypt the invoice content
    encrypted_data = encrypt_message(content)

    # Save the encrypted invoice locally
    invoice_path = os.path.join(settings.BASE_DIR, 'store', 'invoices', 'invoice.txt')
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)  # Create the directory if it doesn't exist
    with open(invoice_path, 'wb') as f:
        f.write(encrypted_data)

    # Upload to IPFS and get the IPFS hash
    ipfs_hash = upload_to_ipfs(invoice_path)

    # Remove the local invoice file after upload
    os.remove(invoice_path)

    return ipfs_hash

from django.shortcuts import render, redirect
from store.utils.invoice import generate_invoice_and_upload

def process_payment(request):
    cart = request.session.get('cart', {})
    total = sum(float(item['price']) * item['quantity'] for item in cart.values())

    ipfs_hash = generate_invoice_and_upload(cart, total)

    if ipfs_hash:
        return redirect(f'/payment-success/?ipfs_hash={ipfs_hash}')
    else:
        return render(request, 'store/payment_failed.html')

def payment_success(request):
    ipfs_hash = request.GET.get('ipfs_hash', None)
    return render(request, 'store/payment_success.html', {'ipfs_hash': ipfs_hash})
