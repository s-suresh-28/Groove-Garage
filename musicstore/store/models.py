from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from PIL import Image



def validate_image(image):
    try:
        img = Image.open(image)
        img.verify()  # Verify the image is valid
    except Exception:
        raise ValidationError("Invalid image. Please upload a valid image file.")


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)  # Ensure this exists
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to='products/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', default=1)
    is_featured = models.BooleanField(default=False)  # Ensure this field exists

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# store/models.py

from django.db import models

class Payment(models.Model):
    buyer_address = models.CharField(max_length=255)
    seller_address = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    transaction_hash = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_hash}"

# store/models.py
from django.db import models

class Invoice(models.Model):
    ipfs_hash = models.CharField(max_length=255)
    buyer_wallet = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
