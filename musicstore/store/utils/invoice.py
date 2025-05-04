import os
from django.conf import settings
from store.utils.encryption import encrypt_message
from store.utils.ipfs_upload import upload_to_ipfs

def generate_invoice_and_upload(cart, total):
    content = "\n".join([
        f"{item['name']} x{item['quantity']} = ${item['price'] * item['quantity']}"
        for item in cart.values()
    ])
    content += f"\nTotal: ${total}"

    encrypted_data = encrypt_message(content)

    invoice_path = os.path.join(settings.BASE_DIR, 'store', 'invoices', 'invoice.txt')
    os.makedirs(os.path.dirname(invoice_path), exist_ok=True)
    with open(invoice_path, 'wb') as f:
        f.write(encrypted_data)

    ipfs_hash = upload_to_ipfs(invoice_path)
    os.remove(invoice_path)

    return ipfs_hash
