import uuid
from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import uuid


def generate_product_id():
    return f"USR{uuid.uuid4().hex[:12].upper()}"



class User(models.Model):
    ROLE_CHOICES = (
        ("ADMIN", "Admin"),
        ("USER", "User"),
    )
    id = models.CharField(
        primary_key=True,
        max_length=30,
        editable=False,
        default=generate_product_id
    )

    
    email = models.EmailField(unique=True)
    contact_number = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=50,null=False)
    last_name = models.CharField(max_length=50,null=True)
    

    password = models.CharField(max_length=128)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="USER")

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        db_table = 'user'
        
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.email
    
    @property
    def is_authenticated(self):
        """
        Required for DRF permission compatibility.
        Any valid JWT-authenticated user is authenticated.
        """
        return True
        
