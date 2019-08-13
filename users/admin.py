from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Account


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('id', 'email', 'full_name', 'loc','balance','is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active', 'loc',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'full_name', 'mobile_no', 'date_of_birth', 'loc','balance',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2','is_staff', 'is_active', 'full_name', 'mobile_no', 'date_of_birth', 'loc')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


# class AccountAdmin(admin.ModelAdmin):
#     """
#     Don't allow addition of more than one model instance in Django admin
#     See: http://stackoverflow.com/a/12469482
#     """
#     def has_add_permission(self, request):
#         if self.model.objects.filter().count() > 5:
#             return False
#         else:
#             return True


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Account, AccountAdmin)