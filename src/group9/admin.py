from django.contrib import admin

# Register your models here.
from .models import TextOptimization, Mistake

admin.site.register(TextOptimization)
admin.site.register(Mistake)