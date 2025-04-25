from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Agent, Post, Service

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'admin_image')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'image_preview')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'image', 'image_preview')
        }),
        ('Date Information', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="300" />')
        return 'No Image'

    def admin_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="50" height="50" style="object-fit: cover;" />')
        return 'No Image'

    image_preview.short_description = 'Image Preview'
    admin_image.short_description = 'Image'

class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'order')
    search_fields = ('name', 'description')
    list_editable = ('order',)

admin.site.register(Agent)
admin.site.register(Post, PostAdmin)
admin.site.register(Service, ServiceAdmin)