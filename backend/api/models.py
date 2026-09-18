import uuid
from django.db import models

class Owner (models.Model):
    #Este campo es para los propietarios, pueden agregar los que gusten
    
    name = models.CharField(max_length=120, verbose_name="Nombre completo")
    number = models.CharField(max_length=15, verbose_name="WhatsApp")
    
    
    def __str__(self):
        return f"{self.name} ({self.number})"
    
    
    class Meta:
        verbose_name = "Adoptante"
        verbose_name_plural = "Adoptantes"

class Animal (models.Model):
    #Estados; se pueden Agregar más solo tengan en cuenta las validaciones
    STATE_CHOICES= (
        ("disponible", "Disponible"),
        ("adoptado", "Adoptado"),
    )
    #Este public id es el que se usa en el slug del Qr
    public_id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    
    #Info del animal
    name = models.CharField(max_length=50, verbose_name="Nombre de la mascota")
    age = models.PositiveIntegerField(verbose_name="Edad estimada")
    race = models.CharField (max_length=60, verbose_name="Raza")
    state = models.CharField(
        choices= STATE_CHOICES,
        max_length=50, default="disponible", 
        verbose_name="Estado de adopción",
        
        )
    visual1 = models.ImageField(
        upload_to="animals/",
        null=True,
        blank=True,
        verbose_name="Fotografía"
    )
    
    #Relación con el dueño para poder poder crear los filtros y etc. Hay que tener en cuenta que es de 1 a muchos
    owner = models.ForeignKey(
        Owner,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name= "animals",
        verbose_name="Adoptante asignado"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.state}" 
    
    class Meta:
        verbose_name = " Mascota"
        verbose_name_plural = "Mascotas"
    
    



