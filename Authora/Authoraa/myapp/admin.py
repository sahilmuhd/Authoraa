from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, Role, UserProfile, Post, Category

# Custom admin for CustomUser
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'full_name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'full_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'role', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Role)
admin.site.register(UserProfile)

# Optional: Admin customization for Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'is_published')  # Add only fields that exist
    list_filter = ('status', 'is_published')
    search_fields = ('title', 'author__email')

    # Only include these if your model actually has them
    # readonly_fields = ('created_at', 'updated_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Category)
