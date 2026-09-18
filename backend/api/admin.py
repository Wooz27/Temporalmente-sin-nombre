from django.contrib import admin
from .models import Owner, Animal
from django.utils.html import format_html
from django import forms

admin.site.site_header = "Panel de Adopciones "
admin.site.site_title = "Adopciones"
admin.site.index_title = "Gestión del Refugio"


class AnimalInline (admin.TabularInline):
    model = Animal
    extra = 0 
    fields = ("name", "race", "state", "public_id", )
    readonly_fields = ("name", "race", "state","public_id",)
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False
    
    
@admin.register(Animal)
class AnimalAdmin (admin.ModelAdmin):
    list_display = ("foto_thumbnail","name", "race", "age", "state", "owner", "public_id", "created_at" )
    list_filter = ("state", "name")
    search_fields = ("name", "public_id", "owner__name", "owner__number")
    list_select_related = ("owner",)
    readonly_fields = ("public_id", "created_at", "foto_preview")
    
    
    # Distribucion visual del formulario
    fieldsets = (
        ("Identificador del Collar", {
            "fields": ("public_id",),
            "description": "Este identificador se genera solo y se usa para el QR."
        }),
        ("Datos del Animal", {
            "fields": ("name", "age", "race", "state", "visual1", "foto_preview")
        }),
        ("Adopción", {
            "fields": ("owner",),
            "description": "Asigna un adoptante únicamente cuando el estado pase a 'adoptado'."
        }),
        ("Metadatos", {
            "fields": ("created_at",),
            "classes": ("collapse",)
        }),
    )

    # Miniatura pequeña para la tabla general
    @admin.display(description="Foto")
    def foto_thumbnail(self, obj):
        if obj.visual1:
            return format_html(
                '<img src="{}" style="width:80px; height: 80px; object-fit: cover; border-radius: 6px;" />',
                obj.visual1.url
            )
        return "Sin foto"
    
    # Previsualizacion grande dentro del formulario
    @admin.display(description="Vista previa actual")
    def foto_preview(self, obj):
        if obj.visual1:
            return format_html(
                '<img src="{}" style="max-width: 250px; height: auto; border-radius: 8px; border: 1px solid #ddd;" />',
                obj.visual1.url
            )
        return "No hay imagen subida aún"
    
    
    
    
class OwnerAdminForm(forms.ModelForm):
    animals_assigned = forms.ModelMultipleChoiceField(
        queryset= Animal.objects.all(),
        required = False,
        label = "Asignar mascotas"
        
    )


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "total_pets")
    search_fields = ("name", "number")
    
    inlines = [AnimalInline]
    
    @admin.display(description="Mascotas Adoptadas")
    def total_pets(self, obj):
        return obj.animals.count()