from django.contrib import admin
from .models import Book
from django.contrib import admin
# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'excerpt']