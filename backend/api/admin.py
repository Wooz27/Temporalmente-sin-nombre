from django.contrib import admin
from .models import Owner, Animal
from django.utils.html import format_html
from django import forms
from .utils import generate_qr_base64
from django.db.models import Q
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.urls import reverse_lazy

admin.site.site_header = "Panel de Adopciones "
admin.site.site_title = "Adopciones"
admin.site.index_title = "Gestión del Refugio"



@admin.register(Animal)
class AnimalAdmin (admin.ModelAdmin):
    list_display = ("foto_thumbnail","name", "race", "age", "state", "owner", "public_id", "created_at" )
    list_filter = ("state", "name")
    search_fields = ("name", "public_id", "owner__name", "owner__number")
    list_select_related = ("owner",)
    readonly_fields = ("public_id", "created_at", "foto_preview","generate_qr","owner")


    # Distribucion visual del formulario
    fieldsets = (
        ("Identificador del Collar", {
            "fields": ("public_id", "generate_qr"),
            "description": "Este identificador se genera solo"
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



    @admin.display(description="Placa QR")
    def generate_qr (self, obj):
        if not obj.public_id:
            return "Aun no existe un el animal, no se puede generar qr"
        url = f"http://localhost:4321/collar/{obj.public_id}/"
        img = generate_qr_base64(url)
        
        return format_html(
                '<img src="data:image/png;base64,{}" style="width:300px; height: 300px; border-radius: 6px;" />',
                img
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
        label = "Asignar mascotas",
        widget = FilteredSelectMultiple (verbose_name = "Mascotas", is_stacked = False)
    )

    class Media:
        css = {"all": ("admin/css/widgets.css",)}
        js = (
            reverse_lazy("admin:jsi18n"),
            "admin/js/core.js",
            "admin/js/SelectBox.js",
            "admin/js/SelectFilter2.js",
        )

    class Meta:
        model = Owner
        fields = "__all__"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if self.instance.pk:
            self.fields ["animals_assigned"].initial = self.instance.animals.all()
            self.fields ["animals_assigned"].queryset = Animal.objects.filter(Q(owner = self.instance) | Q (owner__isnull = True, state = "disponible"))
        else:
            self.fields["animals_assigned"].queryset = Animal.objects.filter(owner__isnull = True, state= "disponible")

    
    


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ("name", "number", "total_pets", )
    search_fields = ("name", "number")
    form = OwnerAdminForm

    def save_related(self, request, form, formsets, change):
      super().save_related(request, form, formsets, change)

      # sacar los datos del dueño 
      owner = form.instance

      # extraer la info limpia y los animales seleccionados
      animals_select = form.cleaned_data.get("animals_assigned", [])
      ids_select = [animal.id for animal in animals_select]

      # Si se desmarca alguno liberar por sobre escritura
      owner.animals.exclude(id__in=ids_select).update(
        owner=None, state="disponible"
      )

      # Asignar esta real
      Animal.objects.filter(id__in=ids_select).update(
          owner=owner, state="adoptado"
      )
    
    @admin.display(description="Mascotas Adoptadas")
    def total_pets(self, obj):
        return obj.animals.count()