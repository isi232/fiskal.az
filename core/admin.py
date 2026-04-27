from django.contrib import admin
from .models import Complaint, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'phone', 'has_bank_card', 'created_at']
    search_fields = ['user__username', 'full_name', 'phone']

    def has_bank_card(self, obj):
        return bool(obj.card_number)
    has_bank_card.boolean = True
    has_bank_card.short_description = 'Kart var?'


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['shop_name', 'user', 'district', 'amount', 'date', 'status', 'created_at']
    list_filter = ['status', 'district', 'reason']
    search_fields = ['shop_name', 'description', 'user__username']
    list_editable = ['status']
    ordering = ['-created_at']
