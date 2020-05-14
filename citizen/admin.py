from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Citizen, Appointment, Noc, Compliant, User
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserAdminCreationForm, UserAdminChangeForm


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('uid', 'phone', 'is_admin')
    list_filter = ('is_admin', 'is_staff')
    fieldsets = (
        (None, {'fields': ('uid', 'password')}),
        ('Personal info', {'fields': ('name', 'email', 'phone', 'state')}),
        ('Permissions', {'fields': ('is_admin','is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user. ( add user with fields below )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('uid', 'name', 'phone', 'email', 'state', 'password1', 'password2')}
        ),
    )
    search_fields = ('uid', 'phone')
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)



# Remove Group Model from admin. We're not using it.

admin.site.register(Citizen)
admin.site.register(Compliant)
admin.site.register(Appointment)
admin.site.register(Noc)
