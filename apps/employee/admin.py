from django.contrib import admin

# Register your models here.
from employee.models import Contact, Social


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'description', 'title', 'contact_type']
    list_display_links = ['title', 'id']


@admin.register(Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ['id', 'instagram', 'telegram']
