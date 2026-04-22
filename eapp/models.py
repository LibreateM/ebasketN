from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.
class Contact(models.Model):
    FullName = models.CharField(max_length=20)
    number = models.CharField(max_length=12)
    message = models.TextField()
    email= models.EmailField()
    created= models.DateField(auto_now_add=True)
    modified= models.DateField(auto_now=True)
    def __str__(self):
        return f"{'self.FullName, self.number, self.message,self.email, self.created, self.modified'}"
class ReviewForm(models.Model):
    name = models.CharField(max_length=20)
    star = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    review = models.TextField()
    created= models.DateField(auto_now_add=True)
    modified= models.DateField(auto_now=True)
    def __str__(self):
        return f"{'self.name, self.star, self.review,self.created, self.modified'}"

class Category(models.Model):
    category = models.CharField(max_length=100)
    pic = models.ImageField(upload_to='uploads/category/', null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return self.category\

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product = models.CharField(max_length=100)
    price = models.IntegerField()
    star = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    pic = models.ImageField(upload_to='uploads/product/', null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)

    def __str__(self):
        return f"{'self.product, self.star, self.price,self.created, self.modified'}"
class Cart(models.Model):
    user     = models.ForeignKey(User, on_delete=models.CASCADE)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created  = models.DateField(auto_now_add=True)
    modified = models.DateField(auto_now=True)
 
    def __str__(self):
        # FIX: was returning a literal string; now returns actual field values
        return f"{self.user.username} | {self.product.product} | qty:{self.quantity}"
 
    @property
    def total_price(self):
        """Convenience property usable in templates as {{ item.total_price }}"""
        return self.product.price * self.quantity

class Wish(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  
    def __str__(self):
        return f"{self.user.email} - {self.product.product}"

class Address(models.Model):
    name = models.CharField(max_length=20)
    user     = models.ForeignKey(User, on_delete=models.CASCADE)

    number = models.CharField(max_length=12)
    add1=models.CharField()
    add2=models.CharField(null=True, blank=True)
    city=models.CharField()
    state=models.CharField()
    zipcode=models.CharField()
    country=models.CharField()
    created= models.DateField(auto_now_add=True)
    modified= models.DateField(auto_now=True)
    def __str__(self):
        return f"{'self.name,self.user, self.number,self.add1, self.add2,self.city,self.state,self.zipcode,self.country,self.created, self.modified'}"


class PaymentMethod(models.Model):

    METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('netbanking', 'Net Banking'),
        ('cod', 'Cash on Delivery'),
    ]

    PAYPAL_CHOICES = [
        ('domestic', 'Domestic'),
        ('international', 'International'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    method_type = models.CharField(max_length=20, choices=METHOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    card_owner = models.CharField(max_length=100, blank=True, null=True)

    paypal_type = models.CharField(max_length=20, choices=PAYPAL_CHOICES, blank=True, null=True)

    bank_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.method_type}"
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField()
    payment_method = models.CharField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return f"{self.product.product} ({self.quantity})"

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
 
    def is_valid(self):
        """Token is valid for 1 hour and not yet used."""
        expiry = self.created_at + timedelta(hours=1)
        return not self.is_used and timezone.now() < expiry
 
    def __str__(self):
        return f"ResetToken for {self.user.email} ({'used' if self.is_used else 'valid'})"



class ContactReply(models.Model):
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    reply_message = models.TextField()
    replied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to {self.contact.email}"
 