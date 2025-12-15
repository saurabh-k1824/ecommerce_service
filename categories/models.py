from django.db import models

import uuid

def generate_category_id():
    return f"CAT{uuid.uuid4().hex[:12].upper()}"



class Category(models.Model):
    id = models.CharField(
        primary_key=True,
        max_length=20,
        default=generate_category_id,
        editable=False,
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        db_table = "categories"
        
    def __str__(self):
        return self.name


